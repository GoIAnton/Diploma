import psycopg2
import datetime
import pandas as pd
import numpy as np
from sqlalchemy import create_engine

K = 50

def likes_sql_to_df():
    try:
        connection = psycopg2.connect(
            user="postgres",
            password="qwerty",
            host="db",
            port="5432",
            database="postgres"
        )
        cursor = connection.cursor()
        sql_select_query = """select * from pages_like"""
        cursor.execute(sql_select_query)
        tuples_list = cursor.fetchall()
        df = pd.DataFrame(tuples_list, columns=['id', 'value', 'publication_id', 'user_id'])
    except (Exception, psycopg2.Error) as error:
        print("Ошибка при работе с postgreSQL", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
        return df


def publications_sql_to_df():
    try:
        connection = psycopg2.connect(
            user="postgres",
            password="qwerty",
            host="db",
            port="5432",
            database="postgres"
        )
        cursor = connection.cursor()
        sql_select_query = """select * from pages_publication"""
        cursor.execute(sql_select_query)
        tuples_list = cursor.fetchall()
        df = pd.DataFrame(tuples_list, columns=[
            'id',
            'title',
            'full_text',
            'pub_date',
            'is_article',
            'is_hidden',
            'author',
        ])
    except (Exception, psycopg2.Error) as error:
        print("Ошибка при работе с postgreSQL", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
        return df

def clear_rec():
    engine = create_engine('postgresql+psycopg2://postgres:qwerty@db:5432/postgres')
    rec = pd.DataFrame(
        {
            'id': pd.Series(dtype='int64'),
            'value': pd.Series(dtype='float64'),
            'publication_id': pd.Series(dtype='int64'),
            'user_id': pd.Series(dtype='int64')
        }
    )
    if 0 <= datetime.datetime.now().hour*60 + datetime.datetime.now().minute < 720:
        rec.to_sql('pages_recommendation1', engine, if_exists='replace')
    else:
        rec.to_sql('pages_recommendation2', engine, if_exists='replace')
def df_to_sql(df):
    engine = create_engine('postgresql+psycopg2://postgres:qwerty@db:5432/postgres')
    if 0 <= datetime.datetime.now().hour*60 + datetime.datetime.now().minute < 720:
        df.to_sql('pages_recommendation1', engine, if_exists='append')
    else:
        df.to_sql('pages_recommendation2', engine, if_exists='append')

    
def create_recommendations():
    df = likes_sql_to_df()
    df = df.drop_duplicates()
    df = df.sort_values(by=['publication_id'])
    ratings = df.pivot_table(index='user_id', columns='publication_id', values='value')
    ratings = ratings.fillna(0)
    clear_rec()

    unique_publications = df.publication_id.unique()
    unique_users = df.user_id.unique()
    r_mean = {}
    for publication in unique_publications:
        r_mean[publication] = df.loc[df['publication_id'] == publication]['value'].mean()
    sim = pd.DataFrame(
        {
            'cor': pd.Series(dtype='float64'),
            'j': pd.Series(dtype='int64')
        }
    )
    rec = pd.DataFrame(
        {
            'id': pd.Series(dtype='int64'),
            'value': pd.Series(dtype='float64'),
            'publication_id': pd.Series(dtype='int64'),
            'user_id': pd.Series(dtype='int64')
        }
    )
    id = 0

    df_publications = publications_sql_to_df()
    df_publications['pub_date'] = pd.to_datetime(df_publications.pub_date).dt.tz_localize(None)
    publications = {}

    now = datetime.datetime.now()

    for i in unique_publications:
        pub = df_publications.loc[df_publications['id'] == i].iloc[0]
        publications[i] = pub
        if not (pub['is_article'] == True or (pub['is_article'] == False
            and now - pub['pub_date'] < datetime.timedelta(weeks=2))):
            unique_publications = np.delete(unique_publications, np.where(unique_publications == i))
    
    for i in unique_publications:
        start = datetime.datetime.now()
        for j in unique_publications:
            if i == j:
                continue
            sum1 = 0
            sum2 = 0
            sum3 = 0
            for u in unique_users:
                r_ui = ratings[i][u]
                r_uj = ratings[j][u]
                sum1 += (r_ui-r_mean[i]) * (r_uj-r_mean[j])
                sum2 += (r_ui-r_mean[i])**2
                sum3 += (r_uj-r_mean[j])**2
            if sum2==0 or sum3==0:
                continue
            sim = sim.append(
                {
                    'cor': sum1 / (sum2*sum3)**0.5,
                    'j': j
                },
                ignore_index=True,
            )

        sim = sim.sort_values(by=['cor'], ascending=False).head(n=K)
        nearest_j = sim['j'].tolist()
        nearest_cor = sim['cor'].tolist()
        j_cor = dict(zip(nearest_j, nearest_cor))

        for u in unique_users:
            if (ratings[i][u] > 0.01
                or publications[i]['author'] == u):
                continue
            sum1 = 0.0
            sum2 = 0.0
            for j in nearest_j:
                if ratings[j][u] > 0.01:
                    r_uj = ratings[j][u]
                else:
                    continue
                sum1 += (r_uj-r_mean[j]) * j_cor[j]
                sum2 += abs(j_cor[j])
            if sum2 == 0:
                continue
            rec = rec.append(
                {
                    'id': int(id),
                    'value': sum1 / sum2 + r_mean[i],
                    'publication_id': i,
                    'user_id': u
                },
                ignore_index=True,
            )
            id += 1
        sim = sim.iloc[0:0]
        rec['id'] = rec['id'].apply(lambda f: format(f, '.0f'))
        rec['publication_id'] = rec['publication_id'].apply(lambda f: format(f, '.0f'))
        rec['user_id'] = rec['user_id'].apply(lambda f: format(f, '.0f'))
        rec['id'] = rec['id'].astype(int)
        rec['publication_id'] = rec['publication_id'].astype(int)
        rec['user_id'] = rec['user_id'].astype(int)
        df_to_sql(rec)
        rec = rec.iloc[0:0]
    
    df_to_sql(rec)
