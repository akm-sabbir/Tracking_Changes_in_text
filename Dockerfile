FROM python:3.8-buster
EXPOSE 8080
RUN mkdir -p /hcc_backend
COPY . /hcc_backend/
WORKDIR /hcc_backend
RUN pip install -r requirements.txt
RUN python3 -m nltk.downloader punkt words
CMD ["python", "run.py", "server"]