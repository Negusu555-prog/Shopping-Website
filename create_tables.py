import pymysql

# הגדרות התחברות (מתחבר ל-localhost כי אנחנו מריצים מהמחשב שלך)
# הסיסמה והמשתמש תואמים למה שהגדרנו ב-docker-compose
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root_password',
    'database': 'main',
    'port': 3306
}


def create_tables():
    print("Connecting to database...")
    try:
        connection = pymysql.connect(**db_config)
    except Exception as e:
        print(f"Error connecting to DB: {e}")
        print("Make sure Docker is running (docker-compose up)")
        return

    try:
        with connection.cursor() as cursor:
            print("Reading init.sql file...")
            try:
                with open('init.sql', 'r', encoding='utf-8') as f:
                    sql_script = f.read()
            except FileNotFoundError:
                print("Error: Could not find 'init.sql' file in this folder!")
                return

            # פיצול הפקודות והרצתן אחת אחת
            commands = sql_script.split(';')
            for command in commands:
                if command.strip():
                    try:
                        print(f"Executing: {command[:50].strip()}...")
                        cursor.execute(command)
                    except Exception as e:
                        print(f"Error executing command: {e}")

        connection.commit()
        print("\n✅ Success! All tables created successfully.")

    finally:
        connection.close()


if __name__ == "__main__":
    create_tables()