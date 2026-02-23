async def run(*args, **kwargs):
    from .main import run as _run

    return await _run(*args, **kwargs)
