from app.database import SessionLocal
from app import crud

def seed_admin():
    db = SessionLocal()

    user = crud.get_user_by_email(db, "admin@test.com")
    if user:
        db.delete(user)
        db.commit()

    crud.create_user(
        db,
        email="admin@test.com",
        password="admin123",
        is_admin=True
    )

    print("Admin user created")
    db.close()

if __name__ == "__main__":
    seed_admin()
