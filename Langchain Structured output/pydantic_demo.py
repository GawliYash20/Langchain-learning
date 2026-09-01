from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Annotated

class Student(BaseModel):
    name: str = 'nitish'
    age: Optional[int] = None
    email: EmailStr
    cgpa: Annotated[int, Field(gt=0, lt=10, default=5, description='A decimal value representing the cgpa of the student')]

new_student = {'age':32, 'email': 'abc@gmail.com', 'cgpa': 5}

student = Student(**new_student)

# student = dict(student)
# print(student['age'])

student = student.model_dump_json()
print(student)