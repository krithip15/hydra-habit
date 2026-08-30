import argparse
from datetime import date, timedelta

from sqlalchemy import text

from app.database.database import SessionLocal
from app.models.hydration_record import HydrationRecord
from app.models.user import User


def reset_database(db):
    """
    Clear application data and reset PostgreSQL IDs.
    Keeps the database tables/schema intact.
    """

    db.execute(
        text(
            """
            TRUNCATE TABLE
                agent_execution_logs,
                recommendations,
                hydration_records,
                users
            RESTART IDENTITY CASCADE
            """
        )
    )

    db.commit()

    print("Application data cleared.")


def create_users(db):
    users = [
        User(
            name="Improving User",
            age=24,
            gender="Female",
            height_cm=165,
            weight_kg=60,
            health_goal="INCREASE_INTAKE",
            daily_water_target_ml=2200,
            preferred_reminder_time="18:00",
        ),
        User(
            name="Imperfect Data User",
            age=30,
            gender="Male",
            height_cm=175,
            weight_kg=75,
            health_goal="BUILD_CONSISTENCY",
            daily_water_target_ml=2500,
            preferred_reminder_time="17:00",
        ),
        User(
            name="Insufficient Data User",
            age=28,
            gender="Female",
            height_cm=160,
            weight_kg=55,
            health_goal="MAINTAIN_HYDRATION",
            daily_water_target_ml=2000,
            preferred_reminder_time="19:00",
        ),
    ]

    db.add_all(users)
    db.commit()

    for user in users:
        db.refresh(user)

    return users


def create_hydration_records(db, users):
    today = date.today()

    improving_values = [
        1300,
        1400,
        1500,
        1600,
        1750,
        1900,
        2050,
    ]

    imperfect_values = [
        1800,
        None,
        2000,
        12000,
        1700,
        None,
        1900,
    ]

    insufficient_values = [
        1700,
        None,
        None,
        None,
        1800,
        None,
        None,
    ]

    datasets = [
        (users[0], improving_values),
        (users[1], imperfect_values),
        (users[2], insufficient_values),
    ]

    for user, values in datasets:

        for days_ago, intake in enumerate(reversed(values)):

            if intake is None:
                continue

            record = HydrationRecord(
                user_id=user.id,
                date=today - timedelta(days=days_ago),
                water_intake_ml=intake,
            )

            db.add(record)

    db.commit()


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--reset",
        action="store_true",
        help="Clear existing application data before seeding.",
    )

    args = parser.parse_args()

    db = SessionLocal()

    try:

        if args.reset:
            reset_database(db)

        users = create_users(db)

        create_hydration_records(
            db,
            users,
        )

        print("Seed data created successfully.")

        for user in users:
            print(
                f"{user.id}: {user.name}"
            )

    finally:
        db.close()


if __name__ == "__main__":
    main()