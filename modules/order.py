import mysql.connector as mysql
import os
from dotenv import load_dotenv
from flask import request


load_dotenv()
db = mysql.connect(host=os.getenv("DB_HOST"),user=os.getenv("DB_USER"), database=os.getenv("DB_NAME"), password=os.getenv("DB_PASSWORD"))
cursor = db.cursor(dictionary=True)

def get_items():
    selected_items = []
    cursor.execute('select NomeAlimento, PrezzoVendita from os_alimento')
    fetched_items = cursor.fetchall()
    for item in fetched_items: # Prendo tutti i piatti selezionati dall'operatore, per fare ciò vado in cerca del tag NAME confrontandolo con tutti gli alimenti nel db
        if request.form.get(item["NomeAlimento"]) != None and request.form.get(item["NomeAlimento"]) != "" and request.form.get(item["NomeAlimento"]) != "0":
            qta =  int(request.form.get(item["NomeAlimento"]))
            selected_items.append({"NomeAlimento": item["NomeAlimento"], "Quantita": qta, "PrezzoComplessivo": item["PrezzoVendita"] * qta})
    return(selected_items)

def verify_availability(selected_items):
    available = True
    missing = []
    for item in selected_items: # Verifico se la quantità degli ingredienti rimanenti dopo aver fatto il piatto è >= 0
        cursor.execute("""
            select NomeIngrediente, os_ingrediente.Qta - os_composizione.Qta * """ + str(item["Quantita"]) + """ as rimanente
            from (os_alimento inner join os_composizione on os_alimento.IDAlimento = os_composizione.IDAlimento) inner join os_ingrediente on os_composizione.IDIngrediente = os_ingrediente.IDIngrediente
            where os_alimento.NomeAlimento = '""" + item["NomeAlimento"] + """'
        """)
        leftovers = cursor.fetchall()
        for leftover in leftovers:
            if leftover["rimanente"] < 0:
                missing.append({"NomeAlimento": item["NomeAlimento"], "NomeIngrediente": leftover["NomeIngrediente"], "Quantita": abs(leftover["rimanente"])})
                available = False
    return available, missing
        

def execute_order(selected_items):
    for item in selected_items:
        cursor.execute("""
            select NomeIngrediente, os_composizione.Qta * """ + str(item["Quantita"]) + """ as necessari
            from (os_alimento inner join os_composizione on os_alimento.IDAlimento = os_composizione.IDAlimento) inner join os_ingrediente on os_composizione.IDIngrediente = os_ingrediente.IDIngrediente
            where os_alimento.NomeAlimento = '""" + item["NomeAlimento"] + """'
        """)
        necessary_ingredients = cursor.fetchall()
        
        for necessary_ingredient in necessary_ingredients:
            cursor.execute("""
                update os_ingrediente set Qta = Qta - """ + str(necessary_ingredient["necessari"]) + """
                where NomeIngrediente = '""" + necessary_ingredient["NomeIngrediente"] + """'
            """)
            db.commit()

def get_last_order():
    cursor.execute("""select max(NOrdine) from os_ordine""")
    last_order = cursor.fetchone()
    if last_order["max(NOrdine)"] == None:
        NOrdine = 1
    else:
        NOrdine = last_order["max(NOrdine)"] + 1
    return NOrdine
    
def register_order(username, selected_items):
    NOrdine = get_last_order()
    
    for item in selected_items:
        cursor.execute("""select IDAlimento from os_alimento where NomeAlimento = '""" + item["NomeAlimento"] + """'""")
        IDAlimento = cursor.fetchone()
        cursor.execute("""
            insert into os_ordine (IDOperatore, IDAlimento, NOrdine, Qta)
            values ('""" + username + """', '""" + IDAlimento["IDAlimento"] + """', """ + str(NOrdine) + """, """ + str(item["Quantita"]) + """)
        """)
        db.commit()

def get_summary():
    summary = []
    cursor.execute("""
        select NOrdine from os_ordine
        group by NOrdine
    """)
    fetched_orders = cursor.fetchall()
    if cursor.rowcount == 0:
        return None

    for order in fetched_orders:

        cursor.execute("""
                    select NomeAlimento, Qta
                    from os_ordine inner join os_alimento on os_ordine.IDAlimento = os_alimento.IDAlimento
                    where NOrdine = """ + str(order["NOrdine"]) + """
                """)
        fetched_items = cursor.fetchall()

        for item in fetched_items:
            totale = cursor.execute("""
                select NOrdine, NomeAlimento, Qta, sum(PrezzoComplessivo) as totale
                from (
                    select NOrdine, NomeAlimento, Qta, PrezzoVendita * Qta as PrezzoComplessivo 
                    from os_ordine inner join os_alimento on os_ordine.IDAlimento = os_alimento.IDAlimento
                    order by NOrdine) as summary
                where NOrdine = """ + str(order["NOrdine"]) + """
            """)
            totale = cursor.fetchone()
            
            summary.append({"NumeroOrdine": order["NOrdine"], "NomeAlimento": item["NomeAlimento"], "Quantita": item["Qta"], "Totale": totale["totale"]})
    return(summary)

    

        

            
                
        
    