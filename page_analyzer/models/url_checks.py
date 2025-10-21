from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class UrlChecks:
    id: int
    url_id: int
    created_at: datetime
    status_code: Optional[int] = None
    h1: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
