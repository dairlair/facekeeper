## How to run dev version

## Daparizations
Facekeep is a darp-compatible application. The application is ready to listed two topics (`memorize` and `recognize`) using the Dapr pub-sub functionalite and process events from these topics along with pushing results in to the Dapr topics.

The app provides endpoint `dapr/subscribe` which returns list of events and their REST handler.

When you run the application you can pass following Dapr settings:

```
DAPR_PUBSUB=pubsub # The Dapr pubsub name
```

### Run locally as a Darp app
Just run

```
PORT=3001 dapr run --app-id facekeeper --dapr-http-port 3500 --app-port 3001 python facekeeper/app.py
```

Send photos for memorize:
```shell script
dapr publish --pubsub "pubsub" --topic "Memorize" --data '{"image": ["https://cdn1-www.comingsoon.net/assets/uploads/2020/02/3631198-fast-9.jpg", "person": "Vin Diesel"]}'
```

Send photos for recognize:
```shell script
dapr publish --pubsub "pubsub" --topic "Recognize" --data '{"images": ["https://m.media-amazon.com/images/M/MV5BODg3MzYwMjE4N15BMl5BanBnXkFtZTcwMjU5NzAzNw@@._V1_.jpg"]}'
# or
http POST http://localhost:3500/v1.0/publish/pubsub/Recognize '{"url": "https://m.media-amazon.com/images/M/MV5BODg3MzYwMjE4N15BMl5BanBnXkFtZTcwMjU5NzAzNw@@._V1_.jpg"}'
```

Once the FaceKeeper received this message it will process it and push original data with added field `recognized` to the recognized topic in format:
```json
{   
    "images": ...
    "recognition": {"<URL>": {"person": "<Person ID>"}}
}
```