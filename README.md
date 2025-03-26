# Cinemate

Cinemate is a web application for discovering, reviewing, and rating movies. It is built using **Django**, **JavaScript**, **HTML**, and **CSS**.

---
## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [User Interface and Branding](#user-interface-and-branding)
- [Installation](#installation)
- [Deployment](#deployment)
  - [Local Deployment](#local-deployment)
  - [Heroku Deployment](#heroku-deployment)
- [Usage](#usage)
- [Manual Testing](#manual-testing)
- [Future Enhancements](#future-enhancements)
- [Credits](#credits)
- [License](#license)

---
## Features

- Browse movie details retrieved from **The Movie Database (TMDB) API**
- Submit and edit reviews dynamically with AJAX
- Rate movies with an interactive star rating system
- User authentication (signup, login, logout)
- Add movies to **favorites** for easy access
- Responsive user interface

---
## Technologies Used

- **Frontend:** HTML, CSS, JavaScript (AJAX)
- **Backend:** Django, Python
- **Database:** SQLite / PostgreSQL
- **APIs:** TMDB API (for movie details and ratings)

## User Interface and Branding

- **Logo:** Created using [VistaPrint](https://www.vistaprint.co.uk/logomaker/wizard)'s online logo maker.
- **Hero Image:** Downloaded from [Unsplash](https://unsplash.com/)

---
## Installation

1. **Clone the repository:**
   ```
   git clone https://github.com/your-username/cinemate.git
   cd cinemate
   ```

2. **Create and activate a virtual environment:**
    ```
    python -m venv env
    source env/bin/activate  # On Windows: env\Scripts\activate
    ```

3. **Install dependencies:**
    ```
    pip install -r requirements.txt
    ```

4. **Set up environment variables: Create a .env file and add the required environment variables:**
    ```
    SECRET_KEY=your-secret-key
    TMDB_API_KEY=your-tmdb-api-key
    ```

5. **Apply database migrations:**
    ```
    python manage.py migrate
    ```

6. **Run the development server locally:**
    ```
    python manage.py runserver
    ```
    Open http://127.0.0.1:8000 in a web browser.

---
## Deployment
**Local Deployment**
- The project can be run locally using Visual Studio Code (VS Code) and the Django development server as shown in installation section above.

**Heroku Deployment**
- Install the Heroku CLI (if not installed):

    ```
    curl https://cli-assets.heroku.com/install.sh | sh  # On macOS/Linux
    choco install heroku-cli  # On Windows
    ```

- Login to Heroku:
    ```
    heroku login
    ```

- Create a Heroku app:
    ```
    heroku create cinemate-app
    ```

- Add Heroku’s PostgreSQL database (if using PostgreSQL):
    ```
    heroku addons:create heroku-postgresql:hobby-dev
    ```

- Set environment variables on Heroku:
    ```
    heroku config:set SECRET_KEY=your-secret-key
    heroku config:set TMDB_API_KEY=your-tmdb-api-key
    ```


- Deploy to Heroku:
    ```
    git push heroku main
    ```


- Run database migrations on Heroku:
    ```
    heroku run python manage.py migrate
    ```


- Open the app in a browser:
    ```
    heroku open
    ```
---
## Usage
- Create an account or log in to submit reviews

- Search for movies and view details

- Leave a review and rate a movie

- Edit or delete reviews dynamically

- Favorite movies to save them for later

---
## Manual Testing

| Feature                     | Test Description | Status |
|-----------------------------|-----------------|--------|
| **User Authentication**      | | |
| Sign Up                     | Register with valid credentials and verify redirection to the login page. | ✅ Successful |
| Login                       | Enter valid credentials and confirm redirection to the homepage. | ✅ Successful |
| Logout                      | Click the logout button and ensure return to the login page. | ✅ Successful |
| **Movie Search and Details** | | |
| Search for a movie          | Ensure results display dynamically. | ✅ Successful |
| Click on a movie            | Verify the movie details page loads correctly. | ✅ Successful |
| Check trailers and providers | Confirm correct information is displayed. | ✅ Successful |
| **Review System**            | | |
| Submit a review             | Ensure it appears dynamically without requiring a page reload. | ✅ Successful |
| Edit a review               | Verify the changes update dynamically. | ✅ Successful |
| Delete a review             | Confirm that the review is removed dynamically. | ✅ Successful |
| **Favorites**               | | |
| Add a movie to favorites    | Ensure the UI updates accordingly. | ✅ Successful |
| Remove a favorite           | Verify the UI reflects the change. | ✅ Successful |
| Check the favorites page    | Confirm that added movies appear correctly. | ✅ Successful |
| **Responsiveness & Compatibility** | | |
| Mobile & Tablet Testing     | Ensure a fully responsive layout. | ✅ Successful |
| Browser Compatibility       | Check on different browsers (Chrome, Firefox, Edge) for consistency. | ✅ Successful |

---
## Future Enhancements

| Feature                   | Description | Status |
|---------------------------|-------------|--------|
| Pagination                | Implement pagination for movie listings. | 🔄 Planned |
| User Profile Pages        | Add profile pages with user review history. | 🔄 Planned |
| Dark Mode Toggle          | Introduce a dark mode toggle for better accessibility. | 🔄 Planned |


---
## Credits
- This project was developed with the assistance of **ChatGPT**, which played a key role in debugging and resolving various development challenges.

---
## License
- This project is **open-source** and available under the MIT License.