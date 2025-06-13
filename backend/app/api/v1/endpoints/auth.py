from fastapi import APIRouter, HTTPException, Depends
from app.schemas.user import UserRegister, UserLogin
from app.database import get_db
from sqlalchemy.orm import Session
from app.services import user_service
from app.core.security import verify_password, create_access_token, get_password_hash
from app.database.models.user import User, UserType
import uuid
from datetime import datetime
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()


@router.post("/register")
async def register(user_data: UserRegister, db: Session = Depends(get_db)):
    try:
        # Checks if user already exists
        existing_user = user_service.get_user_by_email(db=db, email=user_data.email)
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")

        # Hash the password
        hashed_password = get_password_hash(user_data.password)

        # Create user instance
        new_user = User(
            email=user_data.email,
            password_hash=hashed_password,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            phone_number=user_data.phone,
            user_type=UserType.CLIENT,
            is_verified=True,
        )

        # Save to database
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return {
            "message": "User registered successfully",
            "user": {
                "id": str(new_user.id),
                "email": new_user.email,
                "first_name": new_user.first_name,
                "last_name": new_user.last_name,
                "phone": new_user.phone_number,
            },
        }
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # Log error
        import traceback

        print(f"Registration error: {str(e)}")
        print(traceback.format_exc())
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/login")
async def login(user: UserLogin, db: Session = Depends(get_db)):
    try:
        # Get the user from database by email
        db_user = user_service.get_user_by_email(db=db, email=user.email)
        print(f"Login attempt: {user.email}")

        # If user not found, raise exception
        if not db_user:
            print(f"User not found: {user.email}")
            raise HTTPException(status_code=401, detail="Invalid email or password")

        print(f"User found: {db_user.email}, checking password")
        # Checks the correctness of the entered password
        print(
            f"Password check: {user.password} vs hash {db_user.password_hash[:10]}..."
        )
        result = verify_password(user.password, db_user.password_hash)
        print(f"Password verification result: {result}")

        if not result:
            print(f"Password incorrect for: {user.email}")
            raise HTTPException(status_code=401, detail="Invalid email or password")

        # Generate JWT token
        print(f"Generating token for user: {db_user.id}")
        access_token = create_access_token(subject=str(db_user.id))

        return {"access_token": access_token, "token_type": "bearer"}
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Log the error here
        print(f"Login error: {str(e)}")
        import traceback

        print(traceback.format_exc())
        raise HTTPException(status_code=401, detail="Invalid credentials")


@router.post("/create-test-user")
async def create_test_user(db: Session = Depends(get_db)):
    """Creates a test user with a fixed password for demonstration purposes"""
    try:
        # Test user credentials
        test_user = {
            "email": "demo@example.com",
            "password": "Demo123!",
            "first_name": "Demo",
            "last_name": "User",
            "phone_number": "+1234567890",
            "user_type": "client",
        }

        # Check if user already exists
        existing_user = db.query(User).filter(User.email == test_user["email"]).first()
        if existing_user:
            return {
                "message": f"Test user {test_user['email']} already exists",
                "user": {
                    "email": test_user["email"],
                    "password": test_user[
                        "password"
                    ],  # Returning password since this is just for testing
                },
            }

        # Create new user
        user_id = str(uuid.uuid4())
        now = datetime.utcnow()

        hashed_password = get_password_hash(test_user["password"])

        new_user = User(
            id=user_id,
            email=test_user["email"],
            password_hash=hashed_password,
            first_name=test_user["first_name"],
            last_name=test_user["last_name"],
            phone_number=test_user["phone_number"],
            user_type=test_user["user_type"],
            created_at=now,
            updated_at=now,
            is_verified=True,
            is_active=True,
        )

        db.add(new_user)
        db.commit()

        return {
            "message": "Test user created successfully",
            "user": {
                "email": test_user["email"],
                "password": test_user[
                    "password"
                ],  # Returning password since this is just for testing
            },
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500, detail=f"Error creating test user: {str(e)}"
        )


@router.post("/token")
async def login_for_swagger(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    """Login endpoint compatible with Swagger UI and OAuth2 standard"""
    try:
        # Get the user from database by email
        db_user = user_service.get_user_by_email(db=db, email=form_data.username)

        # If user not found or password doesn't match, raise exception
        if not db_user:
            raise HTTPException(status_code=401, detail="Invalid username or password")

        # Check if the password is correct
        if not verify_password(form_data.password, db_user.password_hash):
            raise HTTPException(status_code=401, detail="Invalid username or password")

        # Generate JWT token
        access_token = create_access_token(subject=str(db_user.id))

        return {"access_token": access_token, "token_type": "bearer"}
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Log the error here
        import traceback

        print(f"Swagger login error: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=401, detail="Invalid credentials")
