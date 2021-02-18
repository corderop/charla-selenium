## Instalación de selenium con pip

Para instalar _selenium_ para python debemos tener instalado [pip](https://pip.pypa.io/en/stable/installing/). Ejecutaremos el siguiente comando:

```bash
pip install selenium
```

Una vez hemos instalado selenium, tenemos que descargar el driver correspondiente al navegador que utilicemos. En nuestro caso usaremos el de [Firefox](https://github.com/mozilla/geckodriver/releases/), pero puedes descargar el driver para cualquier otro navegador [aquí](https://selenium-python.readthedocs.io/installation.html#drivers).

Según la distribución de linux, podrás usar diferentes comandos para instalar el driver:

```bash
# Ubuntu
sudo apt-get install firefox-geckodriver
# Archlinux
sudo pacman -S geckodriver
```

## Introducción

Una vez instalado selenium y su driver correspondiente podemos empezar con el código. La primera tarea a realizar será la de obtener, a partir de un [artículo](https://es.wikipedia.org/wiki/Granada_Club_de_F%C3%BAtbol) de la Wikipedia, todos los presidentes de la historia de Granada CF. 

Partiremos del archivo `_introduccion.py` como plantilla. Inicialmente tenemos lo siguiente:

```py
from selenium import webdriver

driver = webdriver.Firefox()
driver.get("https://es.wikipedia.org/wiki/Granada_Club_de_F%C3%BAtbol")
```

Esto básicamente lo que hace es abrir una ventana de Firefox con el artículo de la wikipedia que vamos a utilizar. Lo primero que hacemos es importar el módulo de selenium dedicado a utilizar el driver del navegador que hemos instalado antes:

```py
from selenium import webdriver
```

Luego cargamos el driver de Firefox previamente instalado:

```py
driver = webdriver.Firefox()
```

Por último accedemos a la URL mediante el método `get()` donde especificamos la URL como parámetro.

```py
driver.get("https://es.wikipedia.org/wiki/Granada_Club_de_F%C3%BAtbol")
```

## Localización de elementos y obtención de los datos

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
presidentes = tabla.find_elements_by_tag_name('tr');
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

## Interacción con la página y esperas

Para introducir unos últimos conceptos, vamos a realizar un ejemplo, extrayendo información de reddit. Utilizaremos reddit ya que carga diferentes módulos de la página de forma asíncrona, en lugar de cargar un archivo HTML único, como ocurre con la wikipedia. Esto nos permitirá introducir conceptos como los `wait` y la interacción con las páginas.

Nuestro objetivo va a ser realizar una búsqueda en el propio buscador de reddit y obtener una lista de post de las últimas 24 horas. Para comenzar, lo único que tendremos que hacer es obtener la página de reddit y localizar su barra de búsqueda:

```py
driver.get('https://www.reddit.com/')

input_busqueda = driver.find_element_by_id('header-search-bar');
input_busqueda.send_keys('bitcoin')
```

### Pulsación de teclas físicas

Una vez introducido el texto en la barra de búsqueda, solo nos faltaría pulsar el botón de `ENTER` para enviar el texto. Para esto necesitaremos el uso del módulo `Keys` de selenium. Este nos permitirá simular la pulsación de cualquier tecla, en nuestro caso un ejemplo de uso sería el siguiente:

```py
from selenium.webdriver.common.keys import Keys

driver.get('https://www.reddit.com/')

input_busqueda = driver.find_element_by_id('header-search-bar');
input_busqueda.send_keys('bitcoin')
input_busqueda.send_keys(Keys.ENTER)
```

_Todas las teclas físicas que se pueden emular pueden verse en la [documentación oficial de selenium](https://www.selenium.dev/selenium/docs/api/py/webdriver/selenium.webdriver.common.keys.html)_

### Opciones del navegador en la ejecución del webdriver

Es posible que durante el proceso obtengamos errores del tipo:

```
... is not clickable at point (256,235) because another element ... obscures it
```

Esto se produce porque reddit nos envía una petición acerca de si queremos activar las notificaciones en su sitio. Esto produce que no podamos interactuar con la página porque esta notificación pasa a estar en primer plano. Esto se puede solventar fácilmente modificando las preferencias de la ventana de Firefox que iniciamos.

Si abrimos una instancia de Firefox normal y vamos a la página `about:config` podremos buscar entre las variables de configuración que este tiene. En concreto, para que no aparezcan alertas de notificación, a nosotros nos interesa la variable `dom.webnotifications.enabled`. Si la cambiásemos aquí, esto afectaría a cualquier uso del navegador. Para que podamos modificar esto al iniciar la instancia de selenium, este nos proporciona el módulo `options` para que podamos fácilmente indicar las opciones que deseamos cambiar antes de iniciarlo. Un ejemplo de uso es el siguiente:

```py
from selenium.webdriver.firefox.options import Options

options = Options()
options.set_preference('dom.webnotifications.enabled', False)

driver = webdriver.Firefox(options=options)
```

Aquí creamos un objeto de tipo `Options` al cual le indicamos que variable de configuración deseamos modificar mediante el método `set_preference`. Tras esto, debemos indicarle a la hora de crear el webdriver el objeto de opciones que queremos utilizar.

Esto permite múltiples opciones de configuración (tantas como tiene el navegador). Además permite especificar argumentos de ejecución para el navegador. Por ejemplo, si usamos Firefox, hay un argumento que puede ser muy útil para el scraping. Este es `-headless`, que nos permite ejecutar el script sin cargar la interfaz de usuario, lo que permitirá reducir el tiempo de este:

```py
options.add_argument('-headless')
```

### Esperas 

Si nos fijamos, justo después de hacer la búsqueda, los posts tardan en cargar. Esto puede provocar que si intentamos a acceder a un elemento que todavía no existe obtengamos un error. Para solventar esto, podemos indicarle a selenium que realice una espera hasta que ocurra un evento, por ejemplo en nuestro caso, que exista el elemento indicado:

```py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

try:
    diario = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.Ok_V8Hz99m2KvmtrN-eKW:nth-child(2)"))
    )
except:
    driver.quit()
    exit()
finally:
    diario.click()
    driver.find_element_by_css_selector('._2uYY-KeuYHKiwl-9aF0UiL > a:nth-child(2) > button:nth-child(1)').click()
```

En este trozo de código le estamos diciendo a selenium, que realice una espera hasta que se encuentre el elemento especificado, con un máximo de 10 segundos. Si este tiempo se sobrepasa, se lanza un excepción. `presence_of_element_located` no es el único evento con el que podemos realizar esperas, en la [documentación de selenium](https://selenium-python.readthedocs.io/waits.html#explicit-waits) se pueden encontrar todos.

