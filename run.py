from src import create_app, DevelopmentConfig

app = create_app(DevelopmentConfig)

if __name__ == '__main__':
    print(app.config['RECAPTCHA_PUBLIC_KEY'])
    print(app.config['RECAPTCHA_PRIVATE_KEY'])
    app.run()
