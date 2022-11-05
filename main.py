from threadsnake.http.middlewares.authorization import authorization
from threadsnake.http.middlewares.bodyparser import body_parser
from threadsnake.http.middlewares.multipartformdataparser import multipart_form_data_parser
from threadsnake.http.middlewares.requests import accepts_json, requires_parameters
from threadsnake.turbo import *
from threadsnake.http.middlewares.session import session
from threadsnake.http.middlewares.static import static
from threadsnake.http.tools.routing import configure_routes

app:Application = Application(8084)

configure_routes(app, 'routes')

app.configure(body_parser)
app.configure(authorization)
app.configure(session('threadsnakeSessionId'))
app.configure(static())
app.configure(multipart_form_data_parser())

@app.get('/')
def endpoints(app:Application, req:HttpRequest, res:HttpResponse):
    html:str = ''
    for method in app.routes:
        for route in app.routes[method]:
            html += f'<div><strong>{method}</strong>{route}</div>'
    res.html(html)
            
try:
    app.start()
except:
    pass