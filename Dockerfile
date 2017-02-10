FROM python
ADD . /app
ENTRYPOINT python /app/main.py
