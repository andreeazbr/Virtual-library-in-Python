import sqlite3

def populate_books():
    conn = sqlite3.connect('biblioteca.db')
    cursor = conn.cursor()

    # Lista fixă de cărți
    books = [
        ("Mândrie și prejudecată", "Jane Austen", "Ficțiune"),
        ("Marile speranțe", "Charles Dickens", "Ficțiune"),
        ("Crimă și pedeapsă", "Fyodor Dostoevsky", "Ficțiune"),
        ("Jane Eyre", "Charlotte Brontë", "Ficțiune"),
        ("Frații Karamazov", "Fyodor Dostoevsky", "Ficțiune"),
        ("O mie și una de nopți", "Anonim", "Ficțiune"),
        ("La răscruce de vânturi", "Emily Brontë", "Ficțiune"),
        ("Procesul", "Franz Kafka", "Ficțiune"),
        ("Toată lumina pe care nu o putem vedea", "Anthony Doerr", "Ficțiune"),
        ("Harry Potter și Piatra Filozofală", "J.K. Rowling", "Fantasy"),
        ("Stăpânul inelelor: Frăția inelului", "J.R.R. Tolkien", "Fantasy"),
        ("Hobbitul", "J.R.R. Tolkien", "Fantasy"),
        ("Cronicile din Narnia: Leul, vrăjitoarea și dulapul", "C.S. Lewis", "Fantasy"),
        ("Jocul lui Ender", "Orson Scott Card", "Science Fiction"),
        ("Dune", "Frank Herbert", "Science Fiction"),
        ("Fundatia", "Isaac Asimov", "Science Fiction"),
        ("Războiul lumilor", "H.G. Wells", "Science Fiction"),
        ("2001: O odisee spațială", "Arthur C. Clarke", "Science Fiction"),
        ("Solaris", "Stanislaw Lem", "Science Fiction"),
        ("Frankenstein", "Mary Shelley", "Science Fiction"),
        ("O călătorie spre centrul Pământului", "Jules Verne", "Science Fiction"),
        ("Douăzeci de mii de leghe sub mări", "Jules Verne", "Science Fiction"),
        ("Misterul din Cârțișoara", "Ion Agârbiceanu", "Ficțiune"),
        ("Pădurea spânzuraților", "Liviu Rebreanu", "Ficțiune"),
        ("Ion", "Liviu Rebreanu", "Ficțiune"),
        ("Moromeții", "Marin Preda", "Ficțiune"),
        ("Ultima noapte de dragoste, întâia noapte de război", "Camil Petrescu", "Ficțiune"),
        ("Ciuleandra", "Liviu Rebreanu", "Ficțiune"),
        ("Baltagul", "Mihail Sadoveanu", "Ficțiune"),
        ("Groapa", "Eugen Barbu", "Ficțiune"),
        ("Enigma Otiliei", "George Călinescu", "Ficțiune"),
        ("Maitreyi", "Mircea Eliade", "Ficțiune"),
        ("Accidentul", "Mihail Sebastian", "Ficțiune"),
        ("Medalionul pierdut", "Eugen Lovinescu", "Ficțiune"),
        ("Biblia pierdută", "Igor Bergler", "Ficțiune"),
        ("Codul lui Da Vinci", "Dan Brown", "Ficțiune"),
        ("Îngeri și demoni", "Dan Brown", "Ficțiune"),
        ("Simbolul pierdut", "Dan Brown", "Ficțiune"),
        ("Inferno", "Dan Brown", "Ficțiune"),
        ("Origini", "Dan Brown", "Ficțiune"),
        ("Arta războiului", "Sun Tzu", "Non-ficțiune"),
        ("Gândirea rapidă și lentă", "Daniel Kahneman", "Non-ficțiune"),
        ("De ce națiunile eșuează", "Daron Acemoglu, James A. Robinson", "Non-ficțiune"),
        ("Sapiens: Scurtă istorie a omenirii", "Yuval Noah Harari", "Non-ficțiune"),
        ("Homo Deus: Scurtă istorie a viitorului", "Yuval Noah Harari", "Non-ficțiune"),
        ("21 de lecții pentru secolul XXI", "Yuval Noah Harari", "Non-ficțiune"),
        ("Mintea organizată", "Daniel J. Levitin", "Non-ficțiune"),
        ("Cum să-ți construiești rețele de succes", "Keith Ferrazzi", "Non-ficțiune"),
        ("Inteligența emoțională", "Daniel Goleman", "Non-ficțiune"),
        ("Călătorie în România interbelică", "Jean Bart", "Non-ficțiune"),
        ("Moby Dick", "Herman Melville", "Ficțiune"),
        ("Război și pace", "Lev Tolstoi", "Ficțiune"),
        ("De veghe în lanul de secară", "J.D. Salinger", "Ficțiune"),
        ("Don Quijote", "Miguel de Cervantes", "Ficțiune"),
        ("Dracula", "Bram Stoker", "Horror"),
        ("Portretul lui Dorian Gray", "Oscar Wilde", "Ficțiune"),
        ("Lumea bună nouă", "Aldous Huxley", "Science Fiction"),
        ("Fahrenheit 451", "Ray Bradbury", "Science Fiction"),
        ("Anna Karenina", "Lev Tolstoi", "Ficțiune"),
        ("Ulise", "James Joyce", "Ficțiune"),
        ("Omul invizibil", "H.G. Wells", "Science Fiction"),
        ("Mașina timpului", "H.G. Wells", "Science Fiction"),
        ("Basmele", "Margaret Atwood", "Science Fiction"),
        ("Drumul", "Cormac McCarthy", "Ficțiune"),
        ("Clopotul de sticlă", "Sylvia Plath", "Ficțiune"),
        ("Abatorul cinci", "Kurt Vonnegut", "Science Fiction"),
        ("Căpcăunul", "Joseph Heller", "Ficțiune"),
        ("Grădina secretă", "Frances Hodgson Burnett", "Ficțiune"),
        ("Strigoii", "Henry James", "Horror"),
        ("Adultera", "Simone de Beauvoir", "Ficțiune"),
        ("Pe drum", "Jack Kerouac", "Ficțiune"),
        ("Timpul unui om", "Günter Grass", "Ficțiune"),
        ("Noaptea", "Elie Wiesel", "Memorii"),
        ("Un veac de singurătate", "Gabriel García Márquez", "Ficțiune"),
        ("Luminile din noapte", "Carlos Ruiz Zafón", "Ficțiune"),
        ("Începutul", "David Baldacci", "Ficțiune"),
        ("Marele Gatsby", "F. Scott Fitzgerald", "Ficțiune"),
        ("Vântul prin salcii", "Kenneth Grahame", "Ficțiune"),
        ("Zori de zi", "Khaled Hosseini", "Ficțiune"),
        ("Lumea după noi", "Amitav Ghosh", "Ficțiune"),
        ("Palatul de gheață", "Tarjei Vesaas", "Ficțiune"),
        ("Leul și ursul", "William Peter Blatty", "Horror"),
        ("Iubire", "Elif Shafak", "Ficțiune"),
        ("Cum să învingi orice boală", "Deepak Chopra", "Self-help"),
        ("Călătoria în timp", "Stephen Hawking", "Știință"),
        ("Fericirea în 6 luni", "Robert Kiyosaki", "Self-help"),
        ("Timpul îți aparține", "Brian Tracy", "Self-help"),
        ("Roata timpului: Ochiul lumii", "Robert Jordan", "Fantasy"),
        ("Pelerinul", "John Bunyan", "Ficțiune"),
        ("Culoarea magică", "Terry Pratchett", "Fantasy"),
        ("Casa spiritelor", "Isabel Allende", "Ficțiune"),
        ("Umbra vântului", "Carlos Ruiz Zafón", "Ficțiune"),
        ("Numele trandafirului", "Umberto Eco", "Ficțiune"),
        ("Alchimistul", "Paulo Coelho", "Ficțiune"),
        ("Zbor deasupra unui cuib de cuci", "Ken Kesey", "Ficțiune"),
        ("Omul în căutarea sensului vieții", "Viktor Frankl", "Non-ficțiune"),
        ("1984", "George Orwell", "Science Fiction"),
        ("Ferma animalelor", "George Orwell", "Ficțiune"),
        ("Steaua Sudului", "Jules Verne", "Science Fiction"),
        ("Fata cu cercel de perlă", "Tracy Chevalier", "Ficțiune")
]
         # Adăugarea genurilor literare (fără duplicare)
    genuri = list(set(book[2] for book in books))
    for gen in genuri:
        cursor.execute('INSERT OR IGNORE INTO genuri (nume) VALUES (?)', (gen,))
    conn.commit()

    # Preluare ID-uri pentru genuri
    cursor.execute('SELECT id, nume FROM genuri')
    genuri_map = {row[1]: row[0] for row in cursor.fetchall()}

    # Inserarea cărților
    for titlu, autor, gen in books:
        cursor.execute('INSERT INTO carti (titlu, autor, gen_id) VALUES (?, ?, ?)', (titlu, autor, genuri_map[gen]))

    conn.commit()
    conn.close()
    print(f"{len(books)} cărți au fost adăugate în baza de date.")

if __name__ == "__main__":
    populate_books()
