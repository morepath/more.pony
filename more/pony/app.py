import morepath
from pony.orm import db_session, TransactionError


class App(morepath.App):
    pass


@App.setting_section(section="pony")
def get_pony_settings():
    return {
        "allowed_exceptions": [],
        "immediate": False,
        "retry": 0,
        "retry_exceptions": [TransactionError],
        "serializable": False,
        "strict": False,
    }


@App.tween_factory(over=morepath.EXCVIEW)
def pony_tween_factory(app, handler):
    @db_session(
        allowed_exceptions=app.settings.pony.allowed_exceptions,
        immediate=app.settings.pony.immediate,
        retry=app.settings.pony.retry,
        retry_exceptions=app.settings.pony.retry_exceptions,
        serializable=app.settings.pony.serializable,
        strict=app.settings.pony.strict,
    )
    def pony_tween(request):
        return handler(request)

    return pony_tween
