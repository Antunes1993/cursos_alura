# Curso: Python - Avançando na linguagem.
# Escola: Alura
# Objetivo do código: Jogo da forca. 
import random

def MensagemInicial():
    print("**********************************")
    print("********BEM VINDO AO JOGO*********")
    print("**********************************")

def CarregarPalavra():
    #Abre o arquivo "palavras.txt" e inicializa uma lista
    arquivo = open("palavras.txt", "r")
    palavras = []

    #Adiciona cada linha do arquivo dentro da lista "palavras"
    for linha in arquivo:
        linha = linha.strip()
        palavras.append(linha)
    
    #Fecha o arquivo e cria um numero pseudo-aleatorio com a biblioteca random.
    arquivo.close()
    numero = random.randrange(0,len(palavras))
    
    #Define a palavra secreta como uma das palavras contidas dentro do vetor "palavras".
    palavra_secreta = palavras[numero].lower()
    return palavra_secreta

def MensagemGanhou():
    print("Parabéns, você ganhou!")
    print("       ___________      ")
    print("      '._==_==_=_.'     ")
    print("      .-\\:      /-.    ")
    print("     | (|:.     |) |    ")
    print("      '-|:.     |-'     ")
    print("        \\::.    /      ")
    print("         '::. .'        ")
    print("           ) (          ")
    print("         _.' '._        ")
    print("        '-------'       ")

def MensagemPerdeu(palavra_secreta):
    print("Puxa, você foi enforcado!")
    print("A palavra era {}".format(palavra_secreta))
    print("    _______________         ")
    print("   /               \       ")
    print("  /                 \      ")
    print("//                   \/\  ")
    print("\|   XXXX     XXXX   | /   ")
    print(" |   XXXX     XXXX   |/     ")
    print(" |   XXX       XXX   |      ")
    print(" |                   |      ")
    print(" \__      XXX      __/     ")
    print("   |\     XXX     /|       ")
    print("   | |           | |        ")
    print("   | I I I I I I I |        ")
    print("   |  I I I I I I  |        ")
    print("   \_             _/       ")
    print("     \_         _/         ")
    print("       \_______/           ")

def MensagemErros(erros):
    print("  _______     ")
    print(" |/      |    ")

    if(erros == 1):
        print(" |      (_)   ")
        print(" |            ")
        print(" |            ")
        print(" |            ")

    if(erros == 2):
        print(" |      (_)   ")
        print(" |      \     ")
        print(" |            ")
        print(" |            ")

    if(erros == 3):
        print(" |      (_)   ")
        print(" |      \|    ")
        print(" |            ")
        print(" |            ")

    if(erros == 4):
        print(" |      (_)   ")
        print(" |      \|/   ")
        print(" |            ")
        print(" |            ")

    if(erros == 5):
        print(" |      (_)   ")
        print(" |      \|/   ")
        print(" |       |    ")
        print(" |            ")

    if(erros == 6):
        print(" |      (_)   ")
        print(" |      \|/   ")
        print(" |       |    ")
        print(" |      /     ")

    if (erros == 7):
        print(" |      (_)   ")
        print(" |      \|/   ")
        print(" |       |    ")
        print(" |      / \   ")

    print(" |            ")
    print("_|___         ")
    print()

def Jogar():
    MensagemInicial()    
    palavra_secreta = CarregarPalavra()

    #Inicializa a lista letras_acertadas de acordo com a quantidade de letras da palavra_secreta.
    letras_acertadas = ["_" for letra in palavra_secreta]

    enforcou = False
    acertou = False 
    erros = 0
    #Ciclo do jogo
    
    while (not enforcou and not acertou):
        #Input do usuário
        chute = input ("Digite uma letra: ")
        #Remove espaços
        chute = chute.strip()

        if (chute in palavra_secreta):
            index = 0
            #Busca a letra inserida pelo usuário dentro da palavra_secreta
            for letra in palavra_secreta:
                if(letra.lower() == chute.lower()):
                    letras_acertadas[index] = letra
                    print ("Acertou a letra {} na posição {}".format(chute, index))

                index +=1
        else:
            erros +=1

        #Condições para derrota ou vitória na partida
        enforcou = erros == 6
        acertou = "_" not in letras_acertadas

        #Verifica letras faltantes
        letras_faltando = str(letras_acertadas.count("_"))
        print ("Faltam acertar {} letra(s)".format(letras_faltando))       
        print("Próxima tentativa...", letras_acertadas)
        MensagemErros(erros)
    
    #Rotina para exibir o status final do jogo.
    if(acertou):
        MensagemGanhou()
    else:
        MensagemPerdeu(palavra_secreta)
    print("Fim de jogo!")


if(__name__ == "__main__"):
    Jogar()