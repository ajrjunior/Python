cores = {'preto':'black','branco':'white','amarelo':'yello','verde':'green'}
escolha = input('Escolha a Cor para ser traduzida: ').lower()
traducao = cores.get(escolha, 'Está cor não existe !')
print(traducao)
