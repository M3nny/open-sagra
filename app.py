import mysql.connector as mysql
import os
import datetime
from dotenv import load_dotenv
from hashlib import sha512
from modules import order, management, recover, receipt
from flask import Flask, session, render_template, request, redirect, url_for

load_dotenv()
db = mysql.connect(host=os.getenv("DB_HOST"),user=os.getenv("DB_USER"), database=os.getenv("DB_NAME"), password=os.getenv("DB_PASSWORD"))
cursor = db.cursor(dictionary=True)

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.debug = True

date = datetime.datetime.now().strftime("%d/%m/%Y")
day = datetime.datetime.now().strftime("%A")
time = datetime.datetime.now().strftime("%H:%M")

def refresh():
    db = mysql.connect(host=os.getenv("DB_HOST"),user=os.getenv("DB_USER"), database=os.getenv("DB_NAME"), password=os.getenv("DB_PASSWORD"))
    cursor = db.cursor(dictionary=True)
    return db, cursor

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html")
    if request.method == "POST":
        return redirect(url_for('login'))
    
@app.route('/login', methods=["GET", "POST"])
def login():
    db, cursor = refresh()
    if request.method == "POST":
        session.permanent = True
        username = request.form.get("username")
        password = str(sha512(request.form.get("password").encode("utf-8")).hexdigest())
        cursor.execute('select * from os_operatore where IDOperatore = "' + username + '" and Password = "' + password + '"')
        account = cursor.fetchone()
        if cursor.rowcount == 1:
            if account["Ruolo"] == "cassa":
                session['username'] = username
                session['Ruolo'] = account["Ruolo"]
                return redirect(url_for('cassa'))
            elif account["Ruolo"] == "bar":
                session['username'] = username
                session['Ruolo'] = account["Ruolo"]
                return redirect(url_for('bar'))
            elif account["Ruolo"] == "admin":
                session['username'] = username
                session['Ruolo'] = account["Ruolo"]
                return redirect(url_for('manage'))
        else:
            return render_template('login.html', error = True)

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop("username", None)
    session.pop("Ruolo", None)
    return redirect(url_for('login'))

@app.route('/cassa', methods=["GET", "POST"])
def cassa():
    if "username" in session and (session["Ruolo"] == "cassa" or session["Ruolo"] == "admin"):
        menu_piatti = []
        menu_bevande = {}
        place = "Cassa"
        if day == "Saturday" or day == "Sunday":
            festivo = "True"
        else:
            festivo = "False"

        cursor.execute('select NomeAlimento from os_alimento where (Festivo = ' + festivo + ' or Festivo is null) and Categoria = "piatto" order by NomeAlimento')
        piatti = cursor.fetchall()
        for piatto in piatti:
            menu_piatti.append(piatto["NomeAlimento"])

        cursor.execute('select NomeAlimento, Alcolico from os_alimento where (Festivo = ' + festivo + ' or Festivo is null) and Categoria = "bevanda" order by NomeAlimento')
        bevande = cursor.fetchall()
        for bevanda in bevande:
            NomeBevanda = bevanda["NomeAlimento"]
            Alcolico = bevanda["Alcolico"]
            menu_bevande[NomeBevanda] = Alcolico

        if request.method == "GET":
            return render_template('cassa.html', day=day, place=place, menu_piatti=menu_piatti, menu_bevande=menu_bevande, username=session["username"], ruolo=session["Ruolo"])

        if request.method == "POST":
            items = order.get_items()
            available, missing = order.verify_availability(items)
            if (available):
                session["items"] = items
                return redirect(url_for('confirm_order'))
            else:
                return render_template('cassa.html', day=day, place=place, menu_piatti=menu_piatti, menu_bevande=menu_bevande, username=session["username"], missing=missing, ruolo=session["Ruolo"], error=True)

    else:
        return redirect(url_for('login'))

@app.route('/bar', methods=["GET", "POST"])
def bar():
    if "username" in session and (session["Ruolo"] == "bar" or session["Ruolo"] == "admin"):
        menu_dolci = []
        menu_bevande = {}
        place = "Bar"
        if day == "Saturday" or day == "Sunday":
            festivo = "True"
        else:
            festivo = "False"

        cursor.execute('select NomeAlimento from os_alimento where (Festivo = ' + festivo + ' or Festivo is null) and Categoria = "dolce" order by NomeAlimento')
        dolci = cursor.fetchall()
        for dolce in dolci:
            menu_dolci.append(dolce["NomeAlimento"])

        cursor.execute('select NomeAlimento, Alcolico from os_alimento where (Festivo = ' + festivo + ' or Festivo is null) and Categoria = "bevanda" order by NomeAlimento')
        bevande = cursor.fetchall()
        for bevanda in bevande:
            NomeBevanda = bevanda["NomeAlimento"]
            Alcolico = bevanda["Alcolico"]
            menu_bevande[NomeBevanda] = Alcolico

        if request.method == "GET":
            return render_template('bar.html', day=day, place=place, menu_dolci=menu_dolci, menu_bevande=menu_bevande, username=session["username"], ruolo=session["Ruolo"])

        if request.method == "POST":
            items = order.get_items()
            available, missing = order.verify_availability(items)
            if (available):
                session["items"] = items
                return redirect(url_for('confirm_order'))
            else:
                return render_template('bar.html', day=day, place=place, menu_dolci=menu_dolci, menu_bevande=menu_bevande, username=session["username"], missing=missing, ruolo=session["Ruolo"], error=True)

    else:
        return redirect(url_for('login'))


@app.route('/confirm_order', methods=["GET", "POST"])
def confirm_order():
    totale = 0
    NOrdine = order.get_last_order()
    if "items" in session:
        if request.method == "GET":
            for item in session["items"]:
                totale += item["PrezzoComplessivo"]

            return render_template('confirm_order.html', items=session["items"], username=session["username"], totale=totale, time=time, date=date, NOrdine=NOrdine)
        
        if request.method == "POST":
            order.execute_order(session["items"])
            order.register_order(session["username"], session["items"])
            receipt.print_receipt(session["items"])
            if session["Ruolo"] == "cassa":
                return redirect(url_for('cassa'))
            elif session["Ruolo"] == "bar":
                return redirect(url_for('bar'))
            elif session["Ruolo"] == "admin":
                return redirect(url_for('manage'))
    else:
        if session["Ruolo"] == "cassa":
                return redirect(url_for('cassa'))
        elif session["Ruolo"] == "bar":
            return redirect(url_for('bar'))
        elif session["Ruolo"] == "admin":
            return redirect(url_for('manage'))

@app.route('/history', methods=["GET", "POST"])
def history():
    if "username" in session:
        if request.method == "GET":
            summary = order.get_summary()
            if summary == None:
                return "Ancora nessun ordine"

        return render_template('history.html', summary=summary, place="summary", day=day, ruolo=session["Ruolo"])
    else:
        return redirect(url_for('login'))

@app.route('/manage', methods=["GET", "POST"])
def manage():
    if "username" in session and session["Ruolo"] == "admin":
        if request.method == "GET":
            return render_template('manage.html', username=session["username"], day=day, ruolo=session["Ruolo"])
        if request.method == "POST":
            return render_template('manage.html', username=session["username"], day=day, ruolo=session["Ruolo"])
    else:
        return redirect(url_for('login'))


@app.route('/manage/operatori', methods=["GET", "POST"])
def manage_operatori():
    if "username" in session and session["Ruolo"] == "admin":
        if request.method == "GET":
            users = management.get_users()
            return render_template('manage_operatori.html', users=users, day=day, place="manage", back=True)

        if request.method == "POST" and "Password" not in request.form: # distinguo le richieste post in base alla presenza del campo Password
            IDOperatore = request.form.get("id")
            management.delete_user(IDOperatore)
            return redirect(url_for('manage_operatori'))
        elif request.method == "POST" and "Password" in request.form:
            IDOperatore = request.form.get("IDOperatore")
            NomeOperatore = request.form.get("NomeOperatore")
            CognomeOperatore = request.form.get("CognomeOperatore")
            Email = request.form.get("Email")
            Password = request.form.get("Password")
            Ruolo = request.form.get("Ruolo")
            management.add_user(IDOperatore, NomeOperatore, CognomeOperatore, Email, Password, Ruolo)
            return redirect(url_for('manage_operatori'))
    else:
        return redirect(url_for('login'))

@app.route('/manage/alimenti', methods=["GET", "POST"])
def manage_alimenti():
    if "username" in session and session["Ruolo"] == "admin":
        if request.method == "GET":
            alimenti = management.get_alimenti()
            ingredienti = management.get_ingredienti()
            return render_template('manage_alimenti.html', alimenti=alimenti, ingredienti=ingredienti, day=day, place="manage", back=True)
        if request.method == "POST" and "Ingredienti" not in request.form:
            management.delete_alimento(request.form.get("id"))
            return redirect(url_for('manage_alimenti'))
        elif request.method == "POST" and "Ingredienti" in request.form:
            alimento = []
            IDAlimento = request.form.get("IDAlimento")
            NomeAlimento = request.form.get("NomeAlimento")
            PrezzoVendita = request.form.get("PrezzoVendita")
            Categoria = request.form.get("Categoria")
            Festivo = request.form.get("Festivo")
            Alcolico = request.form.get("Alcolico")
            Ingredienti = request.form.getlist("Ingredienti")
            alimento.append({"IDAlimento": IDAlimento, "NomeAlimento": NomeAlimento, "PrezzoVendita": PrezzoVendita, "Categoria": Categoria, "Festivo": Festivo, "Alcolico": Alcolico, "Ingredienti": Ingredienti})
            session["alimento"] = alimento
            return redirect(url_for('manage_alimenti_quantita'))
            
    else:
        return redirect(url_for('login'))


@app.route('/manage/alimenti/quantità', methods=["GET", "POST"])
def manage_alimenti_quantita():
    if "username" in session and session["Ruolo"] == "admin":
        if request.method == "GET":
            alimento = session["alimento"]
            return render_template('manage_alimenti_quantita.html', alimento=alimento)
        if request.method == "POST":
            IDAlimento = session["alimento"][0]["IDAlimento"]
            NomeAlimento = session["alimento"][0]["NomeAlimento"]
            PrezzoVendita = session["alimento"][0]["PrezzoVendita"]
            Categoria = session["alimento"][0]["Categoria"]
            Festivo = session["alimento"][0]["Festivo"]
            Alcolico = session["alimento"][0]["Alcolico"]
            Ingredienti = session["alimento"][0]["Ingredienti"]
            Quantita = request.form.getlist("Quantita")
            management.add_alimento(IDAlimento, NomeAlimento, PrezzoVendita, Categoria, Festivo, Alcolico, Ingredienti, Quantita)
            session.pop("alimento")
            return redirect(url_for('manage_alimenti'))


@app.route('/manage/magazzino', methods=["GET", "POST"])
def manage_magazzino():
    if "username" in session and session["Ruolo"] == "admin":
        if request.method == "GET":
            ingredienti = management.get_ingredienti()
            return render_template('manage_magazzino.html', ingredienti=ingredienti, day=day, place="manage", back=True)

        if request.method == "POST" and "add" not in request.form and "update" not in request.form:
            management.delete_ingrediente(request.form.get("IDIngrediente"))
            return redirect(url_for('manage_magazzino'))

        elif request.method == "POST" and "add" in request.form and "update" not in request.form:
            IDIngrediente = request.form.get("IDIngrediente")
            NomeIngrediente = request.form.get("NomeIngrediente")
            Quantita = request.form.get("Qta")
            management.add_ingrediente(IDIngrediente, NomeIngrediente, Quantita)
            return redirect(url_for('manage_magazzino'))

        elif request.method == "POST" and "update" in request.form:
            IDIngrediente = request.form.get("IDIngrediente")
            Quantita = request.form.get("Qta_modificata")
            management.update_ingrediente(IDIngrediente, Quantita)
            return redirect(url_for('manage_magazzino'))
    else:
        return redirect(url_for('login'))

@app.route('/reset_password', methods=["GET", "POST"])
def reset_password():
    if request.method == "GET":
        return render_template('reset_password.html')
    if request.method == "POST":
        email = request.form.get("email")
        if recover.exists_user(email):
            recover.send_email(email)
            return render_template('reset_password.html', sent=True)
        else:
            return render_template('reset_password.html', error=True)

@app.route('/reset_password/<token>', methods=["GET", "POST"])
def reset_password_token(token):
    user = recover.verify_token(token)
    if user is None:
        return redirect(render_template('reset_password.html', expired=True))
    else:
        session["restore_user"] = user
        return redirect(url_for('change_password'))


@app.route('/change_password', methods=["GET", "POST"])
def change_password():
    if "restore_user" in session:
        if request.method == "GET":
            return render_template('change_password.html')
        if request.method == "POST":
            password = request.form.get("password")
            confirm_password = request.form.get("confirm_password")
            if password == confirm_password:
                recover.change_password(session["restore_user"], password)
                return render_template('reset_password.html', success=True)
            else:
                return render_template('change_password.html', error=True)
    else:
        return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)
