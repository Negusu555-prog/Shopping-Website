FROM python:3.9

RUN apt-get update && apt-get install -y supervisor

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r req.txt

COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

CMD ["supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
