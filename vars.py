from contextvars import ContextVar

ExternalStatusVar: ContextVar[int] = ContextVar('ExternalStatusVar', default=-1)
