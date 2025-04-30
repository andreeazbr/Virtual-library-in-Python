import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
import sqlite3
import csv

class InterfataBiblioteca:
    def __init__(self, biblioteca, admin=False):
        self.biblioteca = biblioteca
        self.admin = admin
        self.root = tk.Tk()
        self.root.title("Biblioteca Virtuală")
        self.root.geometry("1200x750")

        # 📌 Schimbare culoare fundal
        self.root.configure(bg="#dcc2fc")  # Fundal violet

        # Crearea meniului
        self.meniu = tk.Menu(self.root)
        self.root.config(menu=self.meniu)

        # Meniul principal
        self.file_menu = tk.Menu(self.meniu, tearoff=0)
        if not self.admin:
            self.file_menu.add_command(label="Împrumută Carte", command=self.imprumuta_carte)
            self.file_menu.add_command(label="Returnează Carte", command=self.returneaza_carte)
        if self.admin:
            self.file_menu.add_command(label="Adaugă Utilizator", command=self.adauga_utilizator)
            self.file_menu.add_command(label="Listare Utilizatori", command=self.lista_utilizatori)
        self.file_menu.add_command(label="Exportă Cărți", command=self.exporta_carti)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Ieșire", command=self.root.quit)
        self.meniu.add_cascade(label="Meniu", menu=self.file_menu)

        # Frame pentru căutare
        self.frame_cautare = ttk.LabelFrame(self.root, text="Căutare Carte")
        self.frame_cautare.pack(fill="x", padx=10, pady=10)

        self.entry_cautare = ttk.Entry(self.frame_cautare, width=50)
        self.entry_cautare.pack(side="left", padx=10, pady=5)

        self.btn_cautare = ttk.Button(self.frame_cautare, text="Caută", command=self.cauta_carte)
        self.btn_cautare.pack(side="left", padx=5)

        self.btn_resetare = ttk.Button(self.frame_cautare, text="Resetare Căutare", command=self.resetare_cautare)
        self.btn_resetare.pack(side="left", padx=5)

        # Frame pentru cărți
        self.frame_carti = ttk.LabelFrame(self.root, text="Cărți Disponibile")
        self.frame_carti.pack(fill="both", expand=True, padx=10, pady=10)

        # Tabel pentru cărți
        self.tree_carti = ttk.Treeview(self.frame_carti, columns=("ID", "Titlu", "Autor", "Gen", "Disponibil"),
                                       show="headings", selectmode="browse")
        self.tree_carti.heading("ID", text="ID")
        self.tree_carti.heading("Titlu", text="Titlu")
        self.tree_carti.heading("Autor", text="Autor")
        self.tree_carti.heading("Gen", text="Gen Literar")
        self.tree_carti.heading("Disponibil", text="Disponibil")
        self.tree_carti.column("ID", width=50)
        self.tree_carti.column("Titlu", width=250)
        self.tree_carti.column("Autor", width=150)
        self.tree_carti.column("Gen", width=150)
        self.tree_carti.column("Disponibil", width=100)
        self.tree_carti.pack(fill="both", expand=True)

        # Legare evenimente pentru sortare pe coloane
        for col in ("ID", "Titlu", "Autor", "Gen", "Disponibil"):
            self.tree_carti.heading(col, text=col, command=lambda c=col: self.sorteaza_tabel(c))

        # Legare eveniment pentru selectarea unei cărți
        self.tree_carti.bind("<<TreeviewSelect>>", self.afiseaza_detalii_carte)

        # Frame pentru detalii
        self.frame_detalii = ttk.LabelFrame(self.root, text="Detalii Carte")
        self.frame_detalii.pack(fill="x", padx=10, pady=10)

        self.label_detalii = ttk.Label(self.frame_detalii, text="Selectați o carte pentru a vedea detaliile.")
        self.label_detalii.pack(padx=10, pady=10)

        self.actualizeaza_tabel_carti()

    def actualizeaza_tabel_carti(self):
        for row in self.tree_carti.get_children():
            self.tree_carti.delete(row)

        for id_carte, titlu, autor, gen, disponibil in self.biblioteca.get_carti():
            disponibil_text = "Da" if disponibil else "Împrumutată de mine"
            self.tree_carti.insert("", "end", values=(id_carte, titlu, autor, gen, disponibil_text))

    def afiseaza_detalii_carte(self, event):
        selected_item = self.tree_carti.selection()
        if selected_item:
            values = self.tree_carti.item(selected_item, "values")
            id_carte, titlu, autor, gen, disponibil = values
            self.label_detalii.config(
                text=f"ID: {id_carte}\nTitlu: {titlu}\nAutor: {autor}\nGen: {gen}\nDisponibil: {disponibil}"
            )

    def adauga_carte(self):
        titlu = simpledialog.askstring("Titlu carte", "Introdu titlul cărții:")
        autor = simpledialog.askstring("Autor carte", "Introdu autorul cărții:")
        gen = simpledialog.askstring("Gen carte", "Introdu genul literar:")

        if titlu and autor and gen:
            self.biblioteca.adauga_carte(titlu, autor, gen)
            self.actualizeaza_tabel_carti()
            messagebox.showinfo("Succes", "Cartea a fost adăugată cu succes!")
        else:
            messagebox.showerror("Eroare", "Toate câmpurile sunt obligatorii!")

    def imprumuta_carte(self):
        selected_item = self.tree_carti.selection()
        if selected_item:
            values = self.tree_carti.item(selected_item, "values")
            id_carte = values[0]
            disponibil = values[4]

            if disponibil == "Împrumutată de mine":
                messagebox.showerror("Eroare", "Cartea este deja împrumutată.")
            else:
                confirm = messagebox.askyesno("Confirmare", "Ești sigur că vrei să împrumuți această carte?")
                if confirm:
                    try:
                        # Actualizare disponibilitate în baza de date
                        conn = sqlite3.connect(self.biblioteca.db_name)
                        cursor = conn.cursor()
                        cursor.execute("UPDATE carti SET disponibil = 0 WHERE id = ?", (id_carte,))
                        conn.commit()
                        conn.close()

                        # Actualizare rând în Treeview
                        self.tree_carti.item(selected_item,
                                             values=(values[0], values[1], values[2], values[3], "Împrumutată de mine"))

                        messagebox.showinfo("Succes", "Cartea a fost împrumutată cu succes.")
                    except sqlite3.Error as e:
                        messagebox.showerror("Eroare", f"A apărut o eroare: {e}")
        else:
            messagebox.showerror("Eroare", "Selectați o carte pentru a împrumuta.")

    def returneaza_carte(self):
        selected_item = self.tree_carti.selection()
        if selected_item:
            values = self.tree_carti.item(selected_item, "values")
            id_carte = values[0]
            disponibil = values[4]

            if disponibil == "Da":
                messagebox.showerror("Eroare", "Cartea nu este împrumutată.")
            else:
                confirm = messagebox.askyesno("Confirmare", "Ești sigur că vrei să returnezi această carte?")
                if confirm:
                    try:
                        # Actualizare disponibilitate în baza de date
                        conn = sqlite3.connect(self.biblioteca.db_name)
                        cursor = conn.cursor()
                        cursor.execute("UPDATE carti SET disponibil = 1 WHERE id = ?", (id_carte,))
                        conn.commit()
                        conn.close()

                        # Actualizare rând în Treeview
                        self.tree_carti.item(selected_item, values=(values[0], values[1], values[2], values[3], "Da"))

                        messagebox.showinfo("Succes", "Cartea a fost returnată cu succes.")
                    except sqlite3.Error as e:
                        messagebox.showerror("Eroare", f"A apărut o eroare: {e}")
        else:
            messagebox.showerror("Eroare", "Selectați o carte pentru a returna.")

    def adauga_utilizator(self):
        def salveaza_utilizator():
            username = entry_username.get().strip()
            parola = entry_parola.get().strip()
            tip_utilizator = combobox_tip_utilizator.get().strip()
            nume_complet = entry_nume.get().strip()
            email = entry_email.get().strip()
            telefon = entry_telefon.get().strip()

            # Validăm câmpurile obligatorii
            if not username:
                messagebox.showerror("Eroare", "Numele utilizatorului este obligatoriu!")
                return
            if not parola:
                messagebox.showerror("Eroare", "Parola este obligatorie!")
                return
            if not tip_utilizator:
                messagebox.showerror("Eroare", "Tipul utilizatorului este obligatoriu!")
                return

            # Conectare la baza de date și salvare utilizator
            conn = sqlite3.connect(self.biblioteca.db_name)
            cursor = conn.cursor()
            try:
                cursor.execute('''
                INSERT INTO utilizatori (username, parola, tip_utilizator, nume_complet, email, telefon)
                VALUES (?, ?, ?, ?, ?, ?)''', (username, parola, tip_utilizator, nume_complet, email, telefon))
                conn.commit()
                messagebox.showinfo("Succes", "Utilizatorul a fost salvat cu succes!")
                fereastra.destroy()
            except sqlite3.IntegrityError as e:
                messagebox.showerror("Eroare", f"Eroare la salvarea utilizatorului: {e}")
            finally:
                conn.close()

        # Crearea ferestrei pentru introducerea datelor utilizatorului
        fereastra = tk.Toplevel(self.root)
        fereastra.title("Adaugă Utilizator")
        fereastra.geometry("400x500")

        tk.Label(fereastra, text="Nume Utilizator:").pack(pady=5)
        entry_username = ttk.Entry(fereastra)
        entry_username.pack()

        tk.Label(fereastra, text="Parola:").pack(pady=5)
        entry_parola = ttk.Entry(fereastra, show="*")  # Câmp pentru parolă (ascunde caracterele)
        entry_parola.pack()

        tk.Label(fereastra, text="Tip Utilizator:").pack(pady=5)
        combobox_tip_utilizator = ttk.Combobox(fereastra, values=["admin", "cititor"], state="readonly")
        combobox_tip_utilizator.set("cititor")  # Valoare implicită
        combobox_tip_utilizator.pack()

        tk.Label(fereastra, text="Nume Complet:").pack(pady=5)
        entry_nume = ttk.Entry(fereastra)
        entry_nume.pack()

        tk.Label(fereastra, text="Email:").pack(pady=5)
        entry_email = ttk.Entry(fereastra)
        entry_email.pack()

        tk.Label(fereastra, text="Telefon:").pack(pady=5)
        entry_telefon = ttk.Entry(fereastra)
        entry_telefon.pack()

        ttk.Button(fereastra, text="Salvează Utilizator", command=salveaza_utilizator).pack(pady=20)

    def lista_utilizatori(self):
        fereastra = tk.Toplevel(self.root)
        fereastra.title("Listă Utilizatori")
        fereastra.geometry("600x400")

        tree_utilizatori = ttk.Treeview(fereastra, columns=("ID", "Nume Utilizator", "Nume Complet", "Email", "Telefon"), show="headings")
        tree_utilizatori.heading("ID", text="ID")
        tree_utilizatori.heading("Nume Utilizator", text="Nume Utilizator")
        tree_utilizatori.heading("Nume Complet", text="Nume Complet")
        tree_utilizatori.heading("Email", text="Email")
        tree_utilizatori.heading("Telefon", text="Telefon")

        tree_utilizatori.pack(fill="both", expand=True)

        conn = sqlite3.connect(self.biblioteca.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, nume_complet, email, telefon FROM utilizatori")
        for row in cursor.fetchall():
            tree_utilizatori.insert("", "end", values=row)

        conn.close()

    def exporta_carti(self):
        fisier_export = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Fișiere text", "*.txt")])
        if fisier_export:
            try:
                conn = sqlite3.connect(self.biblioteca.db_name)
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM carti")
                carti = cursor.fetchall()
                conn.close()

                with open(fisier_export, "w", encoding="utf-8") as f:  # Specificăm explicit codificarea UTF-8
                    for carte in carti:
                        linie = f"ID: {carte[0]}, Titlu: {carte[1]}, Autor: {carte[2]}, An: {carte[3]}, Disponibil: {'Da' if carte[4] == 1 else 'Nu'}\n"
                        f.write(linie)

                messagebox.showinfo("Succes", f"Fișierul a fost exportat cu succes la {fisier_export}")
            except Exception as e:
                messagebox.showerror("Eroare", f"A apărut o eroare: {e}")

    def sorteaza_tabel(self, col):
        data = [(self.tree_carti.set(k, col), k) for k in self.tree_carti.get_children("")]
        data.sort(reverse=False)

        for index, (val, k) in enumerate(data):
            self.tree_carti.move(k, '', index)

    def cauta_carte(self):
        query = self.entry_cautare.get().lower()
        for row in self.tree_carti.get_children():
            self.tree_carti.delete(row)

        for id_carte, titlu, autor, gen, disponibil in self.biblioteca.get_carti():
            if query in titlu.lower() or query in autor.lower() or query in gen.lower():
                disponibil_text = "Da" if disponibil else "Împrumutată de mine"
                self.tree_carti.insert("", "end", values=(id_carte, titlu, autor, gen, disponibil_text))

    def resetare_cautare(self):
        self.entry_cautare.delete(0, tk.END)
        self.actualizeaza_tabel_carti()

    def ruleaza_interfata(self):
        self.root.mainloop()
