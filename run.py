from src import create_app, DevelopmentConfig

app = create_app(DevelopmentConfig)

if __name__ == '__main__':
    app.run()
