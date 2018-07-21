FROM python:2.7-slim
ADD . /app
WORKDIR /app
EXPOSE 5000
COPY requirements.txt /app
# Add a cronjob for running the vulnerability_scan script
RUN pip install --trusted-host pypi.python.org -r requirements.txt
COPY . /app
CMD ["python", "app.py"]
