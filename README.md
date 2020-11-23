# FaceKeeper

[![codecov](https://codecov.io/gh/dairlair/facekeeper/branch/master/graph/badge.svg)](https://codecov.io/gh/dairlair/facekeeper)

The application provides ability to memorize and recognize.

## Configuration

Application accepts these environment variables:

* STORAGE_DSN The storage DSN in format: postgresql://user:password@host:port/database
* AMQP_URL The AMQP URL in format: amqp://user:password@host:port/virtual-host?option=value

## How to run docker version

```shell script
# Copy the docker environment file and put your credentials there.
cp .env.example .env
# Just a docker run with environment variables from the .env file
make run
```

## RabbitMQ

Before the start of FaceKeeper exporing you need to load the SQL dump located at `schema/postgres/init.sql` into your PostgreSQL instance.

When your database is ready you cat run application using this command:
```shell script
STORAGE_DSN="postgresql://facekeeper:facekeeper@172.28.128.1:5432/facekeeper" AMQP_URL="amqp://ia:ia@172.28.128.1:5672/iavhost" python facekeeper/amqp.py
```

### Memorize
And the publish to the RabbitMQ queue "facekeeper.memorize" this message:
```json
{"person": "Angelina Jolie", "url": "https://i.pinimg.com/originals/be/ab/f3/beabf3c712d56235cc65d91ea439aaab.jpg"}
```

When it is done FaceKeeper will publish to the queue "facekeeper.memorized" this message:
```json
{"photoId": 16, "person": "Angelina Jolie", "url": "https://example.com/1600975134709.jpg", "embeddingId": "c0bf216a-61cd-4e2e-9253-902a9827f8a1", "digest": "cd6c8de8710af54d649ca56307ee2472ecfe7ca41748f06471b071e5cbb91640", "recognizer": "recognizer-id", "embedding": [-0.06730382144451141], "success": true}
```

### Recognize
When it is done lets try to recognize Angelina Jolie with another photo.
To do that you need to publish to the RabbitMQ queue "facekeeper.recognize" this message:
```json
{"url": "https://data.whicdn.com/images/331364466/original.jpg"}
```

Finally, in the RabbitMQ queue "facekeeper.recognized" you will get this mesasge:
```json
{"url": "https://data.whicdn.com/images/331364466/original.jpg", "facekeeper": {"success": true, "data": {"person": "Angelina Jolie"}}}
```

### Locate
FaceKeeper can locate faces on the photos, just send this message to the `facekeeper.locate` queue:
```json
{"url": "https://images.unsplash.com/photo-1517486808906-6ca8b3f04846"}
```

And you will get response in the queue `facekeeper.located`:
```json
{
    "success": true,
    "faces": [
        {
            "top": 2471, 
            "right": 687, 
            "bottom": 2693, 
            "left": 464, 
            "contentBase64": "..."
        }, 
        // other faces...
    ]
}
```


Note: FaceKeeper do not modify any original content in the received messages. 
It's just add additional field to the json: the `memorizing` field with memorizing results and the `recognition` field with recognition results, obviously.
Both added fields have a format: `{sucess: boolean, data: dict}`.

# Exit codes description:

* `2` - The AMQP broker is not available through the specified URL