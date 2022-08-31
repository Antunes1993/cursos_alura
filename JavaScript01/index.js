var express = require('express');
var app = express();
app.use(express.json())
app.get('/ola', function(req, res){
    res.send('Olá mundo!');
});

app.post('/mensagem', function(req, res){
    var { mensagem } = req.body
    console.clear()
    console.log(mensagem);
    res.send('Recebido');
});

app.listen(3000, function() {
    console.log('App de Exemplo escutando na porta 3000!');
  });