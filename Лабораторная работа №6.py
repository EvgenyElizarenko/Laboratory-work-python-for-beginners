import sqlite3
from flask import Flask, render_template_string

# Создание базы данных и таблицы
def initialize_database():
    connection = sqlite3.connect("gifts.db")
    cursor = connection.cursor()

    # Создание таблицы
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS gifts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            gift TEXT NOT NULL,
            price REAL NOT NULL,
            status TEXT NOT NULL
        )
    """)

    # Заполнение таблицы данными
    gifts_data = [
        ("Иван Иванович Иванов", "Книга", 500.0, "куплен"),
        ("Петр Петрович Петров", "Набор чая", 300.0, "не куплен"),
        ("Мария Сидоровна Сидорова", "Плед", 1200.0, "куплен"),
        ("Ольга Алексеевна Смирнова", "Фоторамка", 800.0, "не куплен"),
        ("Анна Владимировна Орлова", "Часы", 2500.0, "куплен"),
        ("Дмитрий Сергеевич Иванов", "Кошелек", 1500.0, "не куплен"),
        ("Екатерина Павловна Петрова", "Сумка", 3000.0, "куплен"),
        ("Сергей Александрович Смирнов", "Портфель", 4000.0, "не куплен"),
        ("Наталья Викторовна Орлова", "Шарф", 700.0, "куплен"),
        ("Виктор Николаевич Васильев", "Ручка", 200.0, "не куплен")
    ]

    cursor.executemany("""
        INSERT INTO gifts (name, gift, price, status)
        VALUES (?, ?, ?, ?)
    """, gifts_data)

    connection.commit()
    connection.close()

# Flask приложение
app = Flask(__name__)

@app.route("/")
def show_gifts():
    connection = sqlite3.connect("gifts.db")
    cursor = connection.cursor()

    # Получение данных из таблицы
    cursor.execute("SELECT name, gift, price, status FROM gifts")
    gifts = cursor.fetchall()

    connection.close()

    # HTML-шаблон для отображения данных
    html_template = """
    <!doctype html>
    <html>
        <head>
            <title>Список подарков</title>
        </head>
        <body>
            <h1>Список подарков</h1>
            <table border="1">
                <tr>
                    <th>ФИО</th>
                    <th>Подарок</th>
                    <th>Стоимость</th>
                    <th>Статус</th>
                </tr>
                {% for gift in gifts %}
                <tr>
                    <td>{{ gift[0] }}</td>
                    <td>{{ gift[1] }}</td>
                    <td>{{ gift[2] }}</td>
                    <td>{{ gift[3] }}</td>
                </tr>
                {% endfor %}
            </table>
        </body>
    </html>
    """

    return render_template_string(html_template, gifts=gifts)

if __name__ == "__main__":
    initialize_database()
    try:
        print("Попытка запуска сервера...")
        app.run(host="127.0.0.1", debug=False)
    except Exception as unexpected_error:
        print(f"Произошла ошибка при запуске сервера: {unexpected_error}")
