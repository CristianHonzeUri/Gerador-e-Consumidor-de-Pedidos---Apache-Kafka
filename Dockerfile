# 1. Começamos com uma imagem base oficial do Python
FROM python:3.9

# 2. Definimos o diretório de trabalho dentro do container
WORKDIR /app

# 3. Copiamos o arquivo de requisitos
COPY requirements.txt .

# 4. Instalamos as bibliotecas (kafka-python)
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copiamos todos os nossos scripts .py para dentro do container
COPY produtor_pedidos.py .
COPY servico_estoque.py .
COPY servico_pagamento.py .
COPY servico_notificacao.py .

# O comando para rodar será definido no docker-compose.yml