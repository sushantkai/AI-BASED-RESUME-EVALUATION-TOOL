from sqlalchemy.orm import Session

from app.models.ai_data import AIData


class AIDataRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, entity_type: str, entity_id: int, data_type: str, content: str) -> AIData:
        row = AIData(entity_type=entity_type, entity_id=entity_id, data_type=data_type, content=content)
        self.db.add(row)
        self.db.commit()
        self.db.refresh(row)
        return row

