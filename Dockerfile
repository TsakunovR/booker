FROM python:3.10

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python3 -m venv venv

CMD ["bash", "-c", "source venv/bin/activate && pytest -v -s --alluredir reports && allure generate reports && allure serve reports"]
