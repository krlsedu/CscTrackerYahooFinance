FROM python:3.9.18
RUN mkdir /app
ADD . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["python","-u", "app.py"]
