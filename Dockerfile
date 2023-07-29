FROM python:3.10-slim

WORKDIR ./code

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFRERED 1

COPY ./requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt --no-cache-dir

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0"]
