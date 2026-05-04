from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

async def validation_exception_handler(request, exc: RequestValidationError):
    first_error = exc.errors()[0]

    return JSONResponse(
        status_code=422,
        content={
            "error": {
                "code": "VALIDATION_ERROR",
                "message": first_error["msg"]
            }
        },
    )
