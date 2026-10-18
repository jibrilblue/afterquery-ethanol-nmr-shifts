FROM python:3.10-slim

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends build-essential cmake git libhdf5-dev libxc-dev && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

RUN mkdir -p /app/output /app/data

# Isoprene coordinates
RUN cat << 'EOF' > /app/data/isoprene.xyz
13
Isoprene
C 0.000 0.000 0.000
C 0.000 0.000 1.340
C 1.460 0.000 -0.460
C 1.460 0.000 -1.800
C -1.450 0.000 1.700
H -0.930 0.000 -0.380
H -0.930 0.000 1.710
H 1.100 0.880 -1.960
H 1.100 -0.880 -1.960
H 2.490 0.000 -0.100
H 2.490 0.000 -2.100
H -1.200 0.880 1.400
H -1.200 -0.880 1.400
H -2.490 0.000 1.700
EOF
