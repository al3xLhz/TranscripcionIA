# ──────────────────────────────────────────────
# 🧱 Etapa 1: construcción de dependencias
# ──────────────────────────────────────────────
FROM nvidia/cuda:12.8.0-runtime-ubuntu22.04 AS builder

WORKDIR /app

# Instalar Python, pip y ffmpeg
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    ffmpeg \
    && ln -sf /usr/bin/python3 /usr/bin/python && \
    ln -sf /usr/bin/pip3 /usr/bin/pip && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Instalar dependencias de Python
RUN pip install --no-cache-dir torch torchvision torchaudio \
    --index-url https://download.pytorch.org/whl/cu128 && \
    pip install --no-cache-dir openai-whisper pydub

# Copiar tu aplicación
COPY . .

# ──────────────────────────────────────────────
# ⚙️ Etapa 2: imagen final limpia (runtime)
# ──────────────────────────────────────────────
FROM nvidia/cuda:12.8.0-runtime-ubuntu22.04

WORKDIR /app

# Instalar dependencias del sistema necesarias para ffmpeg y numpy/torch
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    ffmpeg \
    libatlas-base-dev \
    && ln -sf /usr/bin/python3 /usr/bin/python && \
    ln -sf /usr/bin/pip3 /usr/bin/pip && \
    apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Copiar las librerías Python ya instaladas desde el builder
COPY --from=builder /usr/local /usr/local

# Copiar tu aplicación final
COPY . .

# Comando para mantener el contenedor vivo
CMD ["tail", "-f", "/dev/null"]
