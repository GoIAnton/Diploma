import psycopg2
import random
import pandas as pd
from sqlalchemy import create_engine


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
    

def update_table(id):
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="qwerty",
                                      host="db",
                                      port="5432",
                                      database="postgres")

        cursor = connection.cursor()
        print("Таблица до обновления записи")
        sql_select_query = """select * from pages_post where id = %s"""
        cursor.execute(sql_select_query, (id,))
        record = cursor.fetchone()
        print(record)

        sql_update_query = """Update pages_post set full_text = %s where id = %s"""
        cursor.execute(sql_update_query, (random.random()*100, id))
        connection.commit()
        count = cursor.rowcount
        print(count, "Запись успешно обновлена")      

    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Соединение с PostgreSQL закрыто")