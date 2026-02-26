# O QUE: Usar uma imagem leve do Python como base
FROM python:3.10-slim

# ONDE: Definir a pasta onde o sistema vai morar dentro do Docker
WORKDIR /app

# FERRAMENTA: Instalar dependencias visuais que o Python precisa no Linux
RUN apt-get update && apt-get install -y \
    python3-tk \
    tk-dev \
    libx11-6 \
    && rm -rf /var/lib/apt/lists/*

# AÇÃO: Copiar o arquivo de bibliotecas para dentro
COPY requirements.txt .

# AÇÃO: Instalar as bibliotecas (pandas, customtkinter, etc)
RUN pip install --no-cache-dir -r requirements.txt

# AÇÃO: Copiar todos os seus arquivos (.py, .db, pastas de icones) para o Docker
COPY . .

# COMANDO: Comando para iniciar o seu sistema
CMD ["python", "main.py"]