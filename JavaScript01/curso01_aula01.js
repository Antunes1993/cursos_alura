console.log("Meu primeiro programa");

const listaDestinos = new Array(
    'Salvador',
    'São Paulo',
    'Rio de Janeiro'
);

console.log(listaDestinos);
const idadeComprador =  15; 

if(idadeComprador >= 18){
    listaDestinos.splice(1,1);
}


let contador = 0; 

while( contador < 3 ){
    console.log(listaDestinos[1]);
    contador = contador + 1;
}