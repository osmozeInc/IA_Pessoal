# Utiliza a imagem oficial do Python 3.11
FROM python:3.11-slim

# Instala dependências do sistema para compilação e reprodução de áudio
RUN apt-get update && apt-get install -y \
    build-essential \
    libsndfile1 \
    alsa-utils \
    portaudio19-dev \
    && rm -rf /var/lib/apt/lists/*

# Define o diretório de trabalho
WORKDIR /app

# Copia e instala as dependências do Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código-fonte da aplicação
COPY nlp_core.py .

# Copia a pasta do modelo acústico para o diretório de trabalho do contêiner
COPY modelo_vosk ./modelo_vosk

# Comando de execução
CMD ["python", "nlp_core.py"]