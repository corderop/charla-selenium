# Interacción con la página y esperas

Para introducir unos últimos conceptos, vamos a realizar un ejemplo, extrayendo información de reddit. Utilizaremos reddit ya que carga diferentes módulos de la página de forma asíncrona, en lugar de cargar un archivo HTML único, como ocurre con la wikipedia. Esto nos permitirá introducir conceptos como los `wait` y la interacción con las páginas.

Nuestro objetivo va a ser realizar una búsqueda en el propio buscador de reddit y obtener una lista de post de las últimas 24 horas. Para comenzar, lo único que tendremos que hacer es obtener la página de reddit y localizar su barra de búsqueda:

```py
driver.get('https://www.reddit.com/')

input_busqueda = driver.find_element_by_id('header-search-bar');
input_busqueda.send_keys('bitcoin')
```

## Pulsación de teclas físicas

Una vez introducido el texto en la barra de búsqueda, solo nos faltaría pulsar el botón de `ENTER` para enviar el texto. Para esto necesitaremos el uso del módulo `Keys` de selenium. Este nos permitirá simular la pulsación de cualquier tecla, en nuestro caso un ejemplo de uso sería el siguiente:

```py
from selenium.webdriver.common.keys import Keys

driver.get('https://www.reddit.com/')

input_busqueda = driver.find_element_by_id('header-search-bar');
input_busqueda.send_keys('bitcoin')
input_busqueda.send_keys(Keys.ENTER)
```

_Todas las teclas físicas que se pueden emular pueden verse en la [documentación oficial de selenium](https://www.selenium.dev/selenium/docs/api/py/webdriver/selenium.webdriver.common.keys.html)_

## Opciones del navegador en la ejecución del webdriver

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

## Esperas 

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

