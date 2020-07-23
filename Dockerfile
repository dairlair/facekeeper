FROM dairlair/face-recognition-docker:0.0.1

WORKDIR /facekeeper

ADD . /facekeeper

RUN pip install -r requirements.txt

ENV MONGODB_HOST=host.docker.internal
ENV PYTHONUNBUFFERED=1

CMD ["python", "facekeeper/app.py"]