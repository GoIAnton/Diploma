import psycopg2
import random
import pandas as pd
from sqlalchemy import create_engine


K = 200


def sql_to_df():
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
        df = pd.DataFrame(tuples_list, columns=['id', 'value', 'post_id', 'user_id'])
    except (Exception, psycopg2.Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
        return df


def df_to_sql(df):
    engine = create_engine('postgresql+psycopg2://postgres:qwerty@db:5432/postgres')
    df.to_sql('pages_recommendation1', engine, if_exists= 'replace')

    
def create_recommendations():
    df = sql_to_df()
    df = df.drop_duplicates()
    df = df.sort_values(by=['post_id'])

    unique_posts = df.post_id.unique()
    unique_users = df.user_id.unique()
    r_mean = {}
    for post in unique_posts:
        r_mean[post] = df.loc[df['post_id'] == post]['value'].mean()
    sim = pd.DataFrame(
        {
            'i': pd.Series(dtype='int64'),
            'cor': pd.Series(dtype='float64'),
            'j': pd.Series(dtype='int64')
        }
    )
    rec = pd.DataFrame(
        {
            'id': pd.Series(dtype='int64'),
            'value': pd.Series(dtype='float64'),
            'post_id': pd.Series(dtype='int64'),
            'user_id': pd.Series(dtype='int64')
        }
    )
    id = 0
    df_of_post = {}

    for i in unique_posts:
        df_of_post[i] = df[df['post_id'] == i]

    for i in unique_posts:
        for j in unique_posts:
            if i == j:
                continue
            sum1 = 0
            sum2 = 0
            sum3 = 0
            for u in unique_users:
                if (df_of_post[i]['user_id'].eq(u)).any():
                    r_ui = df_of_post[i].loc[df_of_post[i]['user_id'] == u].iloc[0]['value']
                else:
                    r_ui = 0
                if (df_of_post[j]['user_id'].eq(u)).any():
                    r_uj = df_of_post[j].loc[df_of_post[j]['user_id'] == u].iloc[0]['value']
                else:
                    r_uj = 0
                sum1 += (r_ui-r_mean[i]) * (r_uj-r_mean[j])
                sum2 += (r_ui-r_mean[i])**2
                sum3 += (r_uj-r_mean[j])**2
            if sum2==0 or sum3==0:
                continue
            sim = sim.append(
                {
                    'i': i,
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
            if (df_of_post[i]['user_id'].eq(u)).any():
                rec = rec.append(
                    {
                        'id': int(id),
                        'value': df_of_post[i].loc[df_of_post[i]['user_id'] == u].iloc[0]['value'],
                        'post_id': i,
                        'user_id': u
                    },
                    ignore_index=True,
                )
                id += 1
                continue
            sum1 = 0.0
            sum2 = 0.0
            for j in nearest_j:
                if (df_of_post[j]['user_id'].eq(u)).any():
                    r_uj = df_of_post[j].loc[df_of_post[j]['user_id'] == u].iloc[0]['value']
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
                    'post_id': i,
                    'user_id': u
                },
                ignore_index=True,
            )
            id += 1
        sim = sim.iloc[0:0]
    rec['id'] = rec['id'].apply(lambda f: format(f, '.0f'))
    rec['post_id'] = rec['post_id'].apply(lambda f: format(f, '.0f'))
    rec['user_id'] = rec['user_id'].apply(lambda f: format(f, '.0f'))
    rec['id'] = rec['id'].astype(int)
    rec['post_id'] = rec['post_id'].astype(int)
    rec['user_id'] = rec['user_id'].astype(int)
    
    df_to_sql(rec)