import sqlite3

conn = sqlite3.connect('database.db')
c = conn.cursor()

c.execute('CREATE TABLE INFO(APIKey, CriticalWins, WarningWins, CriticalNWLVL, WarningNWLVL)')
#c.execute('UPDATE INFO SET APIKey = "5a07d930-e276-462b-8eb4-f884eb365574"')
print(c.execute('SELECT * FROM INFO').fetchall())
conn.commit()
