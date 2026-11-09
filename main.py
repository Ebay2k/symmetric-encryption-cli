import getpass
from crypto_utils import encrypt, decrypt


def main():
    print("=== Symmetrische encryptie (AES-256-GCM) ===")
    while True:
        print("\n1. Tekst versleutelen")
        print("2. Tekst ontsleutelen")
        print("3. Afsluiten")
        keuze = input("Kies een optie: ").strip()

        if keuze == "1":
            tekst = input("Tekst om te versleutelen: ")
            wachtwoord = getpass.getpass("Wachtwoord: ")
            if getpass.getpass("Herhaal wachtwoord: ") != wachtwoord:
                print("Wachtwoorden komen niet overeen.")
                continue
            print("\nVersleutelde tekst:\n" + encrypt(tekst, wachtwoord))

        elif keuze == "2":
            token = input("Versleutelde tekst: ").strip()
            wachtwoord = getpass.getpass("Wachtwoord: ")
            try:
                print("\nOntsleutelde tekst:\n" + decrypt(token, wachtwoord))
            except ValueError as fout:
                print(fout)

        elif keuze == "3":
            break

        else:
            print("Ongeldige keuze.")


if __name__ == "__main__":
    main()