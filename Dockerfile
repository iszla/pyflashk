FROM python:3.8-slim-buster

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ARG FLASK_ENV=development

EXPOSE 5000

ENTRYPOINT ["python"]

CMD ["app.py"]
