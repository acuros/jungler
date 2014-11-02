from jungler.app import create_app
from jungler.ext import celery

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        celery.start()
