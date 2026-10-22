#Nome: Camila Huang      RA:10419606
#Nome: Xuanjun Jin          RA:10436456

FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
