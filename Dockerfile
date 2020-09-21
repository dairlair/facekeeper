FROM dairlair/face-recognition-docker:0.0.1

WORKDIR /facekeeper

ADD . /facekeeper

RUN pip install -r requirements.txt

ENV MONGODB_HOST=host.docker.internal
ENV AMQP_URL=amqp://guest:guest@host.docker.internal:5672/%2F

ENV PYTHONUNBUFFERED=1

CMD ["python", "facekeeper/amqp.py"]