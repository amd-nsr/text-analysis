import uuid
import json

from fastapi import APIRouter, Depends, Header
from app.tasks import process_text
from app.core.firebase_manager import FirebaseManager
from app.core.firestore_manager import FirestoreManager
from app.core.pub_sub_app import publisher, PUBSUB_TOPIC_PATH


router = APIRouter()
firebase_manager = FirebaseManager()
firestore_manager = FirestoreManager()




def get_current_user(authorization: str = Header(...)):
    return firebase_manager.verify_token(authorization)


@router.post("/submit-text")
def submit_text(payload: dict, user=Depends(get_current_user)):
    text = payload.get("text")
    user_id = user["uid"]

    # generate deterministic task_id
    task_id = str(uuid.uuid4())

    # create Firestore doc first
    firestore_manager.create_task(user_id, task_id, text)

    # publish task to Pub/Sub
    message = json.dumps({
        "user_id": user_id,
        "text": text,
        "task_id": task_id
    }).encode("utf-8")
    publisher.publish(PUBSUB_TOPIC_PATH, message)

    return {
        "task_id": task_id,
        "status": "submitted",
        "user_id": user_id
    }

@router.post("/create-user")
def create_user(payload: dict):
    email = payload.get("email")
    password = payload.get("password")
    display_name = payload.get("display_name", "")

    user_record = firebase_manager.create_user(email, password, display_name)

    # Optionally create a Firestore user document
    firestore_manager.create_user(user_record["uid"], {
        "email": email,
        "display_name": display_name
    })

    return user_record

@router.get("/task-status/{task_id}")
def task_status(task_id: str, user=Depends(get_current_user)):
    user_id = user["uid"]
    task_doc = firestore_manager.get_task(user_id, task_id)
    if not task_doc:
        return {"error": "Task not found."}
    return task_doc

@router.get("/list-tasks")
def list_tasks(user=Depends(get_current_user)):
    user_id = user["uid"]
    tasks = firestore_manager.list_tasks(user_id)
    return {"tasks": tasks}

@router.post("/test")
def test_endpoint():
    return {"message": "Text Analysis API is running."}

