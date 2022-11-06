from threadsnake.turbo import *
from threadsnake.http.tools.routing import routes_to

app:Application = Application(8084)

routes_to(app, 'routes/people', 'test-router')

try:
    app.start()
except Exception as e:
    print(e)

