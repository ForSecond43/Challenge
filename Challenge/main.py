import PySimpleGUI as sg
from Basededados import database , comparar , check_mail_exist
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
import pickle
from datetime import datetime, timedelta

list_min=[*range(0,60,1)]
list_hour=[*range(0,24,1)]
list_freq=['Diário', 'Semanal', 'Mensal', 'Anual']
list_freq2=['DAILY', 'WEEKLY', 'MONTHLY', 'YEARLY']
list_rep=['Sempre', *range(1,13,1)]


theme = 'Reddit'

def janela_login_signup():
    sg.theme(theme)
    
    layout = [
        [sg.Text('Login', justification= 'center', font='Courier 20', size = (45,1) )],
        [sg.Text('')],
        [sg.Text('Username', size=(8,1)), sg.Input(size=(30,1), key='email_login', do_not_clear= False )],
        [sg.Text('Password',size=(8,1)), sg.Input(size=(30,1), key='pwd_login', password_char='*',do_not_clear= False )],
        [sg.Text('Se não tiver conta, carregue em "Registrar"'), sg.Button('Registrar',size=(8,1) ,border_width=0)],
        [sg.Text('')],
        [sg.Text(' '*25), sg.Button('Login',size=(9,1) , border_width=0, font = 'Courier', button_color= ('white','green'))]
    ]

    return sg.Window('Login', layout=layout, size=(400,250), finalize=True)

def janela_registro():
    sg.theme('Reddit')

    layout = [
        [sg.Text('Registo', justification= 'center',size=(45,1),font='Courier 20')],
        [sg.Text('')],
        [sg.Text('Username',size=(8,1)), sg.Input(size=(30,1), key='email_signup', do_not_clear= False)],
        [sg.Text('Password', size=(8,1)), sg.Input(size=(30,1), key='pwd_signup', password_char='*', do_not_clear= False)],
        [sg.Text('')],
        [sg.Text(' '*16),sg.Button('Voltar', size=(10,1), border_width=0) ,sg.Text(' '*2), sg.Button('Sign Up', size=(10,1), border_width=0)]
    ]

    return sg.Window('Sign Up', layout = layout, finalize=True , size=(400,250))

def to_do(username):
    sg.theme('Reddit')
    layout = [
        [sg.Text('')],
        [sg.Text('', size=(25,1)),sg.Text('Bem-Vindo', justification= 'center', font='Courier 20' ),sg.Text(f'{username}',font='Courier 15')],
        [sg.Text('')],
        [sg.Text('', size=(20,1)),sg.Text('Evento*', font='Courier 14', size=(8,1)),sg.Text(' '*2), sg.Input(key='evento', size=(35,1))],
        [sg.Text('', size=(20,1)),sg.Text('Descrição*',font='Courier 14'), sg.Input(key='descricao', size=(35,1))],
        [sg.Text('', size=(20,1)),sg.Text('Data*',font='Courier 14'), sg.Button('Data', button_color=('black','white')), 
            sg.In(key='data', enable_events=True, visible=False)],
        [sg.Text('', size=(20,1)),sg.Text('Hora*',font='Courier 14'), sg.Spin(list_hour, readonly=True, size=(3,1), key='hora'),sg.Text('h'),
            sg.Spin(list_min, readonly=True, size=(3,1), key='minuto'), sg.Text('m')],
        [sg.Text('', size=(20,1)),sg.Text('Duração*', font='Courier 14'), sg.Spin(list_hour, readonly=True, size=(3,1), key='d_hora'), sg.Text('h'), 
            sg.Spin(list_min, readonly=True, size=(3,1), key='d_minuto'), sg.Text('m')],
        [sg.Text('', size=(20,1)),sg.Text('Frequência*', font='Courier 14'), sg.Combo(list_freq, readonly=True,size=(9,1),key='frequencia'),
            sg.Text('Repetição*',font='Courier 14'), sg.Combo(list_rep, readonly=True, key='repeticao', size = (9,1))],
        [sg.Text('', size=(20,1)),sg.Text('Localização', font='Courier 14'), sg.Input(key='location', size=(20,1))],
        [sg.Text('',size=(30,1)),sg.Text('(*) Campos obrigatórios', justification='center', font='Courier 10', text_color = 'red')],
        [sg.Text('')],
        [sg.Text('',size=(25,1)), sg.Button('Adicionar Evento', font = 'Courier' , border_width = 0, size=(25,2))]
    ]

    return sg.Window('Tarefas', layout=layout, finalize=True , size=(800,450))

janela_login, janela_signup, janela_atividade = janela_login_signup(), None , None
dia=mes=ano=0

while True:
    window, eventos, valores = sg.read_all_windows()
    
    if window == janela_login and eventos == sg.WIN_CLOSED:
        break
    
    if window == janela_signup and eventos == sg.WIN_CLOSED:
        break

    if window == janela_atividade and eventos == sg.WIN_CLOSED:
        break

    if window == janela_login and eventos == 'Registrar':
        janela_signup = janela_registro()
        janela_login.hide()

    if window == janela_signup and eventos == 'Voltar':
        janela_signup.hide()
        janela_login.un_hide()

    if window == janela_signup and eventos == 'Sign Up':
        mail_check = check_mail_exist(valores['email_signup'])
        if valores['email_signup'] == '' or valores['pwd_signup'] == '' or mail_check:
            sg.popup('Tem de inserir um email ou password válida ou o email inserido já existe!')
        
        else: 
            sg.popup('Conta criada com sucesso')
            janela_signup.hide()
            janela_login.un_hide()

            dict_account = {     
                'email' : valores['email_signup'],
                'password' : valores['pwd_signup']
                }
            database(dict_account)

    if window == janela_login and eventos == 'Login':
        state = comparar(valores['email_login'], valores['pwd_login'])
        if state:
            janela_login.hide()
            janela_atividade = to_do(valores['email_login'])
        else:
            sg.popup('Email ou Password incorreto! Tente novamente :P') # popup de wrong
    
    # Calendario
    if window == janela_atividade and eventos == 'Data':
        data_em_tuple = sg.popup_get_date()
        # Data em str
        dia = ''.join(str(data_em_tuple[1]))
        mes = ''.join(str(data_em_tuple[0]))
        ano = ''.join(str(data_em_tuple[2]))
    
    # Adicionar Evento
    if window == janela_atividade and eventos == 'Adicionar Evento':
        if valores['evento']=='' or valores['hora']=='' or valores['minuto']=='' or dia == 0 or mes == 0 or ano == 0 or valores['d_hora']=='' or valores['d_minuto']=='' or valores['frequencia']=='' or valores['repeticao']=='':
            sg.popup('Caixas em branco')

        else:
            if valores['hora'] < 10:
                valores['hora'] = str(valores['hora'])
                valores['hora'] = '0'+ valores['hora']
            if valores['minuto'] < 10:
                valores['minuto'] = str(valores['minuto'])
                valores['minuto'] = '0'+ valores['minuto']
            if valores['d_hora'] < 10:
                valores['d_hora'] = str(valores['d_hora'])
                valores['d_hora'] = '0'+ valores['d_hora']
            if valores['d_minuto'] < 10:
                valores['d_minuto'] = str(valores['d_minuto'])
                valores['d_minuto'] = '0'+ valores['d_minuto']
            
            sg.popup('Evento: ' + valores['evento'],
                    'Descrição: ' + valores['descricao'], 
                    'Data: ' + dia +'/'+ mes +'/'+ ano, 
                    'Hora: ' + str(valores['hora']) +"h" + str(valores['minuto']),
                    'Duração: ' + str(valores['d_hora']) +"h" + str(valores['d_minuto']),
                    'Localização: ' + valores['location'],
                    grab_anywhere=True, title='')
            # print(valores['data'])
            
            #Frequência e repetição
            if (valores['frequencia'] == list_freq[0]):
                valores['frequencia'] = list_freq2[0]
            if (valores['frequencia'] == list_freq[1]):
                valores['frequencia'] = list_freq2[1]
            if (valores['frequencia'] == list_freq[2]):
                valores['frequencia'] = list_freq2[2]
            if (valores['frequencia'] == list_freq[3]):
                valores['frequencia'] = list_freq2[3]

            #Quando o evento acontece sempre
            if (valores['repeticao'] == list_rep[0]):
                valores['repeticao'] = '0'
            #####################################################
            credentials = pickle.load(open("token_teste.pkl","rb"))
            #print (credentials)

            service = build("calendar", "v3", credentials=credentials)

            #lista os calendarios
            calendar_list = service.calendarList().list().execute()

            #diz o id do calendario 1
            id_calendario = calendar_list ['items'][0]['id']
            # print (id_calendario)

            start_time = datetime(int(ano), int(mes), int(dia), int(valores['hora']), int(valores['minuto']), 0)
            end_time = start_time + timedelta(hours=int(valores['d_hora']), minutes=int(valores['d_minuto']))
            #print (start_time)
            #print (end_time)
            #criar evento
            event = {
            'summary': valores['evento'],
            'location': valores['location'],
            'description': valores['descricao'],
            'start': {
                'dateTime': start_time.strftime("%Y-%m-%dT%H:%M:%S"),
                'timeZone': 'Europe/Lisbon',
            },
            'end': {
                'dateTime': end_time.strftime("%Y-%m-%dT%H:%M:%S"),
                'timeZone': 'Europe/Lisbon',
            },
            'recurrence': [
                'RRULE:FREQ={};COUNT={}'.format(valores['frequencia'], valores['repeticao'])
            ],
            'reminders': {
                'useDefault': False,
                'overrides': [
                {'method': 'email', 'minutes': 24 * 60},
                {'method': 'popup', 'minutes': 10},
                ],
            },
            }

            event = service.events().insert(calendarId= id_calendario, body=event).execute()
            #####################################################

            #clear boxes
            window.FindElement('evento').update('')
            window.FindElement('descricao').update('')
            window.FindElement('data').update('')
            window.FindElement('hora').update('')
            window.FindElement('minuto').update('')
            window.FindElement('d_hora').update('')
            window.FindElement('d_minuto').update('')
            window.FindElement('frequencia').update('')
            window.FindElement('repeticao').update('')
            window.FindElement('location').update('')

window.close()  
