from datetime import date, timedelta

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.hydration_record import HydrationRecord
from app.models.user import User
from app.schemas.health_summary import HealthSummaryResponse

SUSPICIOUS_INTAKE_THRESHOLD_ML = 10_000


def calculate_trend(values: list[int]) -> str:
    if len(values) < 3:
        return "INSUFFICIENT_DATA"

    midpoint = len(values) // 2

    first_half = values[:midpoint]
    second_half = values[midpoint:]

    first_average = sum(first_half) / len(first_half)
    second_average = sum(second_half) / len(second_half)

    difference = second_average - first_average

    if difference > 100:
        return "IMPROVING"

    if difference < -100:
        return "DECLINING"

    return "STABLE"


def get_health_summary(
    db: Session,
    user_id: int,
) -> HealthSummaryResponse | None:

    user = db.get(User, user_id)

    if user is None:
        return None

    end_date = date.today()
    start_date = end_date - timedelta(days=6)

    records = db.scalars(
        select(HydrationRecord)
        .where(
            HydrationRecord.user_id == user_id,
            HydrationRecord.date >= start_date,
            HydrationRecord.date <= end_date,
        )
        .order_by(HydrationRecord.date)
    ).all()

    records_by_date = {record.date: record for record in records}

    valid_values: list[int] = []
    suspicious_days = 0

    for current_date in (start_date + timedelta(days=i) for i in range(7)):
        record = records_by_date.get(current_date)

        if record is None:
            continue

        if record.water_intake_ml > SUSPICIOUS_INTAKE_THRESHOLD_ML:
            suspicious_days += 1
            continue

        valid_values.append(record.water_intake_ml)

    valid_days = len(valid_values)
    missing_days = 7 - len(records_by_date)

    if valid_days == 0:
        return HealthSummaryResponse(
            user_id=user_id,
            target_ml=user.daily_water_target_ml,
            average_intake_ml=None,
            target_achievement_percent=None,
            gap_ml=None,
            target_status="NO_DATA",
            valid_days=0,
            missing_days=missing_days,
            suspicious_days=suspicious_days,
            trend="INSUFFICIENT_DATA",
            data_quality="INSUFFICIENT",
        )

    average = sum(valid_values) / valid_days

    achievement = (average / user.daily_water_target_ml) * 100

    gap = max(
        user.daily_water_target_ml - average,
        0,
    )

    if average < user.daily_water_target_ml:
        target_status = "BELOW_TARGET"
    else:
        target_status = "MEETING_TARGET"

    trend = calculate_trend(valid_values)

    if valid_days < 3:
        data_quality = "INSUFFICIENT"
    elif suspicious_days > 0 or missing_days > 2:
        data_quality = "WARNING"
    else:
        data_quality = "GOOD"

    return HealthSummaryResponse(
        user_id=user_id,
        target_ml=user.daily_water_target_ml,
        average_intake_ml=round(average, 2),
        target_achievement_percent=round(achievement, 2),
        gap_ml=round(gap, 2),
        target_status=target_status,
        valid_days=valid_days,
        missing_days=missing_days,
        suspicious_days=suspicious_days,
        trend=trend,
        data_quality=data_quality,
    )
