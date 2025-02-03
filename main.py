import os
from pathlib import Path
from dotenv import load_dotenv
import time
from selenium import webdriver
from selenium.common.exceptions import WebDriverException, TimeoutException
from selenium.webdriver.common.by import By


BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(os.path.join(BASE_DIR, '.env'))
NAVEGADOR = 'chrome'
URL = os.getenv("URL")
print(URL)
ESPERA_CARGA =  int(os.getenv("ESPERA_CARGA"))  or 10


def inicializar_driver(navegador):
    try:
        if navegador.lower() == 'chrome':
            from selenium.webdriver.chrome.options import Options
            from selenium.webdriver.chrome.service import Service  # <-- Añade esto
            from webdriver_manager.chrome import ChromeDriverManager

            opciones = Options()
            opciones.add_argument('--headless')
            opciones.add_argument('--no-sandbox')
            opciones.add_argument('--disable-dev-shm-usage')
            opciones.add_argument('--disable-gpu')
            opciones.add_argument('--window-size=1920,1080')

            # Versión corregida usando Service
            service = Service(ChromeDriverManager().install())  # <-- Cambio clave
            driver = webdriver.Chrome(service=service, options=opciones)  # <-- Sin executable_path
            return driver
    except WebDriverException as e:
        print(f"Error al inicializar el WebDriver: {e}")
    return None


def es_pagina_error(driver):
    try:
        contenido = driver.page_source.lower()
        if "cloudflare" in contenido or "access denied" in contenido or "error" in contenido:
            return False
        return False
    except Exception as e:
        print(f"Error al verificar la página: {e}")
        return False


def main():
    while True:
        driver = inicializar_driver(NAVEGADOR)
        if not driver:
            print("No se pudo iniciar el navegador. Saliendo del programa.")
            break

        try:
            driver.get(URL)
            print(f"Navegando a {URL}...")

            tiempo_inicial = time.time()
            cargado_correctamente = False

            while True:
                if es_pagina_error(driver):
                    print("Se ha detectado una página de error. Deteniendo el ciclo.")
                    driver.quit()
                    return

                if time.time() - tiempo_inicial > ESPERA_CARGA:
                    cargado_correctamente = True
                    break

                time.sleep(5)

            if cargado_correctamente:
                print(f"Sitio cargado correctamente. Esperando {ESPERA_CARGA} segundos.")
                time.sleep(ESPERA_CARGA)

        except TimeoutException:
            print("Tiempo de espera agotado mientras se cargaba la página.")
        except WebDriverException as e:
            print(f"Ocurrió un error con el WebDriver: {e}")
        except Exception as e:
            print(f"Se produjo un error inesperado: {e}")
        finally:
            try:
                driver.quit()
                print("Navegador cerrado.")
            except Exception as e:
                print(f"Error al cerrar el navegador: {e}")

        print("Reiniciando el ciclo...\n")


if __name__ == "__main__":
    main()