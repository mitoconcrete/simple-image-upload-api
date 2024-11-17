from fastapi.responses import JSONResponse


async def unknown_exception_handler(request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={'message': 'Internal Server Error', 'error_code': 999, 'detail': str(exc)},
    )


exceptions = [
    (
        Exception,
        unknown_exception_handler,
    )
]
