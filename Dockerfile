FROM python:3.8

COPY requirements.txt .
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5000/tcp

CMD ["python", "app.py"]