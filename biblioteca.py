import sqlite3

class Biblioteca:
    def __init__(self, db_name='biblioteca.db'):
        self.db_name = db_name
        self.carti = []

    def incarca_date(self):
        """Încarcă datele din baza de date în memorie."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        # Obține toate cărțile din baza de date
        cursor.execute('''
        SELECT carti.id, carti.titlu, carti.autor, genuri.nume, carti.disponibil
        FROM carti
        JOIN genuri ON carti.gen_id = genuri.id
        ''')
        self.carti = cursor.fetchall()

        conn.close()

    def get_carti(self):
        """Returnează toate cărțile încărcate."""
        return self.carti

    def adauga_carte(self, titlu, autor, gen):
        """Adaugă o carte în baza de date."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        # Obține ID-ul genului
        cursor.execute('SELECT id FROM genuri WHERE nume = ?', (gen,))
        gen_id = cursor.fetchone()
        if not gen_id:
            print(f"Genul '{gen}' nu există.")
            return False

        cursor.execute('INSERT INTO carti (titlu, autor, gen_id) VALUES (?, ?, ?)', (titlu, autor, gen_id[0]))
        conn.commit()
        conn.close()
        return True

    def sterge_carte(self, id_carte):
        """Șterge o carte din baza de date."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute('DELETE FROM carti WHERE id = ?', (id_carte,))
        conn.commit()
        conn.close()
