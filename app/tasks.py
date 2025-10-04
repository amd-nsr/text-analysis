from app.core.firestore_manager import FirestoreManager
from .OpenAI.analyzers import TextAnalyzer

firestore_manager = FirestoreManager()

def process_text(user_id: str, text: str, task_id: str):
    try:
        firestore_manager.update_task(user_id, task_id, {"status": "in_progress_running"})

        print(f"Processing task {task_id} for user {user_id}")
        analysis = TextAnalyzer().analyze(text)

        print(f"Task {task_id} completed for user {user_id}")
        firestore_manager.update_task(user_id, task_id, {
            "status": "completed",
            "result": analysis.model_dump()
        })

        print("analysis:", analysis.model_dump())
        return analysis.model_dump()

    except Exception as e:
        firestore_manager.update_task(user_id, task_id, {
            "status": "failed",
            "error": str(e)
        })
        raise
