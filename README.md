# Pet Adoption Agency

This is a web application built with Flask for managing pet adoptions.

## Setup

1.  **Clone the repository:**

    ```bash
    git clone <your-repo-url>
    cd pet-adoption-agency
    ```

2.  **Set up a virtual environment (recommended):**

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On macOS and Linux
    venv\\Scripts\\activate  # On Windows
    ```

3.  **Install dependencies:**

    ```bash
    pip install Flask Flask-SQLAlchemy Flask-WTF Flask-DebugToolbar python-dotenv
    ```
    * Make sure you have the dependencies in requirements.txt `pip freeze > requirements.txt`

4.  **Set up the database:**

    * Ensure you have a SQLite database set up (or configure a different database in `app.py`).
    * The application should create the database if it doesn't exist.

5.  **Run the application:**

    ```bash
    python app.py
    ```

    * The application should be running at `http://127.0.0.1:5000/`.

## Deployment to Netlify

To deploy this Flask application to Netlify, we need to adapt it to run in a serverless environment using Zappa and AWS Lambda.

### Prerequisites

* **AWS Account:** You'll need an AWS account.
* **Netlify Account:** You'll need a Netlify account
