import os
import asyncio
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import telegram

# Configuración del logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("embassy_appointment.log"),
        logging.StreamHandler()
    ]
)

# Configuración de las opciones del navegador
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")

# Mensaje de notificación
NOTIFICATION_MESSAGE = "¡Se liberó un cupo para la embajada! TEST"

async def send_message_to_channel(bot_token, channel_username):
    """Envía un mensaje al canal de Telegram."""
    try:
        bot = telegram.Bot(token=bot_token)
        await bot.send_message(chat_id=channel_username, text=NOTIFICATION_MESSAGE)
        logging.info(f"Mensaje enviado al canal de Telegram: '{NOTIFICATION_MESSAGE}'")
    except Exception as e:
        logging.error(f"Error al enviar mensaje al canal de Telegram: {e}")

def click_element(driver, by, value, error_message):
    """Hace clic en un elemento especificado y maneja errores si ocurren."""
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((by, value))
        )
        element.click()
        logging.info(f"Click en elemento: {value}")
    except Exception as e:
        logging.error(f"No se pudo {error_message}: {e}")
        raise RuntimeError(f"Error crítico: no se pudo {error_message}")

def select_option(driver, by, value, option_text, error_message):
    """Selecciona una opción en un menú desplegable y maneja errores si ocurren."""
    try:
        option_xpath = f"{value}/option[text()='{option_text}']"
        click_element(driver, by, option_xpath, error_message)
        logging.info(f"Opción seleccionada: {option_text}")
    except Exception as e:
        logging.error(f"No se pudo {error_message}: {e}")

async def main():
    # Validar la presencia de los tokens de Telegram
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    channel_username = os.getenv('TELEGRAM_CHANNEL_USERNAME')

    if not bot_token or not channel_username:
        logging.error("Los tokens de Telegram no están configurados. Asegúrate de establecer TELEGRAM_BOT_TOKEN y TELEGRAM_CHANNEL_USERNAME en las variables de entorno.")
        return

    url = "https://appointment.bmeia.gv.at/"
    driver = webdriver.Chrome(options=chrome_options)

    try:
        driver.get(url)
        logging.info(f"Navegando a {url}")

        # Seleccionar opciones en los menús desplegables
        select_option(driver, By.XPATH, "//select[@id='Language']", "Español", "seleccionar la opción de idioma")
        select_option(driver, By.XPATH, "//select[@id='Office']", "BUENOS-AIRES", "seleccionar la opción de oficina")
        
        # Navegar a través del formulario
        click_element(driver, By.XPATH, "//input[@type='submit']", "hacer clic en el botón Continuar")
        select_option(driver, By.XPATH, "//select[@id='CalendarId']", "Working Holiday Programm", "seleccionar la opción 'Working Holiday Programm'")
        click_element(driver, By.XPATH, "//input[@type='submit']", "hacer clic en el botón Continuar")
        click_element(driver, By.XPATH, "//input[@type='submit']", "hacer clic en el botón Continuar")
        click_element(driver, By.XPATH, "//input[@type='submit' and @value='Continuar']", "hacer clic en el botón Continuar")
        click_element(driver, By.XPATH, "//input[@type='submit' and @value='Continuar']", "hacer clic en el botón Continuar")

        # Verificar el resultado de la interacción
        html_after_interaction = driver.page_source
        soup = BeautifulSoup(html_after_interaction, 'html.parser')
        error_message = soup.find('p', class_='message-error')
        phrase_to_check = "Actualmente no hay fechas disponibles en el horario elegido"

        if not (error_message and phrase_to_check in error_message.get_text()):
            await send_message_to_channel(bot_token, channel_username)
        else:
            logging.info("No hay fechas disponibles en el horario elegido.")

    except Exception as e:
        logging.error(f"Error durante la ejecución: {e}")

    finally:
        driver.quit()
        logging.info("Navegador cerrado.")

if __name__ == "__main__":
    asyncio.run(main())
