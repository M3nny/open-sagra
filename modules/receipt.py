import os
import datetime

WIDTH = 32
FONT_A = b"\x1b!\x00"
HEIGHT_DOUBLE = b"\x1b!\x10"
BOLD = b"\x1b!\x08"
JUSTIFY_LEFT = b"\x1ba\x00"
JUSTIFY_CENTER = b"\x1ba\x01"
RESET = FONT_A + JUSTIFY_LEFT + b"\x1bL\x00\x00"

def print_receipt(items):
    totale = 0
    alimenti = []
    date = datetime.datetime.now().strftime("%d/%m/%Y")

    header = JUSTIFY_CENTER + HEIGHT_DOUBLE + b"OpenSagra\n" + FONT_A + b"" + date.encode() + b"\n\n" + JUSTIFY_LEFT
    titles = b"Alimento" + b" "*(WIDTH - len("Alimento") - len("Prezzo")) + b"Prezzo"
    table = BOLD + titles + b"\n"

    body = RESET
    for item in items:
        alimenti.append((str(item["Quantita"]) + "x " +  item["NomeAlimento"], item["PrezzoComplessivo"]))
        totale += item["PrezzoComplessivo"]
    for name, price in alimenti:
        price = f" ${price}"

        max_name_len = WIDTH - len(price)
        if len(name) > max_name_len:
            name = name[:max_name_len - 3] + "..."

        line = name + " "*(WIDTH - len(name) - len(price)) + price
        body += line.encode() + b"\n"
    body += str(totale).encode() + b"\n"

    content = RESET + header + table + body + RESET
    open("file.txt", "wb").write(content)
    os.system("cat file.txt | lpr -P scontrini")
    os.system("rm file.txt")
