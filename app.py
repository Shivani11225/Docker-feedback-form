
import os
import time

import mysql.connector
from flask import Flask, render_template, request

app = Flask(__name__)

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "mysql"),
    "user": os.getenv("DB_USER", "feedback_user"),
    "password": os.getenv("DB_PASSWORD", "feedback_pass"),
    "database": os.getenv("DB_NAME", "feedback_db"),
}


def get_connection():
    return mysql.connector.connect(**DB_CONFIG)


def initialize_database():
    for attempt in range(30):
        try:
            connection = get_connection()
            cursor = connection.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS feedback (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    email VARCHAR(255) NOT NULL,
                    message TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            connection.commit()
            cursor.close()
            connection.close()
            print("Feedback table is ready.")
            return

        except mysql.connector.Error as error:
            print(f"Database not ready ({attempt + 1}/30): {error}")
            time.sleep(2)

    raise RuntimeError("Could not connect to MySQL.")


@app.route("/", methods=["GET", "POST"])
def index():
    success = False
    error = None

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        message = request.form.get("message", "").strip()

        if not name or not email or not message:
            error = "Please fill in all fields."
        elif len(name) > 100 or len(email) > 255 or len(message) > 5000:
            error = "One or more fields exceed the allowed length."
        else:
            connection = None
            cursor = None

            try:
                connection = get_connection()
                cursor = connection.cursor()

                cursor.execute(
                    """
                    INSERT INTO feedback (name, email, message)
                    VALUES (%s, %s, %s)
                    """,
                    (name, email, message),
                )

                connection.commit()
                success = True

            except mysql.connector.Error:
                error = "Unable to save feedback. Please try again."

            finally:
                if cursor:
                    cursor.close()
                if connection and connection.is_connected():
                    connection.close()

    return render_template("index.html", success=success, error=error)


if __name__ == "__main__":
    initialize_database()
    app.run(host="0.0.0.0", port=5000)

