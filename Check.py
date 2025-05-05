import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import mysql.connector
from mysql.connector import Error
import time

LED_PIN = 17  

def connect_to_db():
    try:
        connection = mysql.connector.connect(
            host='',  
            database='',
            user='',  
            password=''
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Chyba připojení k databázi: {e}")
        return None


def get_user_name_by_card(card_number):
    try:
        connection = connect_to_db()
        if connection:
            cursor = connection.cursor()

            query = """
                SELECT u.name 
                FROM rfid_cards rc 
                JOIN users u ON rc.user_id = u.id 
                WHERE rc.card_number = %s
            """
            cursor.execute(query, (card_number,))
            result = cursor.fetchone()

            cursor.close()
            connection.close()

            if result:
                return result[0]
            else:
                return None  
    except Error as e:
        print(f"Chyba při komunikaci s databází: {e}")
        return None

def set_led(status):
    if status:
        GPIO.output(LED_PIN, GPIO.HIGH) 
        time.sleep(3)  
        GPIO.output(LED_PIN, GPIO.LOW) 
    else:
        GPIO.output(LED_PIN, GPIO.LOW) 

def main():

    GPIO.setmode(GPIO.BCM) 
    GPIO.setup(LED_PIN, GPIO.OUT) 

    reader = SimpleMFRC522()

    try:
        while True:
            print("Nyní přiložte kartu k přihlášení...")
            card_number = reader.read_id()  

            user_name = get_user_name_by_card(card_number)

            if user_name:
                print(f"Přihlášení úspěšné! Vitej: {user_name}")
                set_led(True) 
            else:
                print("Chyba: Tato karta není registrována.")
                set_led(False)  

            time.sleep(2)  

    except KeyboardInterrupt:
        print("Konec programu.")
    finally:
        GPIO.cleanup() 

if __name__ == "__main__":
    main()
