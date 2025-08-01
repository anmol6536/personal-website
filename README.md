# Personal Micro-Site

A hip, personal micro-site for a "developer / photographer / cooking-nerd".

## Tech Stack

*   **Backend:** Flask 3.0
*   **Templating:** Jinja2
*   **Styling:** Tailwind CSS (v3 CDN)
*   **Frontend Interactivity:** HTMX & Alpine.js

## Setup and Running

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2.  **Create a virtual environment and activate it:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install Flask Markdown
    ```

4.  **Set the Flask application:**
    ```bash
    export FLASK_APP=app.py
    ```

5.  **Run the application in debug mode:**
    ```bash
    flask run --debug
    ```

The application will be available at `http://0.0.0.0:5000`.

## Project Structure

```
├── app.py
├── static/
│   ├── css/
│   │   └── main.css
│   └── js/
│       └── htmx.js
└── templates/
    ├── base.html
    ├── landing.html
    ├── timeline.html
    ├── gallery/
    │   ├── index.html
    │   └── modal.html
    └── blog/
        ├── index.html
        └── post.html
``` 