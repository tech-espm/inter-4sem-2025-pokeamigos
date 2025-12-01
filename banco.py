from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session
from config import conexao_banco

engine = create_engine(conexao_banco)

def obterIdArtista(name):
	try:	
		with Session(engine) as sessao:
			registro = sessao.execute(text(f"SELECT ArtId FROM Artista WHERE ArtNm = :name"), {"name": name}).first()

			if registro == None or registro[0] == None:
				return 0
			else:
				return registro[0]
	except Exception as e:
		return str(e)

def obterIdColecao(sigla):
	try:	
		with Session(engine) as sessao:
			registro = sessao.execute(text(f"SELECT CltId FROM Colecao WHERE CltSg = :name"), {"name": sigla}).first()

			if registro == None or registro[0] == None:
				return 0
			else:
				return registro[0]
	except Exception as e:
		return str(e)

def obterIdTpCarta(name):
	try:	
		with Session(engine) as sessao:
			registro = sessao.execute(text(f"SELECT TpCId FROM Tipo_Carta WHERE TpCNm = :name"), {"name": name}).first()

			if registro == None or registro[0] == None:
				return 0
			else:
				return registro[0]
	except Exception as e:
		return str(e)

def obterIdTpFoil(name):
	try:	
		with Session(engine) as sessao:
			registro = sessao.execute(text(f"SELECT TpFId FROM Tipo_Foil WHERE TpFNm = :name"), {"name": name}).first()

			if registro == None or registro[0] == None:
				return 0
			else:
				return registro[0]
	except Exception as e:
		return str(e)

def obterIdLoja(name):
	try:	
		with Session(engine) as sessao:
			registro = sessao.execute(text(f"SELECT LojId FROM Loja WHERE LojNm = :name"), {"name": name}).first()

			if registro == None or registro[0] == None:
				return 0
			else:
				return registro[0]
	except Exception as e:
		return str(e)

def obterIdElemento(name):
	try:	
		with Session(engine) as sessao:
			registro = sessao.execute(text(f"SELECT ElmId FROM Elemento WHERE ElmNm = :name"), {"name": name}).first()

			if registro == None or registro[0] == None:
				return 0
			else:
				return registro[0]
	except Exception as e:
		return str(e)

def obterIdCarta(name):
	try:	
		with Session(engine) as sessao:
			registro = sessao.execute(text(f"SELECT max(CrdId) FROM Carta WHERE CrdNm = :name"), {"name": name}).first()

			if registro == None or registro[0] == None:
				return 0
			else:
				return registro[0]
	except Exception as e:
		return str(e)
	
def obterCarta(name) -> dict:
	try:	
		with Session(engine) as sessao:
			query = '''Select a.AnuVlr, tpf.TpFNm, l.LojNm, c.CrdNm, c.CrdPtvs, c.CrdImg, tpc.TpCNm, e.ElmNm, e.ElmImg, cl.CltNm, cl.CltSg, art.ArtNm
							from Anuncio a 
							inner join Carta c on a.CrdId = c.CrdId
							left join Elemento e on c.ElmId = e.ElmId
							inner join Tipo_Carta tpc on c.TpCId = tpc.TpCId
							inner join Colecao cl on c.CltId = cl.CltId
							inner join Tipo_Foil tpf on a.TpFId = tpf.TpFId
		 					left join Artista art on c.ArtId = art.ArtId 	
		 					inner join Loja l on a.LojId = l.LojId 	
							where CrdNm = :name
		 					order by AnuVlr asc;'''
			

			registros = sessao.execute(
				text(query),
				{"name": name})

			registros = registros.all()
			if len(registros) == 0:
				return "Nenum registro encontrado"
			
			anuncios = []
			for anuncio in registros:
				anuncios.append({
					"valor": anuncio[0],
					"tipoFoil": anuncio[1],
					'loja': anuncio[2]
					})

			carta = {
				'nome' : registros[0][3],
				'hp' : registros[0][4],
				'imagem' : registros[0][5],
				'tipoCarta' : registros[0][6],
				'elemento' : registros[0][7],
				'imagemElemento' : registros[0][8],
				'colecao' : registros[0][9],
				'siglaColecao' : registros[0][10],
				'artista' : registros[0][11],
				'anuncios' : anuncios
			}
			return carta
	except Exception as e:
		return str(e)
	
def procurarCartas(carta, colecao, elemento, album, desejos, usuario) -> list:
	try:
		with Session(engine) as sessao:
			where = "where"
			join = ""
			params = {}
			
			join_album_adicionado = False

			if bool(colecao):
				if where != "where":
					where += " and"
				where += " clt.CltNm = :colecao "
				join += " inner join Colecao clt on c.CltId = clt.CltId "
				params['colecao'] = str(colecao)

			if bool(elemento):
				if where != "where":
					where += " and"
				where += " c.ElmId = :elemento"
				join += " inner join Elemento e on c.ElmId = e.ElmId "
				params['elemento'] = elemento

			if bool(carta):
				if where != "where":
					where += " and"
				where += " c.CrdNm LIKE :carta"
				params['carta'] = f"%{carta}%"

			if bool(album) or bool(desejos) or bool(usuario):
				
				if not join_album_adicionado:
					join += """ 
						inner join Album_Carta ac on c.CrdId = ac.CrdId 
						inner join Album a on ac.AlbId = a.AlbId 
						inner join Usuario u on a.IdUsu = u.UsuId 
					"""
					join_album_adicionado = True

				if bool(usuario):
					if where != "where":
						where += " and"
					where += " u.UsuId = :usuario"
					params['usuario'] = usuario

				if bool(album):
					if where != "where":
						where += " and"
					where += " a.AlbId = :album"
					params['album'] = album

				if bool(desejos):
					if where != "where":
						where += " and"
					where += " a.IsWish = :desejos"
					params['desejos'] = desejos

			if where == "where":
				return 'Nenhum filtro aplicado'
			
			query = f"select c.CrdNm, c.CrdImg, c.CrdId from Carta c {join} {where} order by c.CrdNm"
			registros = sessao.execute(text(query), params).all()

			if not registros:
				return []
			
			cartas = []
			for row in registros:
				a = {
					"nome": row.CrdNm,
					"imagem": row.CrdImg,
					"id": row.CrdId
				}
				cartas.append(a)
			return cartas

	except Exception as e:
		print(f"Erro: {e}")
		return []

def inserirArtista(name):
	try:
		with Session(engine) as sessao, sessao.begin():
			sessao.execute(text(f"INSERT INTO Artista (ArtNm) VALUES (:name)"), {"name": name})
	except Exception as e:
		return str(e)

def inserirTpCarta(name):
	try:
		with Session(engine) as sessao, sessao.begin():
			sessao.execute(text(f"INSERT INTO Tipo_Carta (TpCNm) VALUES (:name)"), {"name": name})
	except Exception as e:
		return str(e)

def inserirTpFoil(name):
	try:
		with Session(engine) as sessao, sessao.begin():
			sessao.execute(text(f"INSERT INTO Tipo_Foil (TpFNm) VALUES (:name)"), {"name": name})
	except Exception as e:
		return str(e)

def inserirLoja(name):
	try:
		with Session(engine) as sessao, sessao.begin():
			sessao.execute(text(f"INSERT INTO Loja (LojNm) VALUES (:name)"), {"name": name})
	except Exception as e:
		return str(e)

def inserirCarta(name, hp, img, CltId, ElmId, TpCId, ArtId):
	try:
		with Session(engine) as sessao, sessao.begin():
			sessao.execute(text(f"INSERT INTO Carta (CrdNm, CrdPtvs, CrdImg, CltId, ElmId, TpCId, ArtId) VALUES (:name,:hp, :img, :CltId, :ElmId, :TpCId, :ArtId)"),
                {
					"name": name,
					"hp": hp,
					"img": img,
					"CltId": CltId,
					"ElmId": ElmId,
					"TpCId": TpCId,
					"ArtId": ArtId
				})
	except Exception as e:
		return str(e)

def inserirCartaT(name, img, CltId, TpCId, ArtId):
	try:
		with Session(engine) as sessao, sessao.begin():
			sessao.execute(text(f"INSERT INTO Carta (CrdNm, CrdImg, CltId, TpCId, ArtId) VALUES (:name, :img, :CltId, :TpCId, :ArtId)"),
                {
					"name": name,
					"img": img,
					"CltId": CltId,
					"TpCId": TpCId,
					"ArtId": ArtId
				})
	except Exception as e:
		return str(e)

def inserirEnergia(name, img, CltId, TpCId, ElmId):
	try:
		with Session(engine) as sessao, sessao.begin():
			sessao.execute(text(f"INSERT INTO Carta (CrdNm, CrdImg, CltId, TpCId, ElmId) VALUES (:name, :img, :CltId, :TpCId, :ElmId)"),
                {
					"name": name,
					"img": img,
					"CltId": CltId,
					"TpCId": TpCId,
					"ElmId": ElmId
				})
	except Exception as e:
		return str(e)

def inserirAnuncio(valor, LojId, CrdId, TpFId):
	try:
		with Session(engine) as sessao, sessao.begin():
			sessao.execute(text(f"INSERT INTO Anuncio (AnuVlr, LojId, CrdId, TpFId) VALUES (:valor, :LojId, :CrdId, :TpFId)"),
                {
					"valor": valor,
					"LojId": LojId,
					"CrdId": CrdId,
					"TpFId": TpFId
				})
	except Exception as e:
		return str(e)

def CartaCaraElm(elemento):
	try:
		with Session(engine) as sessao:
			registro = sessao.execute(text('''select max(ElmNm) as Elm, MAX(AnuVlr) as valor, CrdNm, MAX(CrdPtvs), max(CltNm) 
    from Anuncio a
   inner join Carta c on a.CrdId = c.CrdId
   inner join Elemento e on c.ElmId = e.ElmId
   inner join Colecao clt on clt.CltId = c.CltId
   group by CrdNm
   HAVING Elm LIKE :elemento
   order by valor desc
   limit 5;'''), {"elemento" : elemento})
			lista = []
			for i in registro:
				a = {
					"elemento": i[0],
					"valor": i[1],
					"pokemon": i[2],
					"vida": i[3],
					"colecao": i[4]
				}
				lista.append(a)
			return lista
	except Exception as e:
		return str(e)
	
def CartaMaisCara():
	try:
		with Session(engine) as sessao:
			registro = sessao.execute(text('''select MAX(`ElmNm`) as elemento, MAX(AnuVlr) as valor, CrdNm, MAX(CrdPtvs), max(CltNm) 
    from Anuncio a
   inner join Carta c on a.CrdId = c.CrdId
   inner join Elemento e on c.ElmId = e.ElmId
   inner join Colecao clt on clt.CltId = c.CltId
   group by CrdNm
   order by valor desc
   limit 10;'''))
			lista = []
			for i in registro:
				a = {
					"elemento": i[0],
					"valor": i[1],
					"pokemon": i[2],
					"vida": i[3],
					"colecao": i[4]
				}
				lista.append(a)
			return lista
	except Exception as e:
		return str(e)

def CartaMaisBarata():
	try:
		with Session(engine) as sessao:
			registro = sessao.execute(text('''select MAX(`ElmNm`) as elemento, MIN(AnuVlr) as valor, CrdNm, MAX(CrdPtvs), max(CltNm) 
    from Anuncio a
   inner join Carta c on a.CrdId = c.CrdId
   inner join Elemento e on c.ElmId = e.ElmId
   inner join Colecao clt on clt.CltId = c.CltId
   group by CrdNm
   order by valor ASC
   limit 10;
'''))
			lista = []
			for i in registro:
				a = {
					"elemento": i[0],
					"valor": i[1],
					"pokemon": i[2],
					"vida": i[3],
					"colecao": i[4]
				}
				lista.append(a)
			return lista
	except Exception as e:
		return str(e)

def ArtistaMaisPika():
	try:
		with Session(engine) as sessao:
			registro = sessao.execute(text('''select ArtNm, sum(AnuVlr) as ValorTotal from `Anuncio` a
    inner join Carta c on a.CrdId = c.CrdId
    inner join Artista art on art.ArtId = c.ArtId
    group by ArtNm
    order by ValorTotal desc
    limit 10;
'''))
			lista = []
			for i in registro:
				a = {
					"artista": i[0],
					"valor": i[1]
				}
				lista.append(a)
			return lista
	except Exception as e:
		return str(e)

