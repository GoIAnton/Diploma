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
    tzinfo = datetime.timezone(datetime.timedelta(hours=3.0))
    if 0 <= datetime.datetime.now(tzinfo).hour*60 + datetime.datetime.now(tzinfo).minute < 690:
        rec.to_sql('pages_recommendation1', engine, if_exists='replace')
    else:
        rec.to_sql('pages_recommendation2', engine, if_exists='replace')

def df_to_sql(df):
    engine = create_engine('postgresql+psycopg2://postgres:qwerty@db:5432/postgres')
    tzinfo = datetime.timezone(datetime.timedelta(hours=3.0))
    if 0 <= datetime.datetime.now(tzinfo).hour*60 + datetime.datetime.now(tzinfo).minute < 690:
        df.to_sql('pages_recommendation1', engine, if_exists='append')
    else:
        df.to_sql('pages_recommendation2', engine, if_exists='append')


def get_similar_users(data, publication_id):
    users = data[data['publication_id'] == publication_id]['user_id'].unique()
    return users


def weighted_average(data, ratings_matrix_k, U_k, publication_id, user_id):
    similar_users = get_similar_users(data, publication_id)
    similar_ratings = ratings_matrix_k[similar_users, publication_id]
    weights = np.dot(U_k[user_id], U_k[similar_users].T) / np.sum(np.abs(U_k[similar_users]), axis=1)
    predicted_rating = np.dot(weights, similar_ratings) / np.sum(np.abs(weights))
    # print(predicted_rating, flush=True)
    return predicted_rating


def create_recommendations():
    data = likes_sql_to_df()
    data = data.drop_duplicates()
    ratings = data.pivot_table(index='user_id', columns='publication_id', values='value')
    ratings = ratings.fillna(0)
    clear_rec()

    start = datetime.datetime.now()
    U, sigma, Vt = np.linalg.svd(ratings)
    print(U, flush=True)
    print(sigma, flush=True)
    print(Vt, flush=True)
    k = 50
    U_k = U[:, :k]
    sigma_k = np.diag(sigma[:k])
    Vt_k = Vt[:k, :]
    ratings_matrix_k = U_k @ sigma_k @ Vt_k
    recommendations = pd.DataFrame(columns=['id', 'pred_rating', 'publication_id', 'user_id'])
    # for publication_id in ratings.columns:
    #     for user_id in ratings.index:
    #         if ratings.loc[user_id, publication_id] == 0:
    #             pred_rating = weighted_average(data, ratings_matrix_k, U_k, publication_id, user_id)
    #             recommendations = recommendations.append({'id': len(recommendations),
    #                                                       'pred_rating': pred_rating,
    #                                                       'publication_id': publication_id,
    #                                                       'user_id': user_id}, ignore_index=True)
    recommendations = recommendations.sort_values(by='pred_rating', ascending=False)
    recommendations['id'] = recommendations['id'].apply(lambda f: format(f, '.0f'))
    recommendations['publication_id'] = recommendations['publication_id'].apply(lambda f: format(f, '.0f'))
    recommendations['id'] = recommendations['id'].astype(int)
    recommendations['publication_id'] = recommendations['publication_id'].astype(int)
    recommendations['user_id'] = recommendations['user_id'].astype(int)
    end = datetime.datetime.now()
    print(end-start, flush=True)
    df_to_sql(recommendations)
