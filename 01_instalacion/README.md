# Instalación de selenium con pip

Para instalar _selenium_ para python debemos tener instalado [pip](https://pip.pypa.io/en/stable/installing/). Ejecutaremos el siguiente comando:

```bash
pip install selenium
```

Una vez hemos instalado selenium, tenemos que descargar un driver, según el navegador que utilicemos. En nuestro caso usaremos Firefox por lo que usaremos su [driver](https://github.com/mozilla/geckodriver/releases/), pero puedes descargar el driver para cualquier otros navegador [aquí](https://selenium-python.readthedocs.io/installation.html#drivers).

Según la distribución de linux, podrás usar diferentes comandos para instalar el driver:

```bash
# Ubuntu
sudo apt-get install firefox-geckodriver
# Archlinux
sudo pacman -S geckodriver
```