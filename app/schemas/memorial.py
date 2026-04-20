from typing import List, Optional
from pydantic import BaseModel


class MemorialItemOut(BaseModel):
    title: str
    subtitle: Optional[str] = None
    detail: Optional[str] = None
    status: Optional[str] = None  # "達成間近" / "達成" / "記録" など


class MemorialSectionOut(BaseModel):
    title: str
    items: List[MemorialItemOut]


class MemorialResponseOut(BaseModel):
    source: str  # "jra" or "nankan"
    source_label: str
    source_url: str
    as_of_text: Optional[str] = None
    sections: List[MemorialSectionOut]