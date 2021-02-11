from selenium import webdriver

driver = webdriver.Firefox()
driver.get("https://es.wikipedia.org/wiki/Granada_Club_de_F%C3%BAtbol")
tabla = driver.find_element_by_xpath('/html/body/div[3]/div[3]/div[5]/div[1]/table[16]')

presidentes = tabla.find_elements_by_tag_name('tr')

# Escribimos los títulos
csv = open('presidentes.csv', 'w')
csv.write('desde,hasta,nombre\n')
csv.close()

csv = open('presidentes.csv', 'a')
for i in range(1, len(presidentes)):
    valores = presidentes[i].find_elements_by_tag_name('td')

    # Año de inicio
    csv.write(valores[1].text + ",")
    # Año de salida
    csv.write(valores[2].text + ",")
    # Nombre del presidente
    csv.write(valores[3].text + "\n")
