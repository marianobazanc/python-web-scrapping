import requests
from selenium import webdriver
from bs4 import BeautifulSoup

page_number = 1
inmueble = {}

while True:
    if page_number > 3:
        break
    r = requests.get(f"http://www.zonaprop.com.ar/departamentos-alquiler-nueva-cordoba-pagina-{page_number}.html", headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/113.0'})
    print(f"http://www.zonaprop.com.ar/departamentos-alquiler-nueva-cordoba-pagina-{page_number}.html")
    soup = BeautifulSoup(r.content,'html.parser')

    titulos = soup.find_all('a', attrs={"class": "sc-i1odl-11 kptTyQ"})
    titulos = [i.text for i in titulos]

    enlaces = soup.find_all('div', attrs={'data-qa': 'posting PROPERTY'})
    enlaces = [i.get('data-to-posting') for i in enlaces]

    ubicacion = soup.find_all('div', attrs={'data-qa': 'POSTING_CARD_LOCATION'})
    ubicacion = [i.text for i in ubicacion]

    precios = soup.find_all('div', attrs={'data-qa': 'POSTING_CARD_PRICE'})
    precios = [i.text for i in precios]

    dormitorios = []
    ambientes = []
    next_page_link = soup.find('a', {'data-qa': 'PAGING_NEXT'})
    print(next_page_link)
    if not next_page_link:
        break

    page_number += 1

    for i in range(len(enlaces)):
        if i > 5:
            break

        enlace="https://www.zonaprop.com.ar" + enlaces[i]
        
        driver = webdriver.Firefox()
        driver.get(enlace)

        html = driver.page_source

        soup = BeautifulSoup(html, 'html.parser')

        element = soup.find_all('li', {'class': 'icon-feature'})
        print(element)
        keywords = ["Dormitorio", "Dormitorios"]
        dormitorio = [e.text for e in element if any(word in e.text for word in keywords)]
        if dormitorio:
            dormitorios.append(dormitorio[0].split()[0])
        else:
            dormitorios.append('0')

        keywords = ["Ambientes", "Ambiente"]
        ambiente = [e.text for e in element if any(word in e.text for word in keywords)]
        if ambiente:
            ambientes.append(ambiente[0].split()[0])
        else:
            ambientes.append('0')

        driver.quit()

    # Actualiza el diccionario inmueble con los valores correspondientes
    for i in range(len(titulos)):
        if i > 5:
            break
        inmueble[len(inmueble)] = {
            "titulo": titulos[i],
            "enlace": enlaces[i],
            "ubicacion": ubicacion[i],
            "precio": precios[i],
            "habitaciones": dormitorios[i] if i < len(dormitorios) else "N/A"
        }

# Imprime el diccionario inmueble para verificar que se haya creado correctamente
print(inmueble)

