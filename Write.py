
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
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

def add_new_user(user_name):
    try:
        connection = connect_to_db()
        if connection:
            cursor = connection.cursor()

            insert_query = """INSERT INTO users (name) VALUES (%s)"""
            cursor.execute(insert_query, (user_name,))
            connection.commit()
            user_id = cursor.lastrowid  

            print(f"Nový uživatel {user_name} byl vytvořen s ID {user_id}.")

            cursor.close()
            connection.close()
            return user_id
    except Error as e:
        print(f"Chyba při přidávání uživatele do databáze: {e}")
        return None

def get_or_create_user_id(card_number):
    user_name = input("Zadejte jméno uživatele: ")

    try:
        if is_card_assigned(card_number):
            print(f"Chyba: Karta {card_number} je již přiřazena jinému uživateli.")
            return None

        connection = connect_to_db()
        if connection:
            cursor = connection.cursor()


            query = "SELECT id FROM users WHERE name = %s"
            cursor.execute(query, (user_name,))
            result = cursor.fetchone()

            if result:
                user_id = result[0]
                print(f"Uživatel {user_name} má ID {user_id}.")
            else:
                user_id = add_new_user(user_name)

            cursor.close()
            connection.close()
            return user_id
    except Error as e:
        print(f"Chyba při komunikaci s databází: {e}")
        return None

def is_card_assigned(card_number):
    try:
        connection = connect_to_db()
        if connection:
            cursor = connection.cursor()

            query = "SELECT id FROM rfid_cards WHERE card_number = %s"
            cursor.execute(query, (card_number,))
            result = cursor.fetchone()

            cursor.close()
            connection.close()

            if result:
                return True
            else:
                return False
    except Error as e:
        print(f"Chyba při komunikaci s databází: {e}")
        return True  

def write_card_to_db(card_number, user_id):
    try:
        connection = connect_to_db()
        if connection:
            cursor = connection.cursor()

            insert_query = """INSERT INTO rfid_cards (card_number, user_id) VALUES (%s, %s)"""
            cursor.execute(insert_query, (card_number, user_id))
            connection.commit()
            print(f"RFID karta {card_number} byla přiřazena uživateli s ID {user_id}.")

            cursor.close()
            connection.close()
    except Error as e:
        print(f"Chyba při zápisu do databáze: {e}")


def main():
    reader = SimpleMFRC522()

    try:
        print('Nyní přiložte kartu pro zápis...')
        card_number = reader.read_id()  
        print(f"Čtení karty: {card_number}")

        user_id = get_or_create_user_id(card_number) 
        if user_id is None:
            return

        write_card_to_db(card_number, user_id)

    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    main()
