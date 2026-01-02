import time
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware

# CONFIG
MAX_REQUESTS = 5
WINDOW_SECONDS = 60  # 1 minute

# In-memory store
ip_store = {}

class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host
        current_time = time.time()

        # Get existing IP record
        record = ip_store.get(client_ip)

        if record:
            request_count, first_request_time = record

            # Reset window if time passed
            if current_time - first_request_time > WINDOW_SECONDS:
                ip_store[client_ip] = (1, current_time)
            else:
                if request_count >= MAX_REQUESTS:
                    raise HTTPException(
                        status_code=429,
                        detail="Too many requests. Please try again later."
                    )
                ip_store[client_ip] = (request_count + 1, first_request_time)
        else:
            # First request from this IP
            ip_store[client_ip] = (1, current_time)

        return await call_next(request)
