"""Скрипт для заполнения данными таблиц в БД Postgres."""
import csv
import psycopg2
from config import host, user, password, db_name


def create_table(table_name, columns):
    create_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns})"
    with psycopg2.connect(host=host, user=user, password=password, database=db_name) as connection:
        with connection.cursor() as cursor:
            cursor.execute(create_query)
            connection.commit()


def insert_data_from_csv(filename, table_name):
    with open(filename, 'r') as file:
        csv_data = csv.reader(file)
        header = next(csv_data)

        insert_query = f"INSERT INTO {table_name} VALUES ({', '.join(['%s'] * len(header))})"

        with psycopg2.connect(host=host, user=user, password=password, database=db_name) as connection:
            with connection.cursor() as cursor:
                try:
                    cursor.executemany(insert_query, csv_data)
                    connection.commit()
                    print(f"Данные из файла {filename} успешно добавлены в таблицу {table_name}.")
                except psycopg2.Error as error:
                    connection.rollback()
                    print(f"Ошибка при вставке данных из файла {filename} в таблицу {table_name}: {error}")


def main():
    insert_data_from_csv('north_data/employees_data.csv', 'employees')
    insert_data_from_csv('north_data/customers_data.csv', 'customers')
    insert_data_from_csv('north_data/orders_data.csv', 'orders')


if __name__ == '__main__':
    main()
