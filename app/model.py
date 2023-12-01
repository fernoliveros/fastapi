
from typing import Optional

from pydantic import BaseModel

class Student(BaseModel): 
    student_id: Optional[int] = None
    first_name: str
    done: Optional[bool] = False
