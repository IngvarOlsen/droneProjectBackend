from website import create_app, create_database
from sanic import Sanic
from sanic.response import html

import socketio

app = create_app()
#create_database(app)


#sio = socketio.AsyncServer(async_mode='sanic')
#app = Sanic()
#sio.attach(app)


#@app.route('/socketTest')
#def index(request):
#    with open('latency.html') as f:
#        return html(f.read())


#@sio.event
#async def ping_from_client(sid):
#    await sio.emit('pong_from_server', room=sid)

#app.static('/static', './static')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
