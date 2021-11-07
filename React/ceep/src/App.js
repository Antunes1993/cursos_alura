import React, { Component } from 'react';
import { ListaDeNotas } from './components/ListaDeNotas';
import { FormularioCadastro } from './components/FormularioCadastro';
import "./components/CardNota/CardNotaEstilo.css"

class App extends Component {
  constructor(props){
    super(props);
    this.state = {
      notas:[]
    }
  }

  criarNota(titulo, texto){
    const novaNota = {titulo, texto};
    const novoArrayNotas = [...this.state.notas, novaNota];
    const novoEstado = {
      notas: novoArrayNotas
    }
    this.setState(novoEstado)      
}

  render(){
    console.log("teste");
    return(
    <section className="main-section">
      <FormularioCadastro criarNota={this.criarNota.bind(this)}/>
      <ListaDeNotas notas = {this.state.notas}/>
    </section>    
    );
  }
}

export default App;
