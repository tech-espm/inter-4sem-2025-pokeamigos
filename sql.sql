-- Active: 1764253057582@@127.0.0.1@3306@pokeamigos
use pokeamigos;

select max(ElmNm) as Elm, MAX(AnuVlr) as valor, CrdNm, MAX(CrdPtvs), max(CltNm) 
    from Anuncio a
   inner join Carta c on a.CrdId = c.CrdId
   inner join Elemento e on c.ElmId = e.ElmId
   inner join Colecao clt on clt.CltId = c.CltId
   group by CrdNm
   HAVING Elm LIKE "Água"
   order by valor desc
   limit 5;

select MAX(`ElmNm`) as elemento, MAX(AnuVlr) as valor, CrdNm, MAX(CrdPtvs), max(CltNm) 
    from Anuncio a
   inner join Carta c on a.CrdId = c.CrdId
   inner join Elemento e on c.ElmId = e.ElmId
   inner join Colecao clt on clt.CltId = c.CltId
   group by CrdNm
   order by valor desc
   limit 10;

select MAX(`ElmNm`) as elemento, MIN(AnuVlr) as valor, CrdNm, MAX(CrdPtvs), max(CltNm) 
    from Anuncio a
   inner join Carta c on a.CrdId = c.CrdId
   inner join Elemento e on c.ElmId = e.ElmId
   inner join Colecao clt on clt.CltId = c.CltId
   group by CrdNm
   order by valor ASC
   limit 10;


   select ArtNm, sum(AnuVlr) as ValorTotal from `Anuncio` a
    inner join Carta c on a.CrdId = c.CrdId
    inner join Artista art on art.ArtId = c.ArtId
    group by ArtNm
    order by ValorTotal desc;
