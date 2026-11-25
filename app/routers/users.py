from fastapi import APIRouter,HTTPException,Depends
from app.schemas.user import UserCreate, UserResponse,UserUpdate
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import User
from fastapi import Query


from app.services import user_service
from app.services.user_service import (
    UserNotFoundError,
    UserAlreadyExistsError
)

router = APIRouter()


# @router.get('/', response_model=list[UserResponse])
# def getUsers(db : Session=Depends(get_db)):
#     # return db.query(User).all()
#     return user_service.get_users(db)

@router.get("/", response_model=list[UserResponse])
def get_users(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    name:str| None =None,
    email:str | None = None,
    db: Session = Depends(get_db)
):
    return user_service.get_users(db, page, limit)

@router.get("/{item_id}", response_model=UserResponse)
def getUserById(item_id: int, db: Session= Depends(get_db)):

    # user = db.query(User).filter(User.id == item_id).first()
    # if not user:
    #     raise HTTPException(
    #     status_code=404,
    #     detail="User not found"
    # )
    # return user
    try:
        return user_service.get_user_by_id(db, item_id)
    except UserNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="user not found"
        )

    


@router.post("/", response_model = UserResponse , status_code=201)
def CreateUser(input_user: UserCreate, db: Session = Depends(get_db)):
    # existing_user= db.query(User).filter(
    #     User.email == input_user.email
    # ).first()
    # if existing_user:
    #     raise HTTPException(
    #         status_code = 409,
    #         detail="User with this email already exists"
    #     )

    # new_user= User(**input_user.model_dump())

    # db.add(new_user)
    # db.commit()
    # db.refresh(new_user)

    # return new_user

    try:
        return user_service.create_user(db, input_user)

    except UserAlreadyExistsError:
        raise HTTPException(
            status_code=409,
            detail="Email already Exists..."
        )

@router.put('/{item_id}', response_model =  UserResponse, status_code=200)
def UpdateUser(input_user:UserUpdate, item_id:int,db: Session = Depends(get_db)):
    # for user in users:
    #     if user["id"] == item_id:
    #         user.update(input_user.model_dump())
    #         return user
    #     raise HTTPException(status_code=404, detail="user Doesnot exists")
    try:
        return user_service.update_user(db, item_id, input_user)

    except UserNotFoundError:
        raise HTTPException(status_code=404, detail="User not found")

    except UserAlreadyExistsError:
        raise HTTPException(status_code=409, detail="Email already exists")
    

@router.delete("/{item_id}",status_code=204)
def delete_user(item_id:int, db:Session=Depends(get_db)):

    # user = db.query(User).filter(User.id == item_id).first()
    
    # if not user:
    #     raise HTTPException(status_code=404, detail="Invalid User")
    # db.delete(user)
    # db.commit()
    # return None

    try:
        user_service.delete_user(db, item_id)
    except UserNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="user not found"
        )

@router.patch("/{item_id}", status_code=200, response_model=UserResponse)
def patch_user(item_id:int, input_user:UserCreate, db:Session = Depends(get_db)):
    try:
        user = user_service.patch_user(db, item_id, input_user)
        
    except UserNotFoundError:
        raise HTTPException(status_code=404, detail="User not found")