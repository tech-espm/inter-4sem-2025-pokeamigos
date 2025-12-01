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
    nome = request.args.get('nome')
    if nome is None: 
        return render_template('index/erro.html', titulo='Erro', mensagem='Nome da carta não fornecido.')
    
    carta = b.obterCarta(nome)
    if type(carta) is str:
        return render_template('index/erro.html', titulo='Erro', mensagem=carta)
    return render_template('index/carta.html', titulo='Archen', carta=carta)


@app.get('/colecoes')
def colecoes():
    return render_template('index/colecoes.html', titulo='Coleções')


@app.get('/procurar')
def procurar():
    filtro_nome = request.args.get('nome')
    filtro_colecao = request.args.get('colecao')
    filtro_elemento = request.args.get('elemento')
    filtro_album = request.args.get('album')
    filtro_desejos = request.args.get('desejos')
    filtro_artista = request.args.get('artista')
    
    titulo_pag = "Resultados da Busca"
    if filtro_desejos:
        titulo_pag = "Meus Desejos"
    elif filtro_album:
        titulo_pag = "Meus Álbuns"
    elif filtro_colecao:
        titulo_pag = f"Coleção: {filtro_colecao}"
    elif filtro_nome:
        titulo_pag = f"Busca por: {filtro_nome}"
    elif filtro_elemento:
        titulo_pag = f"Elemento: {filtro_elemento}"

    cartas = b.procurarCartas(
        carta=filtro_nome,
        colecao=filtro_colecao,
        elemento=filtro_elemento,
        album=filtro_album,
        desejos=filtro_desejos,
        artista=filtro_artista,
        usuario=None
    )
    print(filtro_colecao)

    if isinstance(cartas, str):
        return render_template('index/erro.html', titulo='Erro na Busca', mensagem=cartas)

    return render_template('index/listagem.html', titulo=titulo_pag, cartas=cartas)

@app.get('/meu-album')
def meu_album():
    return render_template('index/meu-album.html', titulo='Meu Álbum') #usar listagem.html quando houver usuario




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
    app.run(host=config.host, port=config.port, debug=True)
