from dataclasses import dataclass
from typing import List, Optional


@dataclass
class UserContext:
    user_id: str
    start_location: int
    end_location: int
    preference: str
    avoid: List[str]
    flexibility: str
    budget: Optional[float] = None


