FROM selenium/standalone-chrome:4.18.0-20240220
USER root

RUN apt-get update && \
    apt-get install -y \
    python3.12 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

ENV URL=https://google.com/
ENV ESPERA_CARGA=10

CMD ["python3", "main.py"]