#!/usr/bin/env python
#Script criado por André Luís Drumond Leite (Contato: 11 993812718, e-mail: adrumondleite@gmail.com)
#importanto as bibliotecas necessarias
import sys
import time
import select
import paramiko
import getpass

#Capturando o usuario e password
username = raw_input("Digite seu usuario de rede: ")
password = getpass.getpass("Digite seu password: ")

#Criando a funcao utilizando a variavel host e command
def mod1_bkp_conf(host, command):
    #criando a variavel dia para introduzir ao nome do arquivo
    day = (time.strftime("%d-%m-%y"))
    #setando a primeira tentativa de conexao
    i = 1
    #estrutura de repetiacao para a tentativa de conexao
    while True:
        print "Trying to connect to %s (%i/30)" % (host, i)
        try:
        #Parametros para conexao SSH (Utilizado pela biblioteca paramiko)
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(host, username = username, password = password)
            print "Connected to %s" % host
            break
        #excecao caso haja erro de autenticacao
        except paramiko.AuthenticationException:
            print "Authentication Failed when connection to %s" % host
            sys.exit(1)
        #execao para qualquer outro tipo de erro
        except:
            print "Could not SSH to %s, waiting for it to start" % host
            i = i + 1
            time.sleep(2)
        #na trigesima conexao o programa ira fechar
        if i == 30:
            print "Could not connect to %s. Giving up" % host
            sys.exit(1)
    #rodando o comando imposto na chamada da funcao
    print "Runnning %s" % command
    stdin, stdout, stderr = ssh.exec_command(command)
    #criando o arquivo utilizando a string da variavel host, day no modo appeding
    newfile = open(host + "_" + day + ".txt", "a")
    #estrutura de repeticao para verificar se o output do comando foi finalizado
    while not stdout.channel.exit_status_ready():
        if stdout.channel.recv_ready():
            rl, wl, xl = select.select([stdout.channel], [], [], 0.0)
            if len(rl) > 0:
            #estrutura de repeticao para salvar cada linha no arquivo criado anteriormente
                for each_line in stdout.channel.recv(1024),:
                    newfile.write(each_line)
    newfile.close()
    print "Command done, closing SSH Connection"
    #fechando a conexao ssh
    ssh.close()
#rodando as funcoes com cada host e comando
#Core-Matriz-1
mod1_bkp_conf("192.168.1.1", "show Clock")
mod1_bkp_conf("192.168.1.1", "show int status")
mod1_bkp_conf("192.168.1.1", "show inventory")
mod1_bkp_conf("192.168.1.1", "show Version")
