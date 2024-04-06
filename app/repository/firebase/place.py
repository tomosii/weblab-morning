from app.repository.firebase.firestore import db
from app.models.place import Place


class PlaceRepository:
    def __init__(self):
        self.collection = db.collection("places")

    def get_enabled_places(self):
        docs = self.collection.where("enabled", "==", True).stream()
        places = [Place.from_dict(doc.to_dict()) for doc in docs]
        print(f"[Firestore] Get {len(places)} places.")
        return places
