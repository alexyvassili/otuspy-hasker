FROM ubuntu
RUN apt-get update && apt-get install -y
RUN apt-get install make
RUN apt-get install -y git
ENV SECRET_KEY ''
ENV HASKER_DB_USER ''
ENV HASKER_DB_PASSWORD ''
