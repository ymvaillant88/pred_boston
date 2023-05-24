
FROM python:3.8-alpine
RUN mkdir /src
WORKDIR /src
ADD . /src
RUN pip install -r requirements.txt
CMD ["python", "app.py"]
EXPOSE 5000
