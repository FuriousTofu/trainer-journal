from datetime import datetime, timezone
from zoneinfo import ZoneInfo


def dt_no_seconds(value, format="%d.%m.%Y %H:%M"):
    if value is None:
        return ""
    if not isinstance(value, datetime):
        return value

    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)
    local_dt = value.astimezone(ZoneInfo("Europe/Kyiv"))

    return local_dt.strftime(format)


def init_template_filters(app):
    app.jinja_env.filters["dt_no_seconds"] = dt_no_seconds
