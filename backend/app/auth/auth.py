from fastapi import APIRouter, HTTPException

from app.schemas.user_schema import UserLogin

from app.auth.security import create_access_token

router = APIRouter(tags=["Authentication"])


@router.post("/login")
def login(user: UserLogin):

    if (
        user.username == "admin"
        and
        user.password == "admin123"
    ):

        token = create_access_token(

            {

                "sub": user.username

            }

        )

        return {

            "access_token": token,

            "token_type": "bearer"

        }

    raise HTTPException(

        status_code=401,

        detail="Invalid username or password"

    )