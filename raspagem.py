import sys
import time
import banco as b
from config import link1, link2, tipos
from random import uniform
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

tgcCinit = {
    "WHT": [50118, "white-flare"],
    "MEG": [51065, "mega-evolution"],
    "MEW": [42370, "scarlet-and-violet-151"],
    "PRE": [47035, "prismatic-evolutions"],
    "JTG": [47913, "journey-together"],
    "BLK": [49946, "black-bolt"],
    }

# colecoes = ["MEG", "MEW", "PRE", "JTG", "BLK", "WHT"]
colecoes = ["WHT"]

objetao = {
    "WHT": [],
    "MEG": [],
    "MEW": [],
    "PRE": [],
    "JTG": [],
    "BLK": []
}

driver = webdriver.Chrome()

def inserir():
    driver.close()
    for i in colecoes:
        for j in objetao[i]:
            carta = j[0]
            listaAnun = j[1]
                
            TpCId = b.obterIdTpCarta(carta["tipoCarta"])
            if not TpCId:
                b.inserirTpCarta(carta["tipoCarta"])
                TpCId = b.obterIdTpCarta(carta["tipoCarta"])
            
            CltId = b.obterIdColecao(i)
            if (carta["tipoCarta"].split())[0] == "Energy":
                if carta["nome"] == "Energia de Prisma" or carta["nome"] == "Energia de Ignição":
                    ElmId = b.obterIdElemento("Normal")
                elif len(carta["nome"].split()) > 2:
                    ElmId = b.obterIdElemento((carta["nome"].split())[-4])
                else:
                    ElmId = b.obterIdElemento((carta["nome"].split())[-1])
                b.inserirEnergia(carta["nome"], carta["img"], CltId, TpCId, ElmId)
            else:
                artId = b.obterIdArtista(carta["artista"])
                if not artId:
                    b.inserirArtista(carta["artista"])
                    artId = b.obterIdArtista(carta["artista"])
                if (carta["tipoCarta"].split())[0] == "Pokémon":
                    ElmId = b.obterIdElemento(carta["elemento"])
                    b.inserirCarta(carta["nome"], carta["hp"], carta["img"], CltId, ElmId, TpCId, artId)
                else:
                    b.inserirCartaT(carta["nome"], carta["img"], CltId, TpCId, artId)
            
            
            CrdId = b.obterIdCarta(carta["nome"])
            
            for a in listaAnun:
                
                LojId = b.obterIdLoja(a["nomeLoja"])
                if not LojId:
                    b.inserirLoja(a["nomeLoja"])
                    LojId = b.obterIdLoja(a["nomeLoja"])
                
                TpFId = b.obterIdTpFoil(a["foilType"])
                if not TpFId:
                    b.inserirTpFoil(a["foilType"])
                    TpFId = b.obterIdTpFoil(a["foilType"])
                    
                b.inserirAnuncio(a["valor"], LojId, CrdId, TpFId)

def carta():
    for i in colecoes:
        for j in objetao[i]:
            carta = j[0]
            if (carta["nome"].split())[0] == "Energia":
                continue
            driver.get(link2 + str(tgcCinit[i][0]+int(carta["id"])-1)+"/"+ carta["nome"]+"-"+str(tgcCinit[i][1]) +"-"+str(carta["id"])+"-"+carta["indexColecao"])
            
            divsDetail = WebDriverWait(driver, 20).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div[class="card-info-footer-item"]'))
                )
            
            art = 0
            for div in divsDetail:
                title = (div.find_element(By.CSS_SELECTOR, 'div[class="card-info-footer-item-title"]')).text
                if title == "Illustrators":
                    art = 1
                    carta["artista"] = (div.find_element(By.TAG_NAME, "span")).text
            if not art:
                carta["artista"] = ""
            
            if (carta["tipoCarta"].split())[0] == "Pokémon":
                divaux = WebDriverWait(driver, 20).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div[id="card-info-title-container-meta"] > a'))
                )
                
                hp = (divaux[0].find_elements(By.TAG_NAME, "span"))[1].text
                elemento = (divaux[1].find_element(By.TAG_NAME, "img")).get_attribute("src")
                
                carta["elemento"] = tipos[elemento]
                carta["hp"] = hp

def anuncios():

    for i in colecoes:
        for j in objetao[i]:
            
            driver.get(j[0]["link"])
            
            try:
                loadmore = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[id="marketplace-stores-loadmore"]'))
                )
            
                loadmore.click()
            except:
                loadmore = 0
            
            indexColecao = (WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div[class="item-name"]'))
            ).text)

            indexColecao = indexColecao[-4:-1]
                        
            val_min = j[0]["valMin"]
            val_max = j[0]["valMax"]
            
            namesloja = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div[class="container-header"] > div[class="store-name"] > span'))
            )
            
            tipoCarta = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div[class="container-details-item"]  div[class="container-details"] > span'))
            )
            
            aux = tipoCarta[len(tipoCarta)-1].text
            if aux == "":
                aux = tipoCarta[len(tipoCarta)-1].get_attribute("innerText")
            
            print(j[0]["nome"])
            print(aux)
            j[0]["indexColecao"] = indexColecao
            j[0]["tipoCarta"] = aux
            
            for k in namesloja:
                val =  round(uniform(val_min, val_max),2)
                
                if val == val_max:
                    foil = "Masterball Foil"
                elif val > val_max * 0.85:
                    foil = "Pokeball Foil"
                elif val > val_max * 0.625:
                    foil = "Reverse Foil"
                elif val > val_max * 0.38:
                    foil = "Foil"
                else:
                    foil = "Normal"
                
                j[1].append({
                    "nomeLoja": k.get_attribute("innerText"),
                    "foilType": foil,
                    "valor": val,
                })

def tabela(tab, i, imgs):
    linhas = tab.find_elements(By.TAG_NAME, 'tr')

    for j in range(len(linhas)):
        linha = linhas[j]
        img = imgs[j].get_attribute("data-src")
        link = linha.find_element(By.TAG_NAME, 'a').get_attribute("href")
        colunas = linha.find_elements(By.TAG_NAME, 'td')
        
        _, valMin =  colunas[4].text.split()
        _, valMax =  colunas[5].text.split()
        
        valMin = str(valMin).replace(".", "")
        valMin = str(valMin).replace(",", ".")
        valMax = str(valMax).replace(".", "")
        valMax = str(valMax).replace(",", ".")
        
        valMin = float(valMin)
        valMax = float(valMax)
        
        objetao[i].append(({"id": colunas[0].text, "nome": colunas[1].text, "link": link, "img": img, "valMin": valMin, "valMax": valMax}, []))

def colecao():
    for i in colecoes:
        driver.get(link1+i)
        if i == "MEG":
            btCu = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[class="lgpd-button"] > button'))
            )
            btCu.click()
            
            
        btLista = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[class="order-btns-list tb-view-02"]'))
        )
        
        btLista.click()
        
        tab = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'div.card-table table > tbody'))
        )
        
        imgs = WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div[class="stickyimgs"] img'))
        )
        
        tabela(tab, i, imgs)

colecao()
anuncios()
carta()
inserir()