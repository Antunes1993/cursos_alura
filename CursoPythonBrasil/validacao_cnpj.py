#1. CPF e CNPJ
#1.1. Implementação do conceito de Factory.
#--------------------------------------------------------------------
from validate_docbr import CPF, CNPJ 


#Criação da classe documento 
class Document:

    @staticmethod
    def cria_documento(documento):
        if len(documento) == 11:
            return DocCpf(documento)
        elif len(documento) == 14:
            return DocCnpj(documento)
        else:
            raise ValueError("Quantidade de dígitos incorreta.")

#Criação da classe DocCPF
class DocCpf: 
    def __init__(self, documento):
        if self.valida(documento):
            self.cpf = documento 
        else:
            raise ValueError("CPF inválido.")

    def __str__(self):
        return self.format()

    def valida(self, documento):
        validador = CPF()
        return validador.validate(documento)

    def format(self):
      mascara = CPF()
      return mascara.mask(self.cpf)

#Criação da classe DocCNPJ
class DocCnpj:
    def __init__(self, documento):
        if self.valida(documento):
            self.cnpj = documento
        else:
            raise ValueError("Cnpj inválido!")

    def __str__(self):
        return self.format()

    def valida(self, documento):
        mascara = CNPJ()
        return mascara.validate(documento)

    def format(self):
        mascara = CNPJ()
        return mascara.mask(self.cnpj)

doc1 = CpfCnpj("35379838000112", "cnpj")
print (doc1)