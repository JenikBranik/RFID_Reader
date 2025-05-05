import subprocess

def run_script(script_name):
    subprocess.run(f"source venv/bin/activate && python {script_name}", shell=True, executable="/bin/bash")

def menu():
    while True:
        print("\n=== HLAVNÍ MENU ===")
        print("1. Přihlásit uživatele (Check.py)")
        print("2. Zapsat novou kartu (Write.py)")
        print("3. Smazat databázi (Reset.py)")
        print("4. Konec")
        
        volba = input("Vyber akci (1-4): ")

        if volba == "1":
            run_script("Check2.py")
        elif volba == "2":
            run_script("Write.py")
        elif volba == "3":
            run_script("Reset.py")
        elif volba == "4":
            print("Ukončuji...")
            break
        else:
            print("Neplatná volba, zkus to znovu.")

if __name__ == "__main__":
    menu()
