import sqlite3

# Verander dit pad naar jouw eigen databasebestand
DATABASE_PATH = 'instance/database.db'  # of waar jouw .db staat

def clear_reservaties():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    # Verwijder alles uit de reserveringen-tabel
    cursor.execute("DELETE FROM reserveringen")
    conn.commit()

    print("✅ Alle reservaties zijn verwijderd.")
    conn.close()

if __name__ == '__main__':
    clear_reservaties()
