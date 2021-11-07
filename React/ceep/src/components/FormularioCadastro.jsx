import React, { Component } from 'react';
import "./CardNota/CardNotaEstilo.css"

export class FormularioCadastro extends Component {
    constructor(props){
        super(props);
        this.titulo = "";    
        this.texto = "";    
    }
        
    _handleMudancaTitulo(evento){
        this.titulo = evento.target.value;
    }
    
    _handleMudancaTexto(evento){
        this.texto = evento.target.value;
        
    }

    _criarNota(evento){
        evento.preventDefault();
        this.props.criarNota(this.titulo, this.texto);
        console.log("Iteração: " + this.texto + " " + this.titulo);
    }


    render(){
        return(    
            <form className="main-form"
            onSubmit={this._criarNota.bind(this)}
          >
            <input
              type="text"
              placeholder="Título"
              className="input-form"
              onChange={this._handleMudancaTitulo.bind(this)}
            />
            <textarea
              rows={15}
              placeholder="Escreva sua nota..."
              className="input-form__text-area"
              onChange={this._handleMudancaTexto.bind(this)}
            />
            <button className="input-form__button">
              Criar Nota
            </button>
          </form>   
       
);
    }
    }