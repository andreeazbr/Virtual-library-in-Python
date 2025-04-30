# Virtual Library Management System

A desktop application for managing a virtual library, developed using Python's Tkinter for the graphical interface and SQLite for data storage. The system supports user roles (admin and reader), book borrowing and returning, user management, and exporting book data.

## Features

- 📚 **Book Management**
  - Add new books with title, author, and genre.
  - View a searchable, sortable list of books.
  - Export books to a CSV file with UTF-8 encoding (with Romanian diacritics).

- 👥 **User Management** (Admin only)
  - Add new users (admin or reader).
  - View a list of registered users.

- 🔄 **Borrowing System**
  - Borrow available books (status updates instantly in the interface).
  - Return borrowed books.
  - Book availability is tracked in real time.

- 🔍 **Search and Filtering**
  - Search books by title, author, or genre.
  - Reset filters to show all available books.

## Technologies Used

- **Python 3**
- **Tkinter** for the GUI
- **SQLite3** for local data storage
- **CSV module** for exporting data

## Getting Started

### Prerequisites

Ensure you have Python 3 installed. You can download it from: https://www.python.org/downloads/

### Running the Application

1. Clone the repository or download the source code.
2. Make sure the SQLite database exists and is initialized with the required tables (`carti`, `utilizatori`).
3. Run the main script:

```bash
python main.py
```

> Replace `main.py` with your actual entry-point file if named differently.

### Example Database Schema

You should have a SQLite database with at least the following tables:

```sql
CREATE TABLE carti (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titlu TEXT NOT NULL,
    autor TEXT NOT NULL,
    gen TEXT NOT NULL,
    disponibil INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE utilizatori (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    parola TEXT NOT NULL,
    tip_utilizator TEXT NOT NULL, -- 'admin' or 'cititor'
    nume_complet TEXT,
    email TEXT,
    telefon TEXT
);
```

## Notes

- UTF-8 encoding is used when exporting to ensure Romanian characters (ă, î, ș, ț, â) are preserved.
- Only users with admin privileges can add new users.
- Borrowing status is updated immediately in the interface upon action.

## License

This project is open-source and available under the MIT License.
