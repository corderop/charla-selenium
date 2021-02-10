# Introducción

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
