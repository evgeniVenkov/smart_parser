import json
import pymysql
import os
import dotenv
dotenv.load_dotenv()
PASS_DB = os.getenv('PASS_DB')

# --- 🔧 Настройки подключения к MySQL ---
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": PASS_DB,
    "database": "smart_parser",
    "charset": "utf8mb4"
}
DATA = json.load(open('data/filter.json'))

def add_values(data):
    connection = pymysql.connect(**DB_CONFIG)
    cursor = connection.cursor()

    create_table_query = """
    CREATE TABLE IF NOT EXISTS products (
        id INT AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(255),
        link TEXT,
        thumbnail TEXT,
        source VARCHAR(100),
        price VARCHAR(50),
        currency VARCHAR(10)
    ) CHARACTER SET utf8mb4;
    """
    cursor.execute(create_table_query)

    insert_query = """
    INSERT INTO products (title, link, thumbnail, source, price, currency)
    VALUES (%s, %s, %s, %s, %s, %s)
    """

    for item in data:
        cursor.execute(insert_query, (
            item.get("title", ""),
            item.get("link", ""),
            item.get("thumbnail", ""),
            item.get("source", ""),
            str(item.get("price", "")),
            item.get('currency', "")
        ))

    connection.commit()
    print("✅ Данные успешно добавлены в таблицу `products`!")

    cursor.close()
    connection.close()


