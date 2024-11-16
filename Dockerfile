# Use uma imagem base de PyTorch, que já vem com torch instalado
FROM pytorch/pytorch:1.9.0-cuda10.2-cudnn7-runtime

# Atualize o pip e instale o stanza
RUN pip install stanza>=1.2

# Defina o diretório de trabalho
WORKDIR /app

# Copie o arquivo de dependências e instale as outras dependências
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

# Copie os modelos do Stanza para evitar downloads
COPY stanza_resources /root/stanza_resources

# Copy the static folder (including jeni.jpg)
COPY static /app/static

# Copie o restante do código
COPY . /app

# Configure o comando de inicialização
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--timeout", "1200", "app:app"]
