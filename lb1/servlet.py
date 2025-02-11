from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, EmailStr, field_validator, ValidationError
import re

app = FastAPI()
templates = Jinja2Templates(directory="templates")

class UserInput(BaseModel):
    name: str
    age: int
    email: EmailStr
    phone: str

    @field_validator('name')
    def name_validator(cls, v: str) -> str:
        if not re.match(r"^[a-zA-Zа-яА-ЯёЁ\s-]+$", v):
            raise ValueError("Имя должно содержать только буквы")
        if len(v) < 2:
            raise ValueError("Имя должно быть не короче 2 символов")
        return v

    @field_validator('age')
    def age_validator(cls, v: int) -> int:
        if v < 1 or v > 120:
            raise ValueError("Возраст должен быть от 1 до 120")
        return v

    @field_validator('phone')
    def phone_validator(cls, v: str) -> str:
        cleaned_phone = re.sub(r"[ \-()]", "", v)
        if not re.match(r"^(\+7|8)\d{10}$", cleaned_phone):
            raise ValueError("Телефон должен быть в формате +7 (XXX) XXX-XX-XX или 8 (XXX) XXX-XX-XX")
        return v

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})

@app.post("/submit", response_class=HTMLResponse)
async def submit_form(request: Request, name: str = Form(...), age: int = Form(...), email: str = Form(...), phone: str = Form(...)):
    try:
        user_input = UserInput(name=name, age=age, email=email, phone=phone)
        return templates.TemplateResponse("result.html", {"request": request, "name": user_input.name, "age": user_input.age, "email": user_input.email, "phone": user_input.phone})
    except ValidationError as e:
        error_message = e.errors()[0]['msg']
        return templates.TemplateResponse("form.html", {"request": request, "error": error_message})