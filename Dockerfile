FROM python:3.5
COPY requirements.txt /app/
RUN pip3 install -r /app/requirements.txt
COPY package/templates /app/templates/
COPY package/app.py /app/
WORKDIR /app/
ENTRYPOINT ["python3"]
CMD ["app.py"]

