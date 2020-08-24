## How to run dev version

## Daparizations

Facekeep is a darp-compatible application. The application is ready to listed two topics (`memorize` and `recognize`) using the Dapr pub-sub functionalite and process events from these topics along with pushing results in to the Dapr topics.

The app provides endpoint `dapr/subscribe` which returns list of events and their REST handler.

When you run the application you can pass following Dapr settings:

```
DAPR_URL="" # Is empty by default. When it is empty application will not push any events to the Dapr endpoint.
DAPR_PUBSUB=pubsub # Just a dapr pubsub name
DAPR_TOPIC_MEMORIZE_IN=memorize # This topic is used to get photos to memorize persons from them
DAPR_TOPIC_MEMORIZE_OUT=memorized # This topic used for publishing success responses from `memorize` operation
DAPR_TOPIC_RECOGNIZE_IN=recognize # This topic is used to get photos for recognition
DAPR_TOPIC_RECOGNIZE_OUT=recognized # This topic is used to publish recognition results
```