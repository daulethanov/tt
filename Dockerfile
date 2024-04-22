FROM python:3.10

WORKDIR /backend

COPY req.txt ./
RUN pip install -r req.txt

COPY . .

CMD ["gunicorn", "--bind", "127.0.0.1:8000", "base.wsgi:application"]

