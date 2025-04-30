import tkinter as tk
from tkinter import ttk, messagebox
from biblioteca import Biblioteca
from interfata import InterfataBiblioteca
import sqlite3

def main():
    biblioteca = Biblioteca()

    # Încărcarea datelor
    try:
        biblioteca.incarca_date()
        print("Datele au fost încărcate cu succes.")
    except Exception as e:
        print(f"Eroare la încărcarea datelor: {e}")
        return

    # Fereastra de log-in
    root = tk.Tk()
    root.title("Log in")
    root.geometry("500x561")

    # Încarcă imaginea de fundal (trebuie să fie GIF sau PPM/PGM)
    bg_image = tk.PhotoImage(file="library.gif")

    # Creează un label pentru imagine și îl plasezi pe fereastră
    bg_label = tk.Label(root, image=bg_image)
    bg_label.place(relwidth=1, relheight=1)  # Se întinde pe toată fereastra

    # Adaugă un buton peste imagine
    btn_login = tk.Button(root, text="Bine ați venit!", font=("Arial", 14), bg="white", fg="black")
    btn_login.pack(pady=20)

    def autentificare_admin():
        username = entry_admin_user.get()
        password = entry_admin_pass.get()

        conn = sqlite3.connect('biblioteca.db')
        cursor = conn.cursor()

        cursor.execute(
            'SELECT tip_utilizator FROM utilizatori WHERE username = ? AND parola = ? AND tip_utilizator = "admin"',
            (username, password)
        )
        rezultat = cursor.fetchone()

        if rezultat:
            messagebox.showinfo("Succes", "Autentificare reușită ca admin!")
            root.destroy()
            interfata = InterfataBiblioteca(biblioteca, admin=True)
            interfata.ruleaza_interfata()
        else:
            messagebox.showerror("Eroare", "Nume utilizator sau parolă incorecte pentru admin.")

        conn.close()

    def autentificare_utilizator():
        username = entry_user.get()
        password = entry_pass.get()

        conn = sqlite3.connect('biblioteca.db')
        cursor = conn.cursor()

        cursor.execute(
            'SELECT tip_utilizator FROM utilizatori WHERE username = ? AND parola = ? AND tip_utilizator = "cititor"',
            (username, password)
        )
        rezultat = cursor.fetchone()

        if rezultat:
            messagebox.showinfo("Succes", "Autentificare reușită ca utilizator!")
            root.destroy()
            interfata = InterfataBiblioteca(biblioteca, admin=False)
            interfata.ruleaza_interfata()
        else:
            messagebox.showerror("Eroare", "Nume utilizator sau parolă incorecte pentru utilizator.")

        conn.close()

    # Secțiunea de log-in Admin
    ttk.Label(root, text="Log in admin", font=("Arial", 14)).pack(pady=10)

    ttk.Label(root, text="Nume utilizator:").pack(pady=5)
    entry_admin_user = ttk.Entry(root, width=30)
    entry_admin_user.pack()

    ttk.Label(root, text="Parolă:").pack(pady=5)
    entry_admin_pass = ttk.Entry(root, show="*", width=30)
    entry_admin_pass.pack()

    ttk.Button(root, text="Autentificare ca admin", command=autentificare_admin).pack(pady=10)

    # Separator
    ttk.Separator(root, orient="horizontal").pack(fill="x", pady=10)

    # Secțiunea de log-in Utilizator
    ttk.Label(root, text="Log in cititor", font=("Arial", 14)).pack(pady=10)

    ttk.Label(root, text="Nume utilizator:").pack(pady=5)
    entry_user = ttk.Entry(root, width=30)
    entry_user.pack()

    ttk.Label(root, text="Parolă:").pack(pady=5)
    entry_pass = ttk.Entry(root, show="*", width=30)
    entry_pass.pack()

    ttk.Button(root, text="Autentificare ca utilizator", command=autentificare_utilizator).pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
