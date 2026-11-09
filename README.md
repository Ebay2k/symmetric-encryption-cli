# symmetric-encryption-cli

### Symmetrische encryptie
- Is sneller en vraagt weinig rekenkracht
- Nadeel: je hebt een veilig kanaal nodig om de sleutel te delen, en die zou onderschept kunnen worden

### Asymmetrische encryptie
- Is wat trager
- Voordeel: je hebt een public key en een private key, en die private key weet alleen jij

### Praktijk
- In de praktijk worden ze meestal gecombineerd, HTTPS gebruikt asymmetrische encryptie om veilig een symmetrische sleutel af te spreken en daarna alles weer symmetrisch alles te versleutelen.

### Keuze
- Ik heb voor dit project daarom ook gekozen om alleen symmetrische encryptie te gebruiken want ik ben de enige die vesleutelt en ontsleutelt, het grootste nadeel van symmetrische encryptie oftewel het delen van de sleutel is niet van toepassing in dit project.