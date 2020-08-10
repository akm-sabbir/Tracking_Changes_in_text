FROM python:buster
EXPOSE 8080
RUN mkdir -p /hcc_backend
COPY . /hcc_backend/
WORKDIR /hcc_backend
RUN pip install -r requirements.txt
CMD ["python", "run.py", "server"]