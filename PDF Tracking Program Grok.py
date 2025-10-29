# PDF Tracking Program Grok

# To create a Python program for managing a database of PDFs, I'll provide a solution using SQLite to store PDF metadata and binary data,
# along with PyMuPDF (fitz) for extracting text from PDFs. This program will allow you to store PDFs, extract their text, and perform basic searches. 
# Below is a comprehensive example.
# Prerequisites
# Install required libraries:
# bash
# pip install pymupdf sqlite3
# Python Program
# This program creates an SQLite database to store PDF files as BLOBs, extracts text from each PDF, and allows searching by metadata or extracted text.


import sqlite3
import fitz  # PyMuPDF
import pathlib
import os

# Initialize SQLite database
def init_db():
    conn = sqlite3.connect('pdf_database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pdfs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            data BLOB NOT NULL,
            extracted_text TEXT
        )
    ''')
    conn.commit()
    return conn, cursor

# Store PDF in database
def store_pdf(cursor, conn, pdf_path):
    try:
        # Read PDF file as binary
        pdf_path = pathlib.Path(pdf_path)
        pdf_data = pdf_path.read_bytes()

        # Extract text from PDF
        extracted_text = extract_text_from_pdf(pdf_path)

        # Insert into database
        cursor.execute('INSERT INTO pdfs (name, data, extracted_text) VALUES (?, ?, ?)',
                       (pdf_path.name, pdf_data, extracted_text))
        conn.commit()
        print(f"Stored {pdf_path.name} in database.")
    except Exception as e:
        print(f"Error storing {pdf_path.name}: {e}")

# Extract text from PDF using PyMuPDF
def extract_text_from_pdf(pdf_path):
    try:
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text("text")
        doc.close()
        return text
    except Exception as e:
        print(f"Error extracting text from {pdf_path}: {e}")
        return ""

# Search PDFs by name or extracted text
def search_pdfs(cursor, query, search_type='name'):
    if search_type == 'name':
        cursor.execute('SELECT id, name FROM pdfs WHERE name LIKE ?', (f'%{query}%',))
    elif search_type == 'text':
        cursor.execute('SELECT id, name FROM pdfs WHERE extracted_text LIKE ?', (f'%{query}%',))
    else:
        print("Invalid search type. Use 'name' or 'text'.")
        return []
    return cursor.fetchall()

# Retrieve and save a PDF from database
def retrieve_pdf(cursor, conn, pdf_id, output_path):
    cursor.execute('SELECT name, data FROM pdfs WHERE id = ?', (pdf_id,))
    result = cursor.fetchone()
    if result:
        name, data = result
        with open(os.path.join(output_path, name), 'wb') as f:
            f.write(data)
        print(f"Retrieved {name} and saved to {output_path}")
    else:
        print(f"No PDF found with ID {pdf_id}")

# Main function to demonstrate usage
def main():
    # Initialize database
    conn, cursor = init_db()

    # Example: Store PDFs from a directory
    pdf_directory = "path/to/your/pdf/folder"  # Replace with your PDF directory
    for pdf_file in pathlib.Path(pdf_directory).glob("*.pdf"):
        store_pdf(cursor, conn, pdf_file)

    # Example: Search by name
    print("\nSearching PDFs by name containing 'example':")
    results = search_pdfs(cursor, 'example', search_type='name')
    for pdf_id, name in results:
        print(f"ID: {pdf_id}, Name: {name}")

    # Example: Search by text content
    print("\nSearching PDFs with text containing 'Python':")
    results = search_pdfs(cursor, 'Python', search_type='text')
    for pdf_id, name in results:
        print(f"ID: {pdf_id}, Name: {name}")

    # Example: Retrieve a PDF by ID
    output_directory = "path/to/output/folder"  # Replace with your output directory
    os.makedirs(output_directory, exist_ok=True)
    retrieve_pdf(cursor, conn, 1, output_directory)

    # Close database connection
    conn.close()

if __name__ == "__main__":
    main()
