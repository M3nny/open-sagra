import mysql.connector as mysql
import os
import smtplib
from hashlib import sha512
from flask import url_for
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from dotenv import load_dotenv

load_dotenv()
db = mysql.connect(host=os.getenv("DB_HOST"),user=os.getenv("DB_USER"), database=os.getenv("DB_NAME"), password=os.getenv("DB_PASSWORD"))
cursor = db.cursor(dictionary=True)

def exists_user(email):
    cursor.execute('select * from os_operatore where Email = "' + email + '"')
    user = cursor.fetchone()
    if user:
        return True
    else:
        return False

def get_token(email, expiry_time):
    cursor.execute('select IDOperatore from os_operatore where Email = "' + email + '"')
    user = cursor.fetchone()
    return Serializer(os.getenv("SECRET_KEY"), expires_in=expiry_time).dumps({"IDOperatore": user["IDOperatore"]}).decode('utf-8')

def verify_token(token):
    serial = Serializer(os.getenv("SECRET_KEY"))
    try:
        user=serial.loads(token)["IDOperatore"]
    except:
        return None
    return user

def send_email(email):
    server = smtplib.SMTP(os.getenv("EMAIL_SERVER"), 587)
    server.starttls()
    server.login(os.getenv("EMAIL_USER"), os.getenv("EMAIL_PASSWORD"))
    token = get_token(email, 300)
    msg = f""" Premi sul link per recuperare la tua password 

    {url_for('reset_password_token', token=token, _external=True)}
    
    """
    server.sendmail(os.getenv("EMAIL_USER"), email, msg)
    server.quit()

def change_password(user, password):
    cursor.execute('update os_operatore set Password = "' + str(sha512(password.encode("utf-8")).hexdigest()) + '" where IDOperatore = "' + str(user) + '"')
    db.commit()
