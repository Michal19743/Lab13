
import sqlite3

if __name__ == "__main__":

    conn = sqlite3.connect('database.db')
	
    print("Otworzono Baze Danych")
    
    conn.execute('CREATE TABLE pracownicy (imie_nazwisko TEXT, nr_pracownika TEXT, adres TEXT)')
	
    print("Utworzono Tabele")
    
    conn.close()
	
    print("Zamknieto Baze Danych")
    
    
    conn = sqlite3.connect('database.db')
	
    print("Otworzono Baze Danych")
	
    cur = conn.cursor()
    
    cur.execute("INSERT INTO pracownicy (imie_nazwisko, nr_pracownika, adres) VALUES (?,?,?)",('Majkel Rakowszczak','1','Elbląg') )
    cur.execute("INSERT INTO pracownicy (imie_nazwisko, nr_pracownika, adres) VALUES (?,?,?)",('Łukasz Broda','2','Gdańsk') )
    conn.commit()
    
    cur.execute('SELECT * FROM pracownicy ORDER BY nr_pracownika')
	
    print(cur.fetchall())
    
    conn.close()
	
    print("Zamknieto Baze Danych")