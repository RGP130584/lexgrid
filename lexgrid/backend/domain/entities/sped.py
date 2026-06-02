from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class SpedRecord(BaseModel):
    register_type: str
    data: Dict[str, Any]

class SpedFile(BaseModel):
    filename: str
    file_type: str
    records: List[SpedRecord]
