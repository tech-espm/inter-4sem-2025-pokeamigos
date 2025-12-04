from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session
from config import conexao_banco
import pandas as pd

engine = create_engine(conexao_banco)

def foda():
    try:
        with Session(engine) as sessao:
            registro = sessao.execute(text('select AnuVlr, ElmNm, TpFNm, TpCNm, CltNm from Anuncio a inner join Carta c on a.CrdId = c.CrdId left join Elemento e on c.ElmId = e.ElmId inner join Tipo_Carta tpc on c.TpCId = tpc.TpCId inner join Colecao cl on c.CltId = cl.CltId inner join Tipo_Foil tpf on a.TpFId = tpf.TpFId;'))
            lista = []
            for i in registro:
                l = {
                    "valor": i[0],
                    "elemento": i[1],
                    "foil": i[2],
                    "tipoCarta": i[3],
                    "colecao": i[4],
                }
                lista.append(l)
            
            df = pd.DataFrame(lista)

            def categoriza_tipo(x:str):
                if 'Pokémon' in x:
                    return 'Pokémon'
                elif 'Trainer' in x:
                    return 'Trainer'
                elif 'Energy' in x:
                    return 'Energy'

            df['tipoCarta'] = df['tipoCarta'].apply(lambda x: categoriza_tipo(x))

            df.to_csv("predicaoBase.csv",index=False)
            return len(lista)

    except Exception as e:
        return str(e)

print(foda())
        