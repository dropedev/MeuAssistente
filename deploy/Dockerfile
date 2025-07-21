# Dockerfile para o Assistente Virtual E-commerce

FROM python:3.11-slim

# Definir diretório de trabalho
WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copiar arquivos de dependências
COPY deploy/requirements.txt .

# Instalar dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código fonte
COPY src/ ./src/
COPY data/ ./data/
COPY .env .

# Expor porta
EXPOSE 5000

# Definir variáveis de ambiente
ENV PYTHONPATH=/app
ENV API_HOST=0.0.0.0
ENV API_PORT=5000

# Comando para iniciar a aplicação
CMD ["python", "src/api.py"]

