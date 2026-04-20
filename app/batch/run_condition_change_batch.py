from datetime import date

from app.db.session import SessionLocal
from app.services.condition_change_service import run_condition_change_batch


def main():
    target_date = date.today()

    db = SessionLocal()
    try:
        result = run_condition_change_batch(db, target_date)
        print(result)
    finally:
        db.close()


if __name__ == "__main__":
    main()