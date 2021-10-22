import re

padrao = "\w{5,50}@\w{3,10}.\w{2,3}.\w{2,3}"
texto = "aaabbbcc rodrigo123@gmail.com.br www.google.com"
resposta = re.search(padrao, texto)

print(resposta.group)

padrao_br = "\w{5,50}@[a-z]{3,10}.com.br"
texto_teste = "aaabbbcc rodrigo123@gmail.com.br ccbbbaaa"
resposta = re.search(padrao_br, texto_teste)

print(resposta.group)


# Padrão para telefone 
import re

padrao_molde = "(xx)aaaa-wwww"
padrao = "[0-9]{2}[0-9]{4,5}[0-9]{4}"
texto = "eu gosto do numero 213444372552723"
resposta = re.search(padrao,texto)

print(resposta)
