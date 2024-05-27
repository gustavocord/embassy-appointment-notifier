# Proyecto de Automatización con Selenium y envio de notificación por Telegram

Este proyecto utiliza Selenium para automatizar la interacción con la web de la embajada de Austria y envia una notificación a un canal de Telegram cuando se libera un cupo para una cita.

## Descripción

El script realiza las siguientes acciones:

1. Abre el sitio web de citas para la embajada.
2. Realiza una serie de clics para navegar a través de los formularios.
3. Verifica si hay disponibilidad de citas.
4. Envía una notificación a un canal de Telegram si hay una cita disponible.

## Tecnologías Utilizadas

- Python
- Selenium
- BeautifulSoup
- Telegram Bot API
- Docker

## Prerrequisitos

Antes de ejecutar el proyecto, asegúrate de tener instalados los siguientes requisitos:

- Docker
- Python

## Variables de Entorno

El proyecto requiere las siguientes variables de entorno:

- `TELEGRAM_BOT_TOKEN`: El token del bot de Telegram.
- `TELEGRAM_CHANNEL_USERNAME`: El nombre de usuario del canal de Telegram.

## Configuración

1. Clona este repositorio en tu máquina local.
2. Crea un archivo `.env` en el directorio raíz del proyecto y añade las variables de entorno mencionadas anteriormente:

    ```env
    TELEGRAM_BOT_TOKEN=tu_token_de_telegram
    TELEGRAM_CHANNEL_USERNAME=tu_usuario_del_canal
    ```

## Dockerización

### Dockerfile

Tu archivo `Dockerfile` se verá de la siguiente manera:

    ```Dockerfile
    FROM python:3.11

    RUN apt-get update && apt-get install -y wget gnupg
    RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add -
    RUN sh -c 'echo "deb [arch=amd64] https://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
    RUN apt-get update && apt-get install -y google-chrome-stable

    RUN wget -N https://storage.googleapis.com/chrome-for-testing-public/125.0.6422.78/linux64/chrome-linux64.zip && \
        unzip chrome-linux64.zip && \
        rm chrome-linux64.zip && \
        mv chrome-linux64 /usr/local/bin/chromedriver

    WORKDIR /app

    COPY requirements.txt requirements.txt
    RUN pip install --no-cache-dir -r requirements.txt

    COPY . .

    EXPOSE 8080

    CMD ["python", "app.py"]
    ```

## Ejecución

Para ejecutar el proyecto, utiliza los siguientes comandos:

1. Construye la imagen de Docker:

    ```
    Docker build -t <nombre_imagen>
    ```

2. Inicia el contenedor:

    ```
    Docker run -t <nombre_imagen>
    ```

## Licencia

Este proyecto está licenciado bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.
