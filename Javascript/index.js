class Cliente{
    nome;
    cpf;
    conta_corrente;
}

class ContaCorrente{
    agencia;
    saldo;
}

const cliente1 = new Cliente();
cliente1.nome = "Leonardo";

const contaCorrenteCliente1 = new ContaCorrente();
cliente1.conta_corrente = contaCorrenteCliente1;

cliente1.conta_corrente.agencia = "Santander";
cliente1.conta_corrente.saldo = 10000;

let valorSacado = 200000
contaCorrenteCliente1.saldo = contaCorrenteCliente1.saldo - valorSacado



console.log(cliente1);

