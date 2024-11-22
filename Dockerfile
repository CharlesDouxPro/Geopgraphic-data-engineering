FROM python:3.12-slim

WORKDIR /workspace

ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install

COPY requirements.txt .

RUN python -m pip install -r requirements.txt

COPY . .

CMD ["python", "main.py", "--ref_lat", "-22.951912", "--ref_lon", "-43.210484", "--url", "https://storage.googleapis.com/open-buildings-data/v3/polygons_s2_level_4_gzip/009_buildings.csv.gz" ]