from fastapi import FastAPI, HTTPException, Request
from starlette.responses import JSONResponse

app = FastAPI()


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(status_code=500, content={"detail": "Что-то пошло не так, мы уже исправляем эту ошибку"})
