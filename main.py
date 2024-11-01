from website import create_app

app = create_app()

with app.app_context():
    # noinspection PyUnresolvedReferences
    from website.utils import context_processor

if __name__ == '__main__':
    app.run()
