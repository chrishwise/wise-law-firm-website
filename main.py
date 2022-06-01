from website import create_app
from waitress import serve

app = create_app()

if __name__ == '__main__':
    # app.run()
    # app.run('0.0.0.0',port=server_port)
    serve(app, host='0.0.0.0', port=8080)