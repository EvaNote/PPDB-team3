from src import create_app, ProductionConfig

app = create_app(ProductionConfig)

if __name__ == "__main__":
    app.run()
