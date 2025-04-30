import sqlite3

def initialize_database():
    conn = sqlite3.connect('biblioteca.db')
    cursor = conn.cursor()

    # Crearea tabelului genuri literare
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS genuri (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nume TEXT UNIQUE NOT NULL
    )
    ''')

    # Crearea tabelului carti
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS carti (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titlu TEXT NOT NULL,
        autor TEXT NOT NULL,
        gen_id INTEGER NOT NULL,
        disponibil INTEGER DEFAULT 1,
        FOREIGN KEY (gen_id) REFERENCES genuri (id)
    )
    ''')

    # Crearea tabelului utilizatori
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS utilizatori (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        parola TEXT NOT NULL,
        tip_utilizator TEXT NOT NULL CHECK(tip_utilizator IN ('admin', 'cititor')),
        nume_complet TEXT,
        email TEXT UNIQUE,
        telefon TEXT
    )
    ''')

    # Adaugă un utilizator implicit (admin)
    cursor.execute('''
    INSERT OR IGNORE INTO utilizatori (username, parola, tip_utilizator)
    VALUES ('admin', 'password', 'admin')
    ''')

    # Adaugă un utilizator
    cursor.execute('''
        INSERT OR IGNORE INTO utilizatori (username, parola, tip_utilizator)
        VALUES ('utilizator1', 'utilizator1', 'cititor')
        ''')

    cursor.execute('''
        INSERT OR IGNORE INTO utilizatori (username, parola, tip_utilizator)
        VALUES ('utilizator2', 'utilizator2', 'cititor')
        ''')

    conn.commit()
    conn.close()
    print("Baza de date a fost inițializată cu succes.")

def actualizeaza_baza_de_date():
    conn = sqlite3.connect('biblioteca.db')
    cursor = conn.cursor()

    # Adaugă coloanele necesare dacă acestea nu există deja
    try:
        cursor.execute("ALTER TABLE utilizatori ADD COLUMN nume_complet TEXT")
    except sqlite3.OperationalError:
        pass  # Coloana există deja

    try:
        cursor.execute("ALTER TABLE utilizatori ADD COLUMN email TEXT")
    except sqlite3.OperationalError:
        pass  # Coloana există deja

    try:
        cursor.execute("ALTER TABLE utilizatori ADD COLUMN telefon TEXT")
    except sqlite3.OperationalError:
        pass  # Coloana există deja

    conn.commit()
    conn.close()
    print("Structura bazei de date a fost actualizată.")

if __name__ == "__main__":
    initialize_database()
    actualizeaza_baza_de_date()
