# Projeto Interdisciplinar IV - Sistemas de Informação ESPM

<p align="center">
    <a href="https://www.espm.br/cursos-de-graduacao/sistemas-de-informacao/"><img src="https://raw.githubusercontent.com/tech-espm/misc-template/main/logo.png" alt="Sistemas de Informação ESPM" style="width: 375px;"/></a>
</p>

# *PokéAmigos*

## Visão Geral
O **PokéAmigos** é um projeto acadêmico desenvolvido no contexto do **Projeto Interdisciplinar IV** do curso de **Sistemas de Informação da ESPM**.  
O objetivo do projeto é construir uma **aplicação web integrada a um banco de dados**, capaz de **coletar, tratar e disponibilizar dados** relacionados ao universo Pokémon, utilizando técnicas de **raspagem de dados**, **ETL** e **organização relacional**.

O sistema foi pensado para consolidar dados externos em uma base estruturada e permitir sua visualização e uso por meio de uma interface web simples.

---
## Participantes
Projeto desenvolvido por alunos do curso de **Sistemas de Informação — ESPM**  
        - [Alexandre Martinelli](https://github.com/alexandremartinelli11)
        - [André Henrique Pacheco Alves](https://github.com/andre-alves77)
        - [Gabriel Cardoso Campos Rodrigues](https://github.com/gabrielccr-555)
        - [Hugo Coscelli Ferraz](https://github.com/Z-Hugo-Ferraz)
        - [Julia Akemi Mullis](https://github.com/akemi-m)
        - [Theo Camuri Gaspar](https://github.com/tigasparzin) 

---

## Objetivos do Projeto
- Aplicar conceitos de **engenharia de dados** (coleta, tratamento e persistência);
- Integrar **scripts de raspagem** com uma aplicação web;
- Utilizar **banco de dados relacional** para armazenamento estruturado;
- Desenvolver uma solução alinhada às exigências acadêmicas do Inter IV;
- Demonstrar organização de código, documentação e reprodutibilidade.

---

## Arquitetura e Fluxo de Dados

```
[Raspagem de Dados]
        ↓
[Tratamento / ETL]
        ↓
[Banco de Dados Relacional]
        ↓
[Aplicação Web]
        ↓
[Visualização pelo Usuário]
```

O fluxo é dividido em etapas independentes, facilitando manutenção, testes e evolução do projeto.

---

## Estrutura do Repositório

```
.
├── app.py                  # Aplicação web (ponto de entrada)
├── banco.py                # Conexão e operações com o banco de dados
├── raspagem.py             # Script de coleta/raspagem de dados
├── predicaoEtl.py          # ETL e preparação dos dados
├── predicaoBase.csv        # Base utilizada no processo de ETL/predição
├── pokeamigosBanco.sql     # Script SQL de criação do banco
├── templates/              # Templates HTML da aplicação
└── static/                 # Arquivos estáticos (CSS, JS, imagens)
```

---

## Como Executar o Projeto Localmente

### Pré-requisitos
- Python 3.10 ou superior
- Sistema Gerenciador de Banco de Dados compatível com SQL
- Git

### Criar ambiente virtual
```bash
python -m venv .venv
```

### Ativar o ambiente virtual (Windows)
```bash
.venv\Scripts\activate
```

### Instalar dependências
```bash
pip install -r requirements.txt
```

### Configurar o banco de dados
- Crie um banco local (ex: `pokeamigos`)
- Execute o script:
```sql
pokeamigosBanco.sql
```
- Ajuste as credenciais no arquivo `banco.py` ou via variáveis de ambiente

### Executar a aplicação web
```bash
python app.py
```

---

## Raspagem e ETL
O projeto conta com scripts auxiliares que podem ser executados separadamente:

- **Raspagem de dados**
```bash
python raspagem.py
```

- **Processo de ETL / preparação**
```bash
python predicaoEtl.py
```

Esses scripts alimentam e organizam a base utilizada pela aplicação.

---

## Problemas Comuns (Troubleshooting)
- **Erro de módulo não encontrado:** ambiente virtual não ativado
- **Falha de conexão com o banco:** verifique credenciais e se o SQL foi executado
- **Páginas não carregam:** confirme a estrutura das pastas `templates/` e `static/`

---
# Licença

Este projeto é licenciado sob a [MIT License](https://github.com/tech-espm/inter-4sem-2025-volumetria-de-presenca/blob/main/LICENSE).

<p align="right">
    <a href="https://www.espm.br/cursos-de-graduacao/sistemas-de-informacao/"><img src="https://raw.githubusercontent.com/tech-espm/misc-template/main/logo-si-512.png" alt="Sistemas de Informação ESPM" style="width: 375px;"/></a>
</p>
