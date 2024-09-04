FROM python:3.12

RUN echo "deb http://deb.debian.org/debian bullseye main" > /etc/apt/sources.list.d/bullseye.list

RUN apt-get update && apt-get install -y wget unzip openjdk-17-jdk && \
    rm -rf /var/lib/apt/lists/*

RUN wget -qO allure-commandline.zip https://github.com/allure-framework/allure2/releases/download/2.20.0/allure-2.20.0.zip && \
    unzip allure-commandline.zip -d /opt/ && \
    ln -sf /opt/allure-2.20.0/bin/allure /usr/local/bin/allure && \
    rm allure-commandline.zip

WORKDIR /app
COPY requirements.txt .
RUN python3 -m venv venv && \
    venv/bin/pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["bash", "-c", "venv/bin/pytest -v -s --alluredir reports && allure generate reports --clean -o allure-report && allure serve allure-report"]
