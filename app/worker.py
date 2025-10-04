import os
import json
import threading
from concurrent.futures import ThreadPoolExecutor
from fastapi import FastAPI
from app.core.pub_sub_app import subscriber, PUBSUB_SUBSCRIPTION_PATH
from app.tasks import process_text

app = FastAPI()

# ------------------------------
# Pub/Sub callback
# ------------------------------
def callback(message):
    try:
        data = json.loads(message.data)
        user_id = data["user_id"]
        text = data["text"]
        task_id = data["task_id"]

        # Call your existing processing function
        process_text(user_id=user_id, text=text, task_id=task_id)

        message.ack()
    except Exception as e:
        print(f"Error processing task {data.get('task_id')}: {e}")
        message.nack()

# ------------------------------
# Subscriber loop
# ------------------------------
def start_subscriber():
    print("Worker listening for Pub/Sub messages...")
    with ThreadPoolExecutor() as executor:
        streaming_pull_future = subscriber.subscribe(PUBSUB_SUBSCRIPTION_PATH, callback=callback)
        streaming_pull_future.result()  # blocks indefinitely

# Start the subscriber in a background thread
threading.Thread(target=start_subscriber, daemon=True).start()

# ------------------------------
# Health check endpoint
# ------------------------------
@app.get("/")
def health_check():
    return {"status": "worker running"}

# ------------------------------
# Entrypoint
# ------------------------------
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
