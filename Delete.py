
import mysql.connector
from mysql.connector import Error

def connect_to_db():
    try:
        connection = mysql.connector.connect(
            host='',
            database='rfid_db', 
            user='',  
            password=''  
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Chyba připojení k databázi: {e}")
        return None

def delete_all_records():
    try:
        connection = connect_to_db()
        if connection:
            cursor = connection.cursor()

            delete_cards_query = "DELETE FROM rfid_cards"
            cursor.execute(delete_cards_query)
            connection.commit()
            print("Všechny karty byly smazány.")

            delete_users_query = "DELETE FROM users"
            cursor.execute(delete_users_query)
            connection.commit()
            print("Všichni uživatelé byli smazáni.")

            cursor.close()
            connection.close()

    except Error as e:
        print(f"Chyba při mazání záznamů: {e}")

def main():
    confirm = input("Jste si jistý, že chcete smazat všechny uživatele a karty? (y/n): ")
    if confirm.lower() == 'y':
        delete_all_records()
    else:
        print("Akce byla zrušena.")

if __name__ == "__main__":
    main()
