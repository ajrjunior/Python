import csv

def read():
    row = ['4', ' Danny', ' New York']

    with open('people1.csv', 'a') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(row)

    csvFile.close()

def open_txt():

    valor = open('e:/extracted_ip_addresses.txt','r')
    int = valor.readlines()
    vl = []
    i = 0

    for line in int:
        line.rstrip()
        vl.insert(i,line)
        i = i + 1

    for qnt in vl:
        print (qnt,end=" ")

    valor.close()

open_txt()
