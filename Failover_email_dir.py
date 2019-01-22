import sys
import time
import paramiko
import os
import cmd
import datetime
import socket
import getpass
import zipfile
from datetime import datetime
import smtplib
import email
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os.path

def SendEmail(text,path):

    # Credenciais
    email    = 'firewall.sdsla@samsung.com'
    # Informações da mensagem
    send_to_email = 'edson.j@samsung.com'
    subject      = text
    message      = text
    file_location = 'l:/ASA_FAILOVER/'+path+'/result.txt'

    # msg_envio = '\r\n'.join([
    #   'From: %s' % remetente,
    #   'To: %s' % destinatario,
    #   'Subject: %s' % assunto,
    #   '',
    #   '%s' % texto
    #   ])

    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = send_to_email
    msg['Subject'] = subject

    #server.starttls()
    msg.attach(MIMEText(message, 'plain'))

    filename = os.path.basename(file_location)
    attachment = open(file_location, "rb")
    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    msg.attach(part)

    server = smtplib.SMTP("smtp.w2.samsung.com",25)
    server.ehlo()
    server.helo()
    server.ehlo_or_helo_if_needed()
    #server.starttls()
    #server.login(email, password)
    text = msg.as_string()

    try:
        failed = server.sendmail(email, send_to_email, text)
        server.quit()
    except Exception as e:
        print(e)



def ListDir(name_path):
    path = name_path
    files = os.listdir('l:/ASA_FAILOVER/'+path+'/')
    texto = open('l:/ASA_FAILOVER/'+path+'/result.txt','w+')
    count = 0

    for name in files:
        valor = files[count]
        texto.write(valor+'\n')
        count = count = 1

    if count == 11:
        texto = 'Arquivos de Backup OK!'
        txt = open(path+'result.txt','wb')
        SendEmail(texto,path)
    else:
        texto = 'Alguns Backups Não Foram Feitos!'
        txt = open(path+'result.txt','wb')
        SendEmail(texto,path)


#Criando a pasta que vai salvar os bkps
def create_folde(folder_name):
    os.mkdir('L:/ASA_FAILOVER/'+folder_name)

#Test Copy file - Can Be remove
def copy_file(folder_name,name_file):
    shutil.copy('c:/BKP/'+name_file+'.zip', 'c:/BKP/'+folder_name+'/')
#Função que remove o arquivo .txt
def del_file(name_file,folder_name):
    os.remove(os.path.join('c:/BKP/', 'c:/BKP/'+folder_name+'/'+name_file))
#Função que zipa o arquivo .txt
def zip_test(name_file,namefolder):
    myfile = open("C:/BKP/"+namefolder+"/"+name_file+".zip", "wb")
    zip = zipfile.ZipFile(myfile, mode="w")
    info = zipfile.ZipInfo()
    info.filename=name_file
    # info.data_time = datatime.now().timetuple()
    info.compress_type = zipfile.ZIP_DEFLATED
    zip.close()
    myfile.close()

#Dicionario para ser usado em firewalls com context
context = {'sidia1':'changeto context admin','sidia2':'changeto context main','vpn':'changeto context main'}

#usuario que vai se conectar no Device
username = "firewall.sdsla"
password = str("Network2018!")
#Lendo o arquivo txt com os host que seram feitos os bkp
f1 = open('c:/Users/edson.j/Documents/Python-BKP-ASA/failover_host.txt','rb')
#Lendo quantas linhas existe no arquivo
ip = f1.readlines()
#Criação de pastas sempre que rodar o programa.
namefolder = str(time.strftime('%Y-%m-%d'))
create_folde(namefolder)

for line in ip:
    line = line.rstrip()
    device = str(line)

    try:
        #Conexão SSH
        remote_conn_pre=paramiko.SSHClient()
        remote_conn_pre.load_system_host_keys()
        remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        remote_conn_pre.connect(line, username=username, password=password, timeout=40)
        # Tratativa de erros na hora de logar no firewall
    except paramiko.AuthenticationException:
        print ('Authentication Failed '+device.decode('utf-8'))
        sys.exit(1)
    except:
        print ('Could not SSH to %s, waiting for start' % device.decode('utf-8'))
        sys.exit(1)
    #Msg que indica a Conexão com Firewall
    print("Cliente Connect-> %s" % line.decode('utf-8'))
    remote_conn = remote_conn_pre.invoke_shell()
    time.sleep(3)
    #Enviando a senha de enable
    remote_conn.send("en\n")
    remote_conn.send(password+'\n')
    time.sleep(5)

    #Opção para firewall com context
    if line.decode('utf-8') == '105.103.252.166':
        remote_conn.send(context['vpn']+'\n')
        time.sleep(2)
    elif line.decode('utf-8') == '105.103.141.8':
        remote_conn.send(ontext['sidia1']+'\n')
        time.sleep(2)
    elif line.decode('utf-8') == '105.112.144.36':
        remote_conn.send(ontext['sidia2']+'\n')
        time.sleep(2)
        #Comandos que seram executados depois do enable e verificação de context
    remote_conn.send("term pager 0\n")
    time.sleep(2)

    #remote_conn.send("sh run\n")
    #time.sleep(60)

    remote_conn.send("sh failover\n")
    time.sleep(2)

    #remote_conn.send("sh failover history\n")
    #time.sleep(2)

    #remote_conn.send("sh int\n")
    #time.sleep(2)

    remote_conn.send("\n")
    time.sleep(2)

    remote_conn.send("exit")
    time.sleep(2)
    #Salvando o retorno do comando na variavél
    output = remote_conn.recv(9000000)
    mytime = str(time.strftime('%Y-%m-%d-%H-%M-%S'))
    #namefolder = str(time.strftime('%Y-%m-%d'))

    #Criando o arquivo .txt e passando o conteudo que será salvo no arquivo
    arquivo = open('L:/ASA_FAILOVER/'+namefolder+'/BKP_'+line.decode('utf-8')+'-'+mytime+'.txt', 'wb')
    arquivo.write(output)

    name_file = 'BKP_'+line.decode('utf-8')+'-'+mytime+'.txt'

    arquivo.close()
    remote_conn_pre.close()
    #Msg de Finalização do bkp
    print('Backup of Device %s finished !' % line.decode('utf-8'))

ListDir(namefolder)
#Zipando o arquivo .txt
#zip_test(name_file, namefolder)
#Del o arquivo .txt deixando apenas o .zip
#del_file(name_file,namefolder)

f1.close()
sys.exit(1)
