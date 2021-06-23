import sqlite3

conn = sqlite3.connect('database.db')
c = conn.cursor()

#c.execute('CREATE TABLE INFO(APIKey, CriticalWins, WarningWins, CriticalNWLVL, WarningNWLVL)')
c.execute('UPDATE INFO SET APIKey = "14ceed52-6d03-4d9a-91a4-8b063b3f07e7"')
print(c.execute('SELECT * FROM INFO').fetchall())
conn.commit()
