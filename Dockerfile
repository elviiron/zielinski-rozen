FROM joyzoursky/python-chromedriver

COPY requirements.txt .
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

RUN /bin/sh -c python parser.py

EXPOSE 5000/tcp

CMD ["python", "app.py"]