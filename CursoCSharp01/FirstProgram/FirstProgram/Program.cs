using System;

namespace FirstProgram
{
    class Program
    {
        static void Main(string[] args)
        {
            int fatorial = 1;
            for(int num =3;  num < 11; num++)
            {
                fatorial *= num;
                Console.WriteLine("Fatorial de " + num + " " + fatorial);
            }
        }
    }
}
