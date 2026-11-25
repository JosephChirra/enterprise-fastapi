from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import hash_password


class UserNotFoundError(Exception):
    pass


class UserAlreadyExistsError(Exception):
    pass

# def create_user(db:Session, input_user:UserCreate):

#     existing_user= db.query(User).filter(
#         User.email == input_user.email  # Filter by email
#     ).first()

#     if existing_user:
#         raise UserAlreadyExistsError()
    
#     new_user= User(**input_user.model_dump())

#     db.add(new_user)
#     try:
#         db.commit()
#         db.refresh(new_user)
#         return new_user
#     except IntegrityError:
#         db.rollback()
#         raise UserAlreadyExistsError()

def create_user(db: Session, input_user: UserCreate):

    existing_user = db.query(User).filter(
        User.email == input_user.email
    ).first()

    if existing_user:
        raise UserAlreadyExistsError()

    user_data = input_user.model_dump(exclude={"password"})

    new_user = User(
        **user_data,
        hashed_password=hash_password(input_user.password)
    )

    db.add(new_user)

    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise UserAlreadyExistsError() from exc

    db.refresh(new_user)
    return new_user



def get_users(db:Session, page:int, limit:int, name:str | None=None, email:str | None=None  ):
    # return db.query(User).offset((page-1)*limit).limit(limit).all()
    query = db.query(User)

    if name:
        query =  query.filter(User.name.ilike(f"%{name}%")) 
    if email:
        query = query.filter(
            User.email.ilike(f"%{email}%")
        )

    return query.offset((page-1)*limit).limit(limit).all()

def get_user_by_id(db:Session, item_id:int):

    user = db.query(User).filter(
        User.id == item_id
    ).first()

    if not user:
        raise UserNotFoundError()
    return user


def delete_user(db:Session, item_id:int):

    user= get_user_by_id(db, item_id)

    db.delete(user)
    db.commit()

def update_user(db:Session, item_id:int, input_user:UserCreate):
    user = get_user_by_id(db, item_id)
    print("user:",user.email)

    for key, value in input_user.model_dump().items():
        setattr(user,key, value)

    try:
        db.commit()
        db.refresh(user)
        return user
    except IntegrityError:
        db.rollback()
        raise UserAlreadyExistsError()

def patch_user(db:Session, item_id:int, input_user:UserCreate):
    user= get_user_by_id(db,item_id)

    update_data = input_user.model_dump(exclude_unset=True)
    for key,value in update_data.items():
        setattr(user,key,value)
    
    try:
        db.commit()
        db.refresh(user)
        return user
    except IntegrityError:
        db.rollback()
        raise UserAlreadyExistsError()
