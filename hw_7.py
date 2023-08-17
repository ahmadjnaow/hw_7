import sqlite3

class Book:
    def __init__(self, title, author, year):
        self.title = title
        self.author = author
        self.year = year
    
    def display_info(self):
        print(f"Книга: {self.title}, Автор: {self.author}, Год: {self.year}")

conn = sqlite3.connect('books_database.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Books (
        id INTEGER PRIMARY KEY,
        title TEXT,
        author TEXT,
        year INTEGER
    )
''')
conn.commit()


books_data = [
    ("Война и мир", "Лев Толстой", 1869),
    ("1984", "Джордж Оруэлл", 1949),
    ("Гарри Поттер и философский камень", "Джоан Роулинг", 1997),
    ("Преступление и наказание", "Фёдор Достоевский", 1866),
    ("Властелин колец: Братство кольца", "Дж.Р.Р. Толкин", 1954)
]

for book in books_data:
    cursor.execute('''
        INSERT INTO Books (title, author, year)
        VALUES (?, ?, ?)
    ''', book)
conn.commit()

class BookManager:
    def __init__(self, db_connection):
        self.conn = db_connection
    
    def get_all_books(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM Books')
        return cursor.fetchall()
    
    def add_book(self, title, author, year):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO Books (title, author, year)
            VALUES (?, ?, ?)
        ''', (title, author, year))
        self.conn.commit()
    
    def update_book(self, book_id, author=None, year=None):
        cursor = self.conn.cursor()
        update_query = 'UPDATE Books SET'
        update_data = []
        if author:
            update_query += ' author=?,'
            update_data.append(author)
        if year:
            update_query += ' year=?,'
            update_data.append(year)
        update_query = update_query.rstrip(',') + ' WHERE id=?'
        update_data.append(book_id)
        
        cursor.execute(update_query, tuple(update_data))
        self.conn.commit()
    
    def delete_book(self, title):
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM Books WHERE title=?', (title,))
        self.conn.commit()


book_manager = BookManager(conn)

print("Список книг:")
for book_row in book_manager.get_all_books():
    book = Book(*book_row[1:])
    book.display_info()

book_manager.add_book("Мастер и Маргарита", "Михаил Булгаков", 1967)

book_manager.update_book(2, author="Джордж Оруэлл", year=1984)

book_manager.delete_book("Преступление и наказание")

conn.close()
