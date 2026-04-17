from app import app, api

if __name__ == '__main__':
    app.register_blueprint(api.blueprint)
    app.run(debug=True, host='0.0.0.0', port=5000) # Paste your host and port
