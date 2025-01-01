from datetime import datetime
from typing import Optional


def get_date(value: str) -> Optional[datetime]:
    try:
        return datetime.strptime(
            value, f'%d.%m.{["%-y","%-y","%y","%Y","%Y"][len(value.split(".")[2])]}'
        )
    except ValueError as e:
        print(e, value, type(value), str(value), len(value))
        return None


def get_int(value: str) -> int:
    return 0 if not str(value).isnumeric() else int(value)


def get_float(value: str, dezimal: int = 2) -> float:
    return round(float(value.replace(",", ".")), dezimal)
