from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
import time

MAX_REQUESTS = 5
WINDOW_SECONDS = 60
ip_store = {}


class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host
        current_time = time.time()

        record = ip_store.get(client_ip)

        if record:
            request_count, first_request_time = record

            if current_time - first_request_time > WINDOW_SECONDS:
                ip_store[client_ip] = (1, current_time)
            else:
                if request_count >= MAX_REQUESTS:
                    return JSONResponse(
                        status_code=429,
                        content={"detail": "Too many requests. Please try again later."}
                    )
                ip_store[client_ip] = (request_count + 1, first_request_time)
        else:
            ip_store[client_ip] = (1, current_time)

        return await call_next(request)
