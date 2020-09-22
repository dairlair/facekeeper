# FaceKeeper

[![codecov](https://codecov.io/gh/dairlair/facekeeper/branch/master/graph/badge.svg)](https://codecov.io/gh/dairlair/facekeeper)

The application provides ability to memorize and recognize.

## How to run dev version

## RabbitMQ

Before the start of FaceKeeper exporing you need to load the SQL dump located at `schema/postgres/init.sql` into your PostgreSQL instance.

When your database is ready you cat run application using this command:
```shell script
STORAGE_DSN="postgresql://facekeeper:facekeeper@172.28.128.1:5432/facekeeper" AMQP_URL="amqp://ia:ia@172.28.128.1:5672/iavhost" python facekeeper/amqp.py
```

And the publish to the RabbitMQ queue "facekeeper.memorize" this message:
```json
{"person": "Angelina Jolie", "url": "https://i.pinimg.com/originals/be/ab/f3/beabf3c712d56235cc65d91ea439aaab.jpg"}
```

When it is done FaceKeeper will publish to the queue "facekeeper.memorized" this message:
```json
{"person": "Angelina Jolie", "url": "https://i.pinimg.com/originals/be/ab/f3/beabf3c712d56235cc65d91ea439aaab.jpg", "memorizing": {"success": true, "data": {"id": "b295b5b5-8325-4f8b-b33e-6fd582554d52", "digest": "9780859586097eea39ac14c37e644f0b9cfe66f3bb57a9d6149df300b0757323"}}}
```

When it is done lets try to recognize Angelina Jolie with another photo.
To do that you need to publish to the RabbitMQ queue "facekeeper.recognize" this message:
```json
{"url": "https://data.whicdn.com/images/331364466/original.jpg"}
```

Finally, in the RabbitMQ queue "facekeeper.recognized" you will get this mesasge:
```json
{"url": "https://data.whicdn.com/images/331364466/original.jpg", "recognition": {"success": true, "data": {"person": "Angelina Jolie"}}}
```

Note: FaceKeeper do not modify any original content in the received messages. 
It's just add additional field to the json: the `memorizing` field with memorizing results and the `recognition` field with recognition results, obviously.
Both added fields have a format: `{sucess: boolean, data: dict}`.

# Exit codes description:

* `2` - The AMQP broker is not available through the specified URL