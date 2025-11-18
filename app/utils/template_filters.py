from datetime import datetime


def dt_no_seconds(value, format="%d.%m.%Y %H:%M"):
    if value is None:
        return ""
    if not isinstance(value, datetime):
        return value
    return value.strftime(format)


def init_template_filters(app):
    app.jinja_env.filters["dt_no_seconds"] = dt_no_seconds
