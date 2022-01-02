from realtime.webserver.webapp import app, socket_io

socket_io.run(app, port=5001, debug=True, use_reloader=True)