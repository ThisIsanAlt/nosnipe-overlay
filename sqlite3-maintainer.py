import sqlite3

conn = sqlite3.connect('database.db')
c = conn.cursor()

#c.execute('CREATE TABLE INFO(APIKey, CriticalWins, WarningWins, CriticalNWLVL, WarningNWLVL)')
c.execute('UPDATE INFO SET APIKey = "5784c506-52f8-44c3-a724-af25cdb61a3f"')
print(c.execute('SELECT * FROM INFO').fetchall())
conn.commit()
