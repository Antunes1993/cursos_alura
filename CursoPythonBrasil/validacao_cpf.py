#1. CPF 
#---------------------------------------------------------------------
#Criação de classe
class Cpf: 
    def __init__(self, documento):
        documento = str(documento)
        if self.cpf_valido(documento):
            self.cpf = documento
        else:
            raise ValueError("CPF inválido!")

    def __str__(self):
        return str(self.formata_cpf())

    def cpf_valido(self, documento):
        if len(documento) == 11:
            return True 
        else: 
            return False

    def formata_cpf(self):
        fatia_1 = self.cpf[:3]
        fatia_2 = self.cpf[3:6]
        fatia_3 = self.cpf[6:9]
        fatia_4 = self.cpf[9:]
        return(
            "{}.{}.{}-{}".format(
            fatia_1, fatia_2, fatia_3, fatia_4)
        )


#Teste da classe.
cpf = "15093534270"
obj_cpf = Cpf(cpf)
#print(obj_cpf)

#Pacote de validação de dados brasileiros
# Endereço do projeto: https://pypi.org/project/validate-docbr/
from validate_docbr import CPF 

#Passagem da lógica de validação da biblioteca para a nossa classe. 
class CPF_Validacao: 
    #Construtor da classe
    def __init__(self, documento):

        #Recebe a string com a informação do CPF
        documento = str(documento)

        #Verifica se ele é válido. Caso não seja, exibe um erro.
        if self.cpf_valido(documento):
            self.cpf = documento 
        else:
            raise ValueError("CPF inválido!")   
    
    def __str__(self):
        return self.format_cpf()

    #Rotina para verificar se o CPF é válido.
    def cpf_valido(self, documento):
        if len(documento) == 11:
            #Insere rotina de validação com base na biblioteca importada
            validador = CPF()
            return validador.validate(cpf)           
            
        else:
            print ("Not OK")
            return False

    #Rotina para deixar o cpf com formato correto
    def format_cpf(self):
        fatia_um = self.cpf[:3]
        fatia_dois = self.cpf[3:6]
        fatia_tres = self.cpf[6:9]
        fatia_quatro = self.cpf[9:]
        return(
            "{}.{}.{}-{}".format(
                fatia_um,
                fatia_dois,
                fatia_tres,
                fatia_quatro
            )
        )

cpf = CPF_Validacao('15093534706')
print (cpf)