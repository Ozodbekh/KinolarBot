import uvicorn
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
from starlette_admin.contrib.sqla import Admin, ModelView

from db import db
from db.models import User, Category
from web.provider import UsernameAndPasswordProvider

app = Starlette()
db.init()
admin = Admin(db._engine, title="Example: SQLAlchemy",
              base_url='/',
              auth_provider=UsernameAndPasswordProvider(),
              middlewares=[Middleware(SessionMiddleware, secret_key="qewrerthytju4")],
              )



admin.add_view(ModelView(User))
admin.add_view(ModelView(Category))

admin.mount_to(app)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
# uvicorn web.main:app