# Localización de elementos y obtención de los datos

Los objetos se pueden localizar utilizando varios métodos:

```py
# Para localizar un solo elemento

driver.find_element_by_id()
driver.find_element_by_name()
driver.find_element_by_xpath()
driver.find_element_by_link_text()
driver.find_element_by_partial_link_text()
driver.find_element_by_tag_name()
driver.find_element_by_class_name()
driver.find_element_by_css_selector()

# Para localizar un array de elementos

driver.find_elements_by_name()
driver.find_elements_by_xpath()
driver.find_elements_by_link_text()
driver.find_elements_by_partial_link_text()
driver.find_elements_by_tag_name()
driver.find_elements_by_class_name()
driver.find_elements_by_css_selector()
```

En nuestro caso tenemos que localizar la tabla de [presidentes](https://es.wikipedia.org/wiki/Granada_Club_de_F%C3%BAtbol#Presidentes) que es donde está la información que nosotros queremos obtener. La localización de elementos puede estar anidada, es decir, puedes localizar un elemento que se encuentre dentro de otro elemento localizado previamente. 

Para facilitarnos la localización de elementos haremos uso de las herramientas de desarrollo de nuestro navegador. Si nos dirigimos hacia la tabla en el código vemos que tiene el siguiente código:

```html
<table class="wikitable">
    ...
</table>
```

Como no podemos identificarla por un id único, tendremos que localizarla de otra forma. Podríamos hacerlo obteniendo todos los elementos de la clase `wikitable`, pero esto no sería demasiado eficiente, ya que tendríamos que ver que elemento del array corresponde a esta tabla. Tenemos dos opciones principales para detectar la tabla, utilizar su selector CSS o utilizar su xpath. Gracias a las herramientas de desarrollo de nuestro navegador, ambos pueden ser obtenidos fácilmente, haciendo click derecho sobre el elementos, copiar y seleccionando _'Selector CSS'_ o _'Xpath'_:

```py
tabla = driver.find_element_by_css_selector('table.wikitable:nth-child(216)')
---------
tabla = driver.find_element_by_xpath('/html/body/div[3]/div[3]/div[5]/div[1]/table[16]')
```
Analizando como está formada la tabla,

```html
<table class="wikitable">
    <tbody>
        <tr>
            ...
        </tr>
    </tbody>
</table>
```

la información interesante está en las filas (`tr`). Nuestro objetivo será el de obtener la información correspondiente a cada una de las filas, donde está la información de cada presidente. Para esto podemos buscar todos los elementos `tr` que hay dentro de la tabla, para a partir de ahí iterar sobre ellos obteniendo la información:

```py
presidentes = tabla.find_element_by_tag_name('tr');
```

A partir de aquí tendremos un array en la variable `presidentes` con cada una de las filas de la tabla. Podremos así hacer un bucle recorriendo filas:

```py
presidentes = tabla.find_elements_by_tag_name('tr')
for p in presidentes:
    print(p.text)
```

Esto nos imprimiría todas las filas de la tabla en cuestión. Al iterar sobre todas las filas también nos imprime la fila de títulos. Para evitar esto, podemos iterar a partir de las segunda fila:

```py
presidentes = tabla.find_elements_by_tag_name('tr')
for i in range(1, len(presidentes)):
    print(presidentes[i].text)
```

A partir de aquí ya podemos iterar sobre todos los presidentes. Si miramos las columnas de la tabla, nos interesan las columnas segunda, tercera y cuarta. Básicamente lo que haremos será obtener todos los elementos `td` de cada fila y a partir de ahí coger los que nos interesan. Introduciremos estos datos en un archivo `.csv`, formato abierto que nos permitirá trabajar :

```py
valores = presidentes[i].find_elements_by_tag_name('td')
string_csv += valores[1].text + ',' + valores[2].text + ',' + valores[3].text + '\n'
```
