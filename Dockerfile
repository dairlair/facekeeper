FROM dairlair/face-recognition-docker:0.0.1

WORKDIR /facekeeper

ADD requirements.txt /facekeeper/requirements.txt
RUN pip install -r requirements.txt

ADD . /facekeeper

ENV STORAGE_DSN=postgresql://facekeeper:facekeeper@localhost:5432/facekeeper
ENV AMQP_URL=amqp://guest:guest@host.docker.internal:5672/%2F

ENV PYTHONUNBUFFERED=1

CMD ["python", "facekeeper/amqp.py"]