
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
