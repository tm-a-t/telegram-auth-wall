import urllib.parse

from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates
from joserfc import jwt
from joserfc.errors import JoseError

from src.auth import auth_router
from src.staticfiles import HTMLStaticFiles
from src.vars import COOKIE_NAME, JWT_SECRET_KEY
from src.whitelist import WHITELIST_IDS

app = FastAPI()
templates = Jinja2Templates('src/templates')
static_files = HTMLStaticFiles(directory='site/')

app.mount('/auth', auth_router)
app.mount('/', static_files, name='static')


@app.middleware('http')
async def middleware(request: Request, call_next):
    response = await call_next(request)
    if request.url.path.startswith('/auth/'):
        return response

    url_safe_path = urllib.parse.quote(request.url.path, safe='')
    template_context = {'request': request, 'next_path': url_safe_path}
    login_wall = templates.TemplateResponse('login.html', template_context)

    token = request.cookies.get(COOKIE_NAME)
    if not token:
        return login_wall

    try:
        token_parts = jwt.decode(token, JWT_SECRET_KEY)
    except JoseError:
        return login_wall

    user_id = token_parts.claims['k']
    if user_id not in WHITELIST_IDS:
        return login_wall

    return response
