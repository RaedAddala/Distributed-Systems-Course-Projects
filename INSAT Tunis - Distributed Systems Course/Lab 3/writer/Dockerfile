FROM python:alpine
# install pika to access rabbitmq
RUN pip install pika
# Without this setting, Python never prints anything out.
ENV PYTHONUNBUFFERED=1
# declare the source directory
WORKDIR /usr/src/app/writer
# copy the file
COPY writer.py .
# start command
CMD [ "python", "writer.py" ]