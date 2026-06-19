# Imagem oficial do Python para Django.
FROM python:3.13-slim

# Evita arquivos .pyc e garante logs sem buffer no Docker.
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Diretório de trabalho dentro do container.
WORKDIR /app

# Dependencias de sistema minimas para instalar pacotes Python.
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Instala dependencias Python antes de copiar todo o codigo para aproveitar cache.
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copia a aplicacao Django.
COPY . .

# Porta usada pelo servidor de desenvolvimento do Django.
EXPOSE 8000

# Comando padrao; o docker-compose executa migracoes antes do runserver.
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
