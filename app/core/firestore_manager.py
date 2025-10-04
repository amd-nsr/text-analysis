from typing import Optional, Dict, Any, List
from app.core.firebase_app import firebase_db


class FirestoreManager:
    def __init__(self):
        self.db = firebase_db

    # ------------------------
    # Task Operations
    # ------------------------
    def create_task(self, user_id: str, task_id: str, text: str, status: str = "submitted") -> None:
        """
        Create a task document under user.
        """
        doc_ref = self.db.collection("users").document(user_id).collection("tasks").document(task_id)
        doc_ref.set({
            "task_id": task_id,
            "text": text,
            "status": status,
        })

    def update_task(self, user_id: str, task_id: str, updates: Dict[str, Any]) -> None:
        """
        Update an existing task document.
        """
        doc_ref = self.db.collection("users").document(user_id).collection("tasks").document(task_id)
        doc_ref.update(updates)

    def get_task(self, user_id: str, task_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a single task document.
        """
        doc_ref = self.db.collection("users").document(user_id).collection("tasks").document(task_id)
        doc = doc_ref.get()
        return doc.to_dict() if doc.exists else None

    def delete_task(self, user_id: str, task_id: str) -> None:
        """
        Delete a task document.
        """
        doc_ref = self.db.collection("users").document(user_id).collection("tasks").document(task_id)
        doc_ref.delete()

    def list_tasks(self, user_id: str) -> List[Dict[str, Any]]:
        """
        List all tasks for a user.
        """
        tasks_ref = self.db.collection("users").document(user_id).collection("tasks")
        return [doc.to_dict() for doc in tasks_ref.stream()]

    # ------------------------
    # User-Level Operations
    # ------------------------
    def create_user(self, user_id: str, data: Dict[str, Any]) -> None:
        """
        Create or overwrite a user document.
        """
        doc_ref = self.db.collection("users").document(user_id)
        doc_ref.set(data)

    def get_user(self, user_id: str) -> Optional[Dict[str, Any]]:
        """
        Get user document.
        """
        doc_ref = self.db.collection("users").document(user_id)
        doc = doc_ref.get()
        return doc.to_dict() if doc.exists else None

    def update_user(self, user_id: str, updates: Dict[str, Any]) -> None:
        """
        Update fields in a user document.
        """
        doc_ref = self.db.collection("users").document(user_id)
        doc_ref.update(updates)

    def delete_user(self, user_id: str) -> None:
        """
        Delete a user document (and optionally tasks).
        """
        # Delete main doc
        doc_ref = self.db.collection("users").document(user_id)
        doc_ref.delete()
        # TODO: If you want, also delete subcollection tasks here
