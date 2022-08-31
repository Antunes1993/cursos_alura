using System;

namespace bytebank
{
    class Program
    {
        static void Main(string[] args)
        {
            ContaCorrente conta1 = new ContaCorrente();
            conta1.titular = "Leonardo";
            conta1.conta = "10123";
            conta1.nome_agencia = "Itau";
            conta1.numero_agencia = 1;
            conta1.saldo = 100.00;

            conta1.Sacar(50);
            
        }
    }
}
