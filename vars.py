from contextvars import ContextVar

HTTPResponseCodeVar: ContextVar[int] = ContextVar(
    'ExternalStatusVar',
    default=-1,
)
