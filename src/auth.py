import hmac
from typing import Annotated

from fastapi import APIRouter, Query
from fastapi.requests import Request
from fastapi.responses import PlainTextResponse, RedirectResponse
from joserfc import jwt

from src.vars import BOT_TOKEN_HASH, JWT_SECRET_KEY, COOKIE_NAME

auth_router = APIRouter()


@auth_router.get('/telegram-callback')
async def telegram_callback(
        request: Request,
        user_id: Annotated[int, Query(alias='id')],
        query_hash: Annotated[str, Query(alias='hash')],
        next_url: Annotated[str, Query(alias='next')] = '/',
):
    params = request.query_params.items()
    data_check_string = '\n'.join(sorted(f'{x}={y}' for x, y in params if x not in ('hash', 'next')))
    computed_hash = hmac.new(BOT_TOKEN_HASH.digest(), data_check_string.encode(), 'sha256').hexdigest()
    is_correct = hmac.compare_digest(computed_hash, query_hash)
    if not is_correct:
        return PlainTextResponse('Authorization failed. Please try again', status_code=401)

    token = jwt.encode({'alg': 'HS256'}, {'k': user_id}, JWT_SECRET_KEY)
    response = RedirectResponse(next_url)
    response.set_cookie(key=COOKIE_NAME, value=token)
    return response


@auth_router.get('/logout')
async def logout():
    response = RedirectResponse('/')
    response.delete_cookie(key=COOKIE_NAME)
    return response


@auth_router.get('<path:path>')
async def unknown(path: str):
    return PlainTextResponse('Not found', status_code=404)
