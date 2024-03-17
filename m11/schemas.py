from datetime import date
from pydantic import BaseModel, Field



class ContactsIn(BaseModel):
    first_name: str = Field(max_length=50)
    last_name: str = Field(max_length=50)
    email: str
    phone_number: str = Field(max_length=20)
    date_of_birth: date
    nick: str | None = None


class ContactsOut(ContactsIn):
    id: int

    class Config:
        orm_mode = True
