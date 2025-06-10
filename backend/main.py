from fastapi import FastAPI, Response, HTTPException, Request, Depends, status
from pydantic import BaseModel
import uvicorn
from typing import Optional
from uuid import uuid4
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

sessions: dict[str, str] = {}  # session_id -> username

class User(BaseModel):
    username: str
    password: str # always store a hashed password
    sessions = [] # one to many relationship with session

class Session(BaseModel):
    session_id: str
    user_id: str # foreign key to user
    username: str

users = {
    "stacho": "booze",
    "rusty": "boats"
}

session_cookie_id = "session_id"

def get_current_user(request: Request) -> Optional[str]:
    session_id = request.cookies.get(session_cookie_id)
    if not session_id or session_id not in sessions:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Credentials"
        )
    return sessions[session_id]

@app.get('/authenticated-resource')
async def get_authenticated_route(username: str = Depends(get_current_user)):
    print(username)
    print("I will only allow authenticated requests")


# POST body: {user:{username,password}}
@app.post("/login")
async def create_cookie(user: User, response: Response):
    if user.username not in users or users[user.username] != user.password:
        raise Exception("Invalid login")

    session_id = str(uuid4())
    sessions[session_id] = user.username
    
    # This is where the magic happens. The browser will automatically store this cookie in the browser
    # https://fastapi.tiangolo.com/advanced/response-cookies/

    # If you come from server foo and you get a httponly cookie. any cookie from foo will be sent back.
    response.set_cookie(
        key=session_cookie_id,
        value=session_id,
        httponly=True, # This makes it so Javascript cannot access this cookie.
        max_age=1800,
        samesite="lax"
    )


    return {"message": "You are now logged in"}


# imagine the button just makes this request
@app.post("/logout")
async def logout(response: Response):
    response.delete_cookie(key=session_cookie_id)
    return {"message":"You are logged out"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)