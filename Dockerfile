FROM python
RUN pip install boto3
ADD . /app
ENTRYPOINT python /app/main.py
