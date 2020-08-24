## How to run dev version

## Daparizations
Facekeep is a darp-compatible application. The application is ready to listed two topics (`memorize` and `recognize`) using the Dapr pub-sub functionalite and process events from these topics along with pushing results in to the Dapr topics.

The app provides endpoint `dapr/subscribe` which returns list of events and their REST handler.

When you run the application you can pass following Dapr settings:

```
# Set DARP_URL=http://localhost:3500/v1.0 to to activate Dapr integration
DAPR_URL="" # Is empty by default. When it is empty application will not push any events to the Dapr endpoint.
DAPR_PUBSUB=pubsub # Just a dapr pubsub name
DAPR_TOPIC_MEMORIZE_IN=Memorize # This topic is used to get photos to memorize persons from them
DAPR_TOPIC_MEMORIZE_OUT=Memorized # This topic used for publishing success responses from `memorize` operation
DAPR_TOPIC_RECOGNIZE_IN=Recognize # This topic is used to get photos for recognition
DAPR_TOPIC_RECOGNIZE_OUT=Recognized # This topic is used to publish recognition results
```

### Run locally as a Darp app
Just run

```
DAPR_URL="http://localhost:3500/v1.0" PORT=3001 dapr run --app-id facekeeper --dapr-http-port 3500 --app-port 3001 python facekeeper/app.py
```

Send photos for recognize:
```
dapr publish --pubsub=pubsub --topic "Recognize" --data '{"images": ["https://m.media-amazon.com/images/M/MV5BODg3MzYwMjE4N15BMl5BanBnXkFtZTcwMjU5NzAzNw@@._V1_.jpg"]}'
# or
http POST http://localhost:3500/v1.0/publish/pubsub/Recognize '{"url": "https://m.media-amazon.com/images/M/MV5BODg3MzYwMjE4N15BMl5BanBnXkFtZTcwMjU5NzAzNw@@._V1_.jpg"}'
```

Once the FaceKeeper received this message it will process it and push original data with added field `recognized` to the recognized topic in format:
```json
{   
    "images": ...
    "recognition": {<url>: {'person': <person>}}
}
```