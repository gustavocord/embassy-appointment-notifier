from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import telegram
import os
import asyncio

chrome_options = webdriver.ChromeOptions()

chrome_options.add_argument("--no-sandbox")

chrome_options.add_argument("--headless")

chrome_options.add_argument("--disable-gpu")


async def send_message_to_channel():
    
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

    TELEGRAM_CHANNEL_USERNAME = os.getenv('TELEGRAM_CHANNEL_USERNAME')

    notification_message = "¡Se liberó un cupo para la embajada!"

    bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)

    await bot.send_message(chat_id=TELEGRAM_CHANNEL_USERNAME, text=notification_message)

    print(f"Mensaje enviado al canal de Telegram: '{notification_message}'")

def click_element(driver, by, value, error_message):
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((by, value))
        )
        element.click()
    except Exception as e:
        print(f"No se pudo {error_message}: {e}")

async def main():

    url = "http://appointment.bmeia.gv.at"

    driver = webdriver.Chrome(options=chrome_options)

    try:
        driver.get(url)

        click_element(driver, By.XPATH, "//select[@id='Language']/option[text()='Español']", "seleccionar la opción")
    
        click_element(driver, By.XPATH, "//select[@id='Office']/option[text()='BUENOS-AIRES']", "seleccionar la opción")

        click_element(driver, By.XPATH, "//input[@type='submit']", "hacer clic en el botón Continuar")

        click_element(driver, By.XPATH, "//select[@id='CalendarId']/option[@value='11997661' and text()='Working Holiday Programm']", "seleccionar la opción 'Working Holiday Programm'")

        click_element(driver, By.XPATH, "//input[@type='submit']", "hacer clic en el botón Continuar")

        click_element(driver, By.XPATH, "//input[@type='submit']", "hacer clic en el botón Continuar")
  
        click_element(driver, By.XPATH, "//input[@type='submit' and @value='Continuar']", "hacer clic en el botón Continuar")
 
        click_element(driver, By.XPATH, "//input[@type='submit' and @value='Continuar']", "hacer clic en el botón Continuar")

        html_after_interaction = driver.page_source

        soup = BeautifulSoup(html_after_interaction, 'html.parser')

        error_message = soup.find('p', class_='message-error')

        phrase_to_check = "Actualmente no hay fechas disponibles en el horario elegido"

        if  not(error_message and phrase_to_check in error_message.get_text()):
            await send_message_to_channel()

    finally:

        driver.quit()

if __name__ == "__main__":
    asyncio.run(main())