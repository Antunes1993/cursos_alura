using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace bytebank
{
    public class ContaCorrente
    {
        public string titular;
        public string conta;
        public string nome_agencia;
        public int numero_agencia;
        public double saldo;

        public void Sacar(double valor)
        {
            if (saldo < valor)
            {
                Console.WriteLine("Não pode sacar esse valor");

            }
            else
            {
                saldo -= valor;
                Console.WriteLine("Dinheiro sacado.");
            }
        }
    }
}
