from website import create_app

app = create_app()

# if the main.py file is run create the application
if __name__ == '__main__':
    app.run(debug=True)
