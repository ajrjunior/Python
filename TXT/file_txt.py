test_txt = open('test_txt.txt','rb')
cores = {'verde': 'green', 'vermelho': 'red', 'preto': 'black', 'branco': 'white'}

qnt = test_txt.readlines()


for line in qnt:
    line = line.rstrip()
    ch = test_txt.read(1)
    ch = str(ch,'utf-8')

    if line.decode('utf-8') == 'AQ':
        print(cores['verde'])
