from fastapi import FastAPI
import pymysql
import requests
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()
app = FastAPI()

connection = pymysql.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)

@app.get("/cartas")
def obtener_cartas():
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM cartas")
        return cursor.fetchall()

@app.get("/agregar/{id}")
def agregar_cartas(id: str):
    url = f"https://api.tcgdex.net/v2/en/cards/{id}"

    response = requests.get(url)

    data = response.json()

    name = data["name"]
    set = data["set"]["name"]
    precio = data["pricing"]["cardmarket"]["avg"]

    with connection.cursor() as cursor:
        sql = """
        INSERT INTO cartas (nombre, set_name, precio)
        VALUES (%s, %s, %s)
        """
        
        cursor.execute(sql, (name, set, precio))

    connection.commit()

    return {"Name": name,
            "Set" : set,
            "Precio":precio,
            "Mensaje":"Carta añadida correctamente v1"}

