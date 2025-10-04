from fastapi import HTTPException, status
from typing import Optional, Dict
from app.core.firebase_app import firebase_auth


class FirebaseManager:
    def __init__(self):
        self.auth = firebase_auth

    # ------------------------
    # Auth / Token Operations
    # ------------------------
    def verify_token(self, authorization: str) -> Dict:
        """
        Verify Firebase ID token from Authorization header.
        """
        if not authorization or not authorization.startswith("Bearer "):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing or invalid token")

        id_token = authorization.split(" ")[1]

        try:
            decoded_token = self.auth.verify_id_token(id_token)
            return decoded_token  # { uid, email, name, ... }
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid or expired token: {str(e)}")

    # ------------------------
    # User Management
    # ------------------------
    def get_user(self, uid: str) -> Optional[Dict]:
        """Get Firebase user by UID."""
        try:
            user = self.auth.get_user(uid)
            return {"uid": user.uid, "email": user.email, "display_name": user.display_name}
        except Exception:
            return None

    def create_user(self, email: str, password: str, display_name: Optional[str] = None) -> Dict:
        """Create a new Firebase user."""
        user = self.auth.create_user(email=email, password=password, display_name=display_name)
        return {"uid": user.uid, "email": user.email, "display_name": user.display_name}

    def delete_user(self, uid: str) -> None:
        """Delete a Firebase user."""
        self.auth.delete_user(uid)

    def update_user(self, uid: str, **kwargs) -> Dict:
        """Update a Firebase user (email, password, display_name, etc.)."""
        user = self.auth.update_user(uid, **kwargs)
        return {"uid": user.uid, "email": user.email, "display_name": user.display_name}
