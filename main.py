from website import create_app, create_database

app = create_app()
#create_database(app)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80, debug=True)
