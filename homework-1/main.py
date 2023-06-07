"""Скрипт для заполнения данными таблиц в БД Postgres."""
import csv
import psycopg2
from dotenv import dotenv_values

config = dotenv_values('.env')


def insert_data_from_csv(filename, table_name):
    with open(filename, 'r') as file:
        csv_data = csv.reader(file)
        header = next(csv_data)

        insert_query = f"INSERT INTO {table_name} VALUES ({', '.join(['%s'] * len(header))})"

        with psycopg2.connect(
                host=config['HOST'],
                user=config['USER'],
                password=config['PASSWORD'],
                database=config['DB_NAME'],
        ) as connection:
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
