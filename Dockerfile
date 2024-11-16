# Use a PyTorch base image with torch already installed
FROM pytorch/pytorch:1.9.0-cuda10.2-cudnn7-runtime

# Install Stanza
RUN pip install stanza>=1.2

#Define workdir
WORKDIR /app

# Copy dependency files and install
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

# Copie os Stanza resources
COPY stanza_resources /root/stanza_resources

# Copy the static folder (including jeni.jpg)
COPY static /app/static

# Copy the remain code
COPY . /app

# Configure the start command
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--timeout", "1200", "app:app"]
