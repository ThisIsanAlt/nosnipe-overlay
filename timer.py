import sqlite3, time

def get_api_key():
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        data = c.execute('SELECT APIKey FROM INFO')
        data = data.fetchone()
        conn.close()
        try:
            return data[0]
        except:
            return

start = time.perf_counter()
print(get_api_key())
end = time.perf_counter()
print(end-start)