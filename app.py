from flask import Flask, render_template, json, request, Response, make_response
import config
from datetime import datetime
import banco as b

app = Flask(__name__)

@app.get('/')
def index():
    hoje = datetime.today().strftime('%Y-%m-%d')
    return render_template('index/index.html', hoje=hoje)

@app.get('/sobre')
def sobre():
    return render_template('index/sobre.html', titulo='Sobre Nós')

@app.get('/dash')
def t():
    return render_template('index/t.html', titulo='Dash')


# adicionar a queryString com o id ou nome
@app.get('/carta')
def carta():
    return render_template('index/carta.html', titulo='Carta')

@app.get('/colecoes')
def colecoes():
    return render_template('index/colecoes.html', titulo='Coleções')

@app.get('/desejos')
def desejos():
    return render_template('index/desejos.html', titulo='Desejos')


@app.get('/meu-album')
def meu_album():
    return render_template('index/meu-album.html', titulo='Meu Álbum')



@app.get('/obterDados')
def obterDados():
    dados = [
        { 'dia': '10/09', 'valor': 80 },
        { 'dia': '11/09', 'valor': 92 },
        { 'dia': '12/09', 'valor': 90 },
        { 'dia': '13/09', 'valor': 101 },
        { 'dia': '14/09', 'valor': 105 },
        { 'dia': '15/09', 'valor': 100 },
        { 'dia': '16/09', 'valor': 64 },
        { 'dia': '17/09', 'valor': 78 },
        { 'dia': '18/09', 'valor': 93 },
        { 'dia': '19/09', 'valor': 110 }
    ]
    return json.jsonify(dados)

@app.get('/obterArtistas')
def obterArtistasMaisCaros():
    dados = b.ArtistaMaisPika()
    resposta = make_response(json.jsonify(dados))

    if type(dados) == str:
        resposta.status_code = 500
    else:
        resposta.status_code = 200
        
    return resposta

@app.get('/obterPokemons')
def obterPokemonsMaisCaros():
    dados = b.CartaMaisCara()
    resposta = make_response(json.jsonify(dados))

    if type(dados) == str:
        resposta.status_code = 500
    else:
        resposta.status_code = 200
        
    return resposta

@app.get('/obterElemento')
def obterElementoMaisCaros():
    elm = request.args["elemento"]
    dados = b.CartaCaraElm(elm)
    resposta = make_response(json.jsonify(dados))

    if type(dados) == str:
        resposta.status_code = 500
    else:
        resposta.status_code = 200
        
    return resposta

@app.get('/obterPokemonsBaratos')
def obterPokemonsMaisBaratos():
    dados = b.CartaMaisBarata()
    resposta = make_response(json.jsonify(dados))

    if type(dados) == str:
        resposta.status_code = 500
    else:
        resposta.status_code = 200

    return resposta

@app.post('/criar')
def criar():
    dados = request.json
    print(dados['id'])
    print(dados['nome'])
    return Response(status=204)

if __name__ == '__main__':
    app.run(host=config.host, port=config.port)
