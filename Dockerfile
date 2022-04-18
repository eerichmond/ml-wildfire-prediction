FROM python:3.9.12-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV ENVIRONMENT prod

RUN mkdir -p /home/app
RUN addgroup --system app && adduser --system --group app
ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME
WORKDIR $APP_HOME

RUN apt-get update && \
    apt-get -y install netcat gcc && \
    apt-get clean

RUN pip install --upgrade pip
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ app/

RUN chown -R app:app $APP_HOME

USER app

EXPOSE 8000

ENTRYPOINT ["uvicorn", "app.main:app", "--host=0.0.0.0"]
