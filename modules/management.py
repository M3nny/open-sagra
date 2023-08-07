import mysql.connector as mysql
import os
from dotenv import load_dotenv
from flask import redirect, url_for
from hashlib import sha512


load_dotenv()
db = mysql.connect(host=os.getenv("DB_HOST"),user=os.getenv("DB_USER"), database=os.getenv("DB_NAME"), password=os.getenv("DB_PASSWORD"))
cursor = db.cursor(dictionary=True)

def get_users():
    users = []
    cursor.execute('select IDOperatore, NomeOperatore, CognomeOperatore, Email, Ruolo from os_operatore')
    fetched_users = cursor.fetchall()
    for user in fetched_users:
        users.append({"IDOperatore": user["IDOperatore"], "NomeOperatore": user["NomeOperatore"], "CognomeOperatore": user["CognomeOperatore"], "Email": user["Email"], "Ruolo": user["Ruolo"]})
    return users

def get_alimenti():
    alimenti = []
    cursor.execute('select * from os_alimento')
    fetched_alimenti = cursor.fetchall()
    for alimento in fetched_alimenti:
        alimenti.append({"IDAlimento": alimento["IDAlimento"], "NomeAlimento": alimento["NomeAlimento"], "PrezzoVendita": alimento["PrezzoVendita"], "Categoria": alimento["Categoria"], "Festivo": alimento["Festivo"], "Alcolico": alimento["Alcolico"]})
    return alimenti

def get_ingredienti():
    ingredienti = []
    cursor.execute('select * from os_ingrediente')
    fetched_ingredienti = cursor.fetchall()
    for alimento in fetched_ingredienti:
        ingredienti.append({"IDIngrediente": alimento["IDIngrediente"], "NomeIngrediente": alimento["NomeIngrediente"], "Quantita": alimento["Qta"]})
    return ingredienti


def add_user(IDOperatore, NomeOperatore, CognomeOperatore, Email, Password, Ruolo):
    try:
        cursor.execute("""insert into os_operatore (IDOperatore, NomeOperatore, CognomeOperatore, Email, Password, Ruolo) values (
        '""" + IDOperatore + """', 
        '""" + NomeOperatore + """', 
        '""" + CognomeOperatore + """', 
        '""" + Email + """', 
        '""" + str(sha512(Password.encode("utf-8")).hexdigest()) + """', 
        '""" + Ruolo + """'
        ) """)
    except:
        return redirect(url_for('manage_operatori'))
    db.commit()


def add_alimento(IDAlimento, NomeAlimento, PrezzoVendita, Categoria, Festivo, Alcolico, Ingredienti, Quantita):
    try:
        cursor.execute("""insert into os_alimento (IDAlimento, NomeAlimento, PrezzoVendita, Categoria, Festivo, Alcolico) values (
        '""" + IDAlimento + """',
        '""" + NomeAlimento + """',
        '""" + str(PrezzoVendita) + """',
        '""" + Categoria + """',
        """ + Festivo + """,
        """ + Alcolico + """
        ) """)

        count = 0
        for ingrediente in Ingredienti:
            cursor.execute('select IDIngrediente from os_ingrediente where NomeIngrediente = "' + ingrediente + '"')
            fetched_ingrediente = cursor.fetchone()

            cursor.execute("""insert into os_composizione (IDAlimento, IDIngrediente, Qta) values (
            '""" + IDAlimento + """',
            '""" + fetched_ingrediente["IDIngrediente"] + """',
            '""" + str(Quantita[count]) + """'
            ) """)
            count += 1
    except:
        return redirect(url_for('manage_alimenti'))
    db.commit()

def add_ingrediente(IDIngrediente, NomeIngrediente, Quantita):
    try:
        cursor.execute("""insert into os_ingrediente (IDIngrediente, NomeIngrediente, Qta) values (
        '""" + IDIngrediente + """',
        '""" + NomeIngrediente + """',
        '""" + str(Quantita) + """'
        ) """)
    except:
        return redirect(url_for('manage_magazzino'))
    db.commit()

def delete_user(IDOperatore):
    cursor.execute('delete from os_operatore where IDOperatore = "' + IDOperatore + '"')
    db.commit()

def delete_alimento(IDAlimento):
    cursor.execute('delete from os_alimento where IDAlimento = "' + IDAlimento + '"')
    db.commit()

def delete_ingrediente(IDIngrediente):
    cursor.execute('delete from os_ingrediente where IDIngrediente = "' + IDIngrediente + '"')
    db.commit()

def update_ingrediente(IDIngrediente, Quantita):
    cursor.execute("""update os_ingrediente set Qta = """ + Quantita + """ where IDIngrediente = '""" + IDIngrediente + """'""")
    db.commit()