from app import create_app

app = create_app()
app.config.from_object('config.Config')

if __name__ == '__main__':
    app.run(debug=True)