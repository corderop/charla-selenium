from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
import time

options = Options()
options.set_preference('dom.webnotifications.enabled', False)
# options.add_argument('-headless')

def obtener_posts(driver, tema):
    
    start = time.time()
    
    driver.get("https://www.reddit.com/")

    # Búsqueda
    try:
        busqueda = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "header-search-bar"))
        )
    except:
        driver.quit()
        exit()
    finally:
        busqueda.send_keys(tema)
        busqueda.send_keys(Keys.ENTER)

    # Carga de las noticias de una semana
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

    # Obtención de los posts
    try:
        posts = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "SQnoC3ObvgnGjWt90zD9Z"))
        )
    except:
        driver.quit()
        exit()
    finally:
        for p in posts:
            print(p.text + ',' + p.get_attribute('href'))

    end = time.time()
    print(end-start)                

driver = webdriver.Firefox(options=options)
obtener_posts(driver, 'bitcoin')

