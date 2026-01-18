FROM python:3.12-slim
RUN groupadd -r groupdjango && useradd -r -g groupdjango userdj
ENV PYTHONBUFFERED=1

RUN pip install --upgrade pip

WORKDIR /app/www/geopints

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
USER userdj
