import sqlite3
from datetime import datetime

# Connessione al database SQLite (crea il file se non esiste)
conn = sqlite3.connect('gestione_spese.db')
cursor = conn.cursor()

# Creazione delle tabelle se non esistono
cursor.execute('''
    CREATE TABLE IF NOT EXISTS categorie (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT UNIQUE NOT NULL
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS spese (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        data TEXT NOT NULL,
        importo REAL NOT NULL,
        categoria_id INTEGER,
        descrizione TEXT,
        FOREIGN KEY (categoria_id) REFERENCES categorie (id)
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS budget (
        mese TEXT NOT NULL,
        categoria_id INTEGER,
        importo REAL NOT NULL,
        PRIMARY KEY (mese, categoria_id),
        FOREIGN KEY (categoria_id) REFERENCES categorie (id)
    )
''')
conn.commit()

# --- Funzioni di Gestione ---
def aggiungi_categoria():
    nome = input("Nome nuova categoria: ").strip()
    if nome:
        try:
            cursor.execute("INSERT INTO categorie (nome) VALUES (?)", (nome,))
            conn.commit()
            print(f"Categoria '{nome}' inserita correttamente.")
        except sqlite3.IntegrityError:
            print("La categoria esiste già.")

def inserisci_spesa():
    print("\n--- Inserisci Spesa ---")
    data = input("Data (YYYY-MM-DD) [oggi]: ") or datetime.now().strftime('%Y-%m-%d')
    try:
        importo = float(input("Importo: "))
        if importo <= 0:
            print(" Errore. L'importo deve essere maggiore di 0.")
            return
       
        # Mostra categorie
        cursor.execute("SELECT * FROM categorie")
        cats = cursor.fetchall()
        for c in cats: print(f"{c[0]}:{c[1]}")

           
        cat_id = int(input("ID Categoria: "))
        desc = input("Descrizione: ")

             
        cursor.execute("INSERT INTO spese (data, importo, categoria_id, descrizione) VALUES (?, ?, ?, ?)",
                       (data, importo, cat_id, desc))
        conn.commit()
        print("Spesa inserita con successo.")
       
    except ValueError:
        print("Errore. Input non valido.")

def definisci_budget():
    print("\n--- Definisci Budget Mensile ---")
    mese = input("Mese (YYYY-MM) [corrente]: ") or datetime.now().strftime('%Y-%m')
   
    cursor.execute("SELECT * FROM categorie")
    cats = cursor.fetchall()
    for c in cats: print(f"{c[0]}: {c[1]}")
   
    try:
        cat_id = int(input("ID Categoria: "))
        importo = float(input("Importo Budget: "))
       
        cursor.execute("INSERT OR REPLACE INTO budget (mese, categoria_id, importo) VALUES (?, ?, ?)",
                       (mese, cat_id, importo))
        conn.commit()
        print("Budget mensile salvato correttamente.")
    except ValueError:
        print("Input non valido.")

def visualizza_report():
    print("\n--- Report Spese Mensili Vs Budget ---")
    mese = input("Mese da analizzare (YYYY-MM) [corrente]: ") or datetime.now().strftime('%Y-%m')
   
    query = '''
        SELECT c.nome, SUM(s.importo) as totale_speso, b.importo as budget_mensile
        FROM categorie c
        LEFT JOIN spese s ON c.id = s.categoria_id AND s.data LIKE ?
        LEFT JOIN budget b ON c.id = b.categoria_id AND b.mese = ?
        GROUP BY c.id
    '''
    cursor.execute(query, (f"{mese}%", mese))
    report = cursor.fetchall()
   
    print(f"\nReport {mese}:")
    print(f"{'Categoria':<15} | {'Speso':<10} | {'Budget':<10} | {'Differenza':<10}")
    print("-" * 55)
    for row in report:
        nome, speso, budget = row
        speso = speso or 0
        budget = budget or 0
        diff = budget - speso
       
        print(f"{nome:<15} | {speso:<10.2f} | {budget:<10.2f} | {diff:<10.2f}")

# --- Menu Principale

print("-"*40)
print("BENVENUTO NEL SISTEMA SPESE PERSONALI")
print("-"*40)

def menu():
    while True:
        print("\n=== MENU GESTIONE SPESE ===")
        print("1. Gestisci Categorie ")
        print("2. Inserisci Spesa ")
        print("3. Definisci Budget Mensile")
        print("4. Visualizza Report")
        print("5. Esci")
       
        scelta = input("Seleziona opzione: ")
       
        # Simulazione switch/case con if-elif
        if scelta == '1':
            aggiungi_categoria()
        elif scelta == '2':
            inserisci_spesa()
        elif scelta == '3':
            definisci_budget()
        elif scelta == '4':
            visualizza_report()
        elif scelta == '5':
            break
        else:
            print("Scelta non valida.Riprovare.")

    conn.close()

if __name__ == '__main__':
    menu() 
