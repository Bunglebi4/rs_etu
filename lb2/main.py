import secrets

from fastapi import FastAPI, Form, Depends, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import RedirectResponse

from database import SessionLocal, init_db
import crud

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

init_db()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/register/")
def register_form(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.post("/register/")
def register_user(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    if crud.get_user_by_username(db, username):
        return templates.TemplateResponse("register.html", {"request": request, "error": "Пользователь уже существует!"})
    crud.create_user(db, username, crud.hash_password(password))
    return templates.TemplateResponse("index.html", {"request": request, "message": "Регистрация успешна!"})


@app.get("/login/")
def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/login/")
def login_user(
        request: Request,
        username: str = Form(...),
        password: str = Form(...),
        db: Session = Depends(get_db)
):
    user = crud.get_user_by_username(db, username)
    if user is None or not crud.verify_password(password, user.password):
        return templates.TemplateResponse("login.html",
                                          {"request": request, "error": "Неверное имя пользователя или пароль!"})

    session_token = secrets.token_hex(16)  # Генерация случайного токена

    crud.update_user_session_token(db, user.id, session_token)

    response = RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(key="session_token", value=session_token)

    return response