FROM python:3.8-buster
EXPOSE 8080
RUN mkdir -p /hcc_backend
WORKDIR /hcc_backend
ADD requirements.txt /hcc_backend/
RUN pip install -r requirements.txt
RUN python3 -m nltk.downloader punkt words
RUN pip install https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.4.0/en_core_sci_sm-0.4.0.tar.gz
ADD . /hcc_backend/
CMD ["python", "run.py", "server"]
