from selenium import webdriver

driver = webdriver.Firefox()
driver.get("https://es.wikipedia.org/wiki/Granada_Club_de_F%C3%BAtbol")
tabla = driver.find_element_by_xpath('/html/body/div[3]/div[3]/div[5]/div[1]/table[16]')

presidentes = tabla.find_elements_by_tag_name('tr')
string_csv = 'desde,hasta,nombre\n'

for i in range(1, len(presidentes)):
    valores = presidentes[i].find_elements_by_tag_name('td')
    string_csv += valores[1].text + ',' + valores[2].text + ',' + valores[3].text + '\n'

# Introducimos el csv en un archivo
csv = open('presidentes.csv', 'w')
csv.write(string_csv)
csv.close()