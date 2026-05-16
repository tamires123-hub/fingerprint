FROM python:3.12-slim

# Dependências mínimas para rodar mindtct/bozorth3
RUN apt-get update && apt-get install -y \
    libjpeg62-turbo-dev \
    libpng-dev \
    libtiff-dev \
    libx11-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copiar NBIS compilado para o local correto
COPY build_nbis /opt/nbis_build

# Colocar NBIS no PATH
ENV PATH="/opt/nbis_build/bin:${PATH}"

# Copiar código da aplicação
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Criar pastas de entrada/saída
RUN mkdir -p /app/dados/img_digital /app/dados/minucias

EXPOSE 5000
CMD ["python", "extrator_api.py"]
