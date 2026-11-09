# symmetric-encryption-cli

Een simpele command-line app waarmee je tekst kan versleutelen en weer ontsleutelen met symmetrische encryptie (AES-256-GCM).

## Onderzoek

### Symmetrische encryptie
- Is sneller en vraagt weinig rekenkracht
- Je gebruikt één en dezelfde sleutel om te versleutelen en te ontsleutelen
- Nadeel: je hebt een veilig kanaal nodig om de sleutel te delen, en die zou onderschept kunnen worden
- Het algoritme zelf is niet het probleem, AES wordt nog steeds als heel veilig gezien. Het zwakke punt zit puur in het delen van de sleutel

### Asymmetrische encryptie
- Is wat trager
- Voordeel: je hebt een public key en een private key, en die private key weet alleen jij
- Iemand versleutelt met jouw public key en alleen jij kan het met je private key weer ontsleutelen, dus je hoeft geen geheim te delen

### Praktijk
- In de praktijk worden ze meestal gecombineerd, HTTPS gebruikt asymmetrische encryptie om veilig een symmetrische sleutel af te spreken en daarna wordt alles weer symmetrisch versleuteld.

### Kerckhoffs's Principe
- Een versleutelingssysteem moet veilig zijn, zelfs als alle details van het systeem bekend zijn, behalve de sleutel
- Je beveiliging mag dus niet afhangen van het geheim houden van je code of je algoritme, alleen van de sleutel

### Keuze
- Ik heb voor dit project daarom ook gekozen om alleen symmetrische encryptie te gebruiken want ik ben de enige die versleutelt en ontsleutelt, het grootste nadeel van symmetrische encryptie oftewel het delen van de sleutel is niet van toepassing in dit project.

## Hoe de applicatie werkt

### Installeren en starten
```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

### Gebruik
- Na het starten krijg je een menu met 3 opties: versleutelen, ontsleutelen en afsluiten
- Bij versleutelen typ je de tekst en een wachtwoord (2x), daarna krijg je één lange tekst terug die je kan kopiëren
- Bij ontsleutelen plak je die tekst en typ je hetzelfde wachtwoord, dan krijg je je originele tekst weer terug
- Het wachtwoord typ je in met `getpass`, dus het is niet zichtbaar op je scherm terwijl je typt
- Als je een fout wachtwoord invult of als iemand de versleutelde tekst heeft aangepast krijg je een foutmelding en wordt er niks ontsleuteld

### Bestanden
- `crypto_utils.py`: hier zit alle encryptie in (`derive_key`, `encrypt` en `decrypt`)
- `main.py`: het menu van de CLI

### Wat er gebeurt bij versleutelen
1. Er wordt een willekeurige salt van 16 bytes gemaakt
2. Van het wachtwoord + de salt wordt met Argon2id een sleutel van 32 bytes gemaakt
3. Er wordt een willekeurige nonce van 12 bytes gemaakt
4. De tekst wordt versleuteld met AES-256-GCM
5. Alles wordt achter elkaar geplakt en omgezet naar base64 zodat je het makkelijk kan kopiëren

```
[ nonce: 12 bytes ][ salt: 16 bytes ][ ciphertext + tag ]
```

Als je twee keer dezelfde tekst met hetzelfde wachtwoord versleutelt krijg je elke keer een andere uitkomst, omdat de salt en de nonce elke keer nieuw zijn. Zo kan iemand die meekijkt niet zien dat twee berichten hetzelfde zijn.

## Algoritme: AES-256-GCM

- Ik gebruik AES-256, dat is de sterkste variant van AES met een sleutel van 32 bytes
- AES alleen is niet genoeg, je moet ook een modus kiezen. Ik heb gekeken naar ECB, CBC en GCM:
  - ECB versleutelt gelijke stukken tekst altijd op dezelfde manier waardoor patronen zichtbaar blijven (zoek maar eens op "ECB penguin"), dus die is niet te gebruiken voor gevoelige data
  - CBC is beter maar kan niet parallel draaien en controleert niet of iemand de versleutelde tekst heeft aangepast
  - GCM is snel, kan parallel draaien en is authenticated encryption. Er wordt een tag meegestuurd die controleert of de versleutelde tekst is aangepast, als dat zo is weigert het ontsleutelen. Daarom heb ik voor GCM gekozen
- Bij GCM mag je met dezelfde sleutel nooit twee keer dezelfde nonce gebruiken, daarom maak ik bij elke versleuteling een nieuwe aan met `os.urandom`
- Ik heb geen eigen encryptie geschreven maar gebruik de library `cryptography`, want "Don't roll your own crypto". In deze library zit ook Argon2id, dus ik heb maar één library nodig

## Sleutelbeheer

### Generatie
- De sleutel wordt niet willekeurig gemaakt en ergens opgeslagen, maar elke keer afgeleid van een wachtwoord
- Dit gebeurt met Argon2id (64 MB geheugen, 3 rondes, 4 threads), dezelfde instellingen die ik ook in mijn hashing opdracht van WP3 gebruikte
- Argon2id is expres traag en gebruikt veel geheugen, waardoor het veel moeilijker is om wachtwoorden te brute-forcen met een GPU

### Opslag
- De sleutel wordt nergens opgeslagen, die bestaat alleen even in het geheugen terwijl de app draait
- Wat wel bewaard wordt (in de versleutelde tekst zelf) is de salt en de nonce, maar die zijn niet geheim. Zonder het wachtwoord heb je er niks aan
- Ik heb er bewust niet voor gekozen om een sleutelbestand op mijn pc op te slaan, want dan kan iedereen die bij dat bestand komt alles ontsleutelen

### Uitwisseling
- In mijn geval is er geen uitwisseling nodig, want ik versleutel en ontsleutel zelf
- Als ik toch iets met iemand anders wil delen moet ik het wachtwoord via een ander veilig kanaal doorgeven, dus niet in hetzelfde bericht als de versleutelde tekst

### Beveiligingsimplicaties
- De sleutel is zo sterk als het wachtwoord, een zwak wachtwoord betekent een zwakke sleutel. Argon2id maakt het wel een stuk trager om te raden
- Als je je wachtwoord vergeet ben je je data kwijt, er is geen "wachtwoord vergeten"
- Voor mij als enige gebruiker werkt dit prima, maar bij veel gebruikers wordt het een probleem. Iedereen die met elkaar wil communiceren heeft dan een eigen gedeelde sleutel nodig en dat aantal groeit heel snel. Dan heb je eigenlijk asymmetrische encryptie nodig om de sleutels veilig uit te wisselen, zoals bij HTTPS

## Reflectie op Kerckhoffs's Principe
- Mijn app volgt Kerckhoffs's Principe: de code staat gewoon openbaar op GitHub, AES-GCM en Argon2id zijn bekende algoritmes en de salt en nonce staan zelfs gewoon in de versleutelde tekst
- Het enige geheim is het wachtwoord. Zolang dat sterk is en geheim blijft kan niemand de tekst ontsleutelen, ook niet als diegene precies weet hoe mijn app werkt
- Dit vind ik eigenlijk het mooiste van het hele principe: ik hoef mijn code niet te verstoppen om veilig te zijn

## Bronnen
- Biryukov, A., Dinu, D., Khovratovich, D., & Josefsson, S. (2021). *Argon2 memory-hard function for password hashing and proof-of-work applications* (RFC 9106). Internet Engineering Task Force. https://datatracker.ietf.org/doc/rfc9106/
- OWASP Foundation. (z.d.). *Password Storage Cheat Sheet*. OWASP Cheat Sheet Series. https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html
- Python Cryptographic Authority. (z.d.). *Authenticated encryption (AESGCM)*. cryptography documentation. https://cryptography.io/en/latest/hazmat/primitives/aead/
- Python Cryptographic Authority. (z.d.). *Key derivation functions (Argon2id)*. cryptography documentation. https://cryptography.io/en/latest/hazmat/primitives/key-derivation-functions/