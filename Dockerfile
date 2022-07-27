FROM python:3.8-buster
EXPOSE 8080
ARG USERNAME
ARG TOKEN
RUN mkdir -p /hcc_backend
WORKDIR /hcc_backend
ADD requirements.txt /hcc_backend/
RUN sed -i -e "s/bitbucket.org/$USERNAME:$TOKEN@bitbucket.org/g" requirements.txt
RUN pip install -r requirements.txt
RUN python3 -m nltk.downloader punkt words
ADD . /hcc_backend/
CMD ["python", "run.py", "server"]
