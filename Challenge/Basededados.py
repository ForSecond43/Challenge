import gspread
import hashlib

def database(dados):
    gc = gspread.service_account(filename="Credenciais.json")
    sh = gc.open_by_key('1Wrsej1yftA9Prh0Mm7sztV2xwK_15Qqjaxjay1Wrbws')
    worksheet = sh.sheet1
    idssheet = worksheet.col_values(1)
    dados['id'] = len(idssheet)+1
    password_hash = hashlib.md5( dados['password'].encode() ).hexdigest()
    data = [dados['id'], dados['email'], password_hash]
    worksheet.append_row(data)

def comparar(email,pwd):
    gc = gspread.service_account(filename="Credenciais.json")
    sh = gc.open_by_key('1Wrsej1yftA9Prh0Mm7sztV2xwK_15Qqjaxjay1Wrbws')
    worksheet = sh.sheet1
    emailsheet = worksheet.col_values(2)

    for index , emails in enumerate(emailsheet):
        if email == emails:
            Line = index + 1
            print(Line)
            account_test = True
            break
        else:
            account_test = False
            continue

    if account_test == False:
        account_test = True
        return False       

    values = worksheet.row_values(Line)
    print(values)
    password_hash_login = hashlib.md5( pwd.encode() ).hexdigest()
    if password_hash_login == values[2]:
        return True
    else:
        return False

def check_mail_exist(email):
    gc = gspread.service_account(filename="Credenciais.json")
    sh = gc.open_by_key('1Wrsej1yftA9Prh0Mm7sztV2xwK_15Qqjaxjay1Wrbws')
    worksheet = sh.sheet1
    emailsheet = worksheet.col_values(2)

    if email in emailsheet:
        return True
    else:
        return False