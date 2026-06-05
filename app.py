from app import create_app

if __name__ == "__main__":
    # Local development server (Render uses gunicorn via the Procfile)
    create_app().run(host="0.0.0.0", port=8000, debug=False)
