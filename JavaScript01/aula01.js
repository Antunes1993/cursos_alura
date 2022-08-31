function hello(){
    console.log("Hello");
}

class Pessoa{
    constructor(nome){
        this.nome = nome;
        this.apresentar()
    }
    apresentar(){
        console.log("Olá, eu me chamo", this.nome)
    }
}



module.exports = { Pessoa, hello };
