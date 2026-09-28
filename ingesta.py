import pymysql
import csv
import boto3
import os

MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_PORT = int(os.getenv("MYSQL_PORT", 3306))
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")
MYSQL_TABLE = os.getenv("MYSQL_TABLE")

BUCKET_NAME = os.getenv("BUCKET_NAME")

connection = pymysql.connect(
    host=MYSQL_HOST,
    port=MYSQL_PORT,
    user=MYSQL_USER,
    password=MYSQL_PASSWORD,
    database=MYSQL_DATABASE
)

cursor = connection.cursor()
cursor.execute(f"SELECT * FROM {MYSQL_TABLE}")

rows = cursor.fetchall()
columnas = [descripcion[0] for descripcion in cursor.description]

with open("data.csv", "w", newline="") as archivo:
    writer = csv.writer(archivo)
    writer.writerow(columnas)
    writer.writerows(rows)

cursor.close()
connection.close()

s3 = boto3.client("s3")
s3.upload_file("data.csv", BUCKET_NAME, "data.csv")

print("Datos extraidos de MySQL y subidos a S3 correctamente")
