FROM dairlair/face-recognition-docker:0.0.1

WORKDIR /facekeeper

COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt

ADD requirements.txt /facekeeper/requirements.txt
RUN pip install -r requirements.txt

ADD . /facekeeper
RUN pip install -e .

ENV STORAGE_DSN=postgresql://facekeeper:facekeeper@localhost:5432/facekeeper
ENV AMQP_URL=amqp://guest:guest@host.docker.internal:5672/%2F

ENV PYTHONUNBUFFERED=1

CMD ["python", "facekeeper/amqp.py"]