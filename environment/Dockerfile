FROM python:3.13-slim-bookworm

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
build-essential \
git \
curl \
ca-certificates \
libopenblas-dev \
&& rm -rf /var/lib/apt/lists/*

# pinned per submission policy; verify these versions exist on PyPI at submit time
RUN pip install --no-cache-dir \
numpy==2.3.2 \
scipy==1.16.1 \
pyscf==2.9.0 \
pyqmc==0.5.0

RUN mkdir -p /app/output /app/work
WORKDIR /app
