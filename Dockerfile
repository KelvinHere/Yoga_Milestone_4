FROM python:3

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /work

RUN apt-get update && apt-get install -y netcat

# Install requirements
RUN pip3 install --upgrade pip
COPY ./requirements.txt .
RUN pip3 install -r requirements.txt

# Copy project
COPY ./work /work

# Entrypoint
COPY ./entrypoint.sh /
ENTRYPOINT ["sh", "/entrypoint.sh"]