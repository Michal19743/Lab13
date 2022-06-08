from flask import Flask, Response, redirect, url_for, request, session, abort, render_template
from flask_login import LoginManager, UserMixin,login_required, login_user, logout_user
import sqlite3 as sql

app = Flask(__name__)

app.config.update(
 DEBUG = False,
 SECRET_KEY = 'sekretny_klucz'
)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

class User(UserMixin):
    def __init__(self, id):
        self.id = id
        self.name = "user" + str(id)
        self.password = self.name + "_secret"

    def __repr__(self):
        return "%d/%s/%s" % (self.id, self.name, self.password)
#login: user1 Password: user1_secret
#generacja uzytkownikow
users = [User(id) for id in range(1, 10)]

@app.route("/login", methods=["GET", "POST"])
def login():
    dane = {'tytul': 'Zalgouj się', 'tresc': 'Wpisz swoje dane logowania.'}
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if password == username + "_secret":
            id = username.split('user')[1]
            user = User(id)
            login_user(user)
            return redirect(url_for("main"))
        else:
            return abort(401)
    else:
        return render_template('login.html', tytul = dane['tytul'], tresc = dane['tresc'])
    
@app.errorhandler(401)
def page_not_found(e):
    dane = {'tytul': 'Coś poszło nie tak...', 'blad': '401'}
    return render_template('blad.html', tytul = dane['tytul'], blad = dane['blad'])

@app.route("/logout")
@login_required
def logout():
    logout_user()
    dane = {'tytul': 'Wylogowanie'}
    return render_template('logout.html', tytul = dane['tytul'])

@login_manager.user_loader
def load_user(userid):
    return User(userid)


@app.route("/")
@login_required
def main():
     dane = {'tytul': 'Strona główna', 'tresc': 'To jest strona główna.'}
     return render_template('index.html', tytul = dane['tytul'], tresc = dane['tresc'])

@app.route("/dodaj")
@login_required
def dodaj():
    dane = {'tytul': 'Dodaj pracownika', 'tresc': 'Dodawanie pracownika.'}
    return render_template('dodaj.html', tytul = dane['tytul'], tresc = dane['tresc'])

@app.route('/addrec',methods = ['POST', 'GET'])
def addrec():
    if request.method == 'POST':
        try:
            imie_nazwisko = request.form['imie_nazwisko']
            nr_pracownika = request.form['nr_pracownika']
            adres = request.form['adres']
            with sql.connect("database.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO pracownicy (imie_nazwisko, nr_pracownika, adres) VALUES (?, ?, ?)", (imie_nazwisko, nr_pracownika, adres))
                con.commit()
                msg = "Rekord zapisany pomyślnie!"
        except:
            con.rollback()
            msg = "Wystąpił problem przy zapisywaniu rekordu :("
        finally:
            return render_template("rezultat.html", tytul = "Rezultat", tresc = msg)
            con.close()

@app.route("/lista")
@login_required
def lista():
    dane = {'tytul': 'Lista pracownikow', 'tresc': ' To jest Lista pracowników'}
    con = sql.connect('database.db')
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM pracownicy")
    rekordy = cur.fetchall()
    con.close()
    return render_template('lista.html', tytul = dane['tytul'], tresc = dane['tresc'], rekordy = rekordy)

if __name__ == "__main__":
    app.run()