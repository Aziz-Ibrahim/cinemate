# Cinemate

[Cinemate](https://cinemate-776f20737057.herokuapp.com/)

Cinemate is a dynamic web application designed to empower movie enthusiasts to discover, review, and curate their favorite films. Built using **Django** for a robust backend and **JavaScript** for a fluid frontend experience, it leverages the **TMDB API** to provide a rich, up-to-date movie database.

---

## Table of Contents

- [Key Features](#key-features)
- [Technologies Employed](#technologies-employed)
- [User Interface and Branding](#user-interface-and-branding)
- [Installation](#installation)
- [Deployment](#deployment)
  - [Local Deployment](#local-deployment)
  - [Heroku Deployment](#heroku-deployment)
- [Usage](#usage)
- [Manual Testing](#manual-testing)
- [Static Analysis Reports](#static-analysis-reports)
- [Future Enhancements](#future-enhancements)
- [Credits](#credits)
- [License](#license)

---

## Key Features

* **Rich Movie Discovery:** Explore comprehensive movie details, including plot summaries, cast information, ratings, and trailers, all powered by the **TMDB API**, enabling users to make informed viewing choices.
* **Real-Time Review System:** Contribute to a vibrant community by submitting and editing movie reviews dynamically with AJAX, fostering user engagement and providing valuable insights.
* **Intuitive Star Ratings:** Express opinions quickly and visually with an interactive star rating system, enhancing user feedback and movie evaluation.
* **Secure User Authentication:** Enjoy a personalized and secure experience with robust user authentication, protecting user data through signup, login, and logout functionalities.
* **Personalized Movie Collections:** Curate your own movie library by adding films to a favorites list, enabling quick access and personalized recommendations.
* **Dark Mode Toggle:** Easily switch between light and dark themes for enhanced user experience and accessibility.
* **Seamless Responsive Design:** Experience optimal viewing and interaction across desktops, tablets, and mobile phones, ensuring a consistent user experience.

---

## Technologies Employed

* **Frontend:** HTML, CSS, and JavaScript with AJAX to create a dynamic and interactive user interface, delivering a smooth, single-page application-like feel.
* **Backend:** Django framework for its robust ORM, built-in security features, and efficient database management, powered by Python for clean and powerful server-side logic.
* **Database:** SQLite for development and PostgreSQL for production, ensuring scalability and data integrity, with Django's ORM facilitating seamless database interactions.
* **APIs:** TMDB API integration for fetching up-to-date movie information, enriching the application with a vast movie database.

---

## User Interface and Branding

* **Logo:** Created using [VistaPrint](https://www.vistaprint.co.uk/logomaker/wizard), reflecting the application's modern and user-friendly design.
* **Hero Image:** Sourced from [Unsplash](https://unsplash.com/), providing a visually appealing backdrop for movie discovery.

---

## Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/Aziz-Ibrahim/cinemate
    cd cinemate
    ```
2. **Create a virtual environment:**
    ```bash
    python -m venv env
    source env/bin/activate # On Windows: env\Scripts\activate
    ```
3. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4. **Set environment variables (.env):**
    ```
    SECRET_KEY=your-secret-key
    TMDB_API_KEY=your-tmdb-api-key
    ```
5. **Apply database migrations:**
    ```bash
    python manage.py migrate
    ```
6. **Run the development server:**
    ```bash
    python manage.py runserver
    ```
    Open http://127.0.0.1:8000 in a browser.

---

## Deployment

### Local Deployment

* Run locally using VS Code and the Django development server (see Installation).

### Heroku Deployment

1. **Install Heroku CLI:**
    ```bash
    curl https://cli-assets.heroku.com/install.sh | sh # macOS/Linux
    ```
    or
    ```bash
    pip install heroku-cli # Windows
    ```
2. **Login to Heroku:**
    ```bash
    heroku login
    ```
3. **Create a Heroku app:**
    ```bash
    heroku create cinemate-app
    ```
4. **Add PostgreSQL database:**
    ```bash
    heroku addons:create heroku-postgresql:hobby-dev
    ```
5. **Set environment variables:**
    ```bash
    heroku config:set SECRET_KEY=your-secret-key
    heroku config:set TMDB_API_KEY=your-tmdb-api-key
    ```
6. **Deploy to Heroku:**
    ```bash
    git push heroku main
    ```
7. **Run database migrations:**
    ```bash
    heroku run python manage.py migrate
    ```
8. **Open the app:**
    ```bash
    heroku open
    ```

---

## Usage

* Create an account or log in to submit reviews and personalize your experience.
* Search for movies and explore detailed information.
* Leave reviews and rate movies to share your opinions.
* Edit or delete reviews dynamically, ensuring your voice is heard.
* Add movies to your favorites for easy access and personalized recommendations.

---

## Manual Testing

| Feature                     | Test Description                                                                 | Status         |
| :-------------------------- | :------------------------------------------------------------------------------- | :------------- |
| **User Authentication**     |                                                                                 |                |
| Sign Up                     | Register with valid credentials and verify redirection to the login page.        | ✅ Successful  |
| Login                       | Enter valid credentials and confirm redirection to the homepage.                 | ✅ Successful  |
| Logout                      | Click the logout button and ensure return to the login page.                     | ✅ Successful  |
| **Movie Search and Details** |                                                                                 |                |
| Search                      | Ensure movie search results display dynamically.                                 | ✅ Successful  |
| Movie Details               | Verify that movie details pages load correctly.                                  | ✅ Successful  |
| Trailers and Providers      | Confirm that correct trailer and provider information is displayed.              | ✅ Successful  |
| **Review System**            |                                                                                 |                |
| Submit Review               | Ensure that reviews are submitted dynamically without requiring a page reload.   | ✅ Successful  |
| Edit Review                 | Verify that review edits update dynamically.                                     | ✅ Successful  |
| Delete Review               | Confirm that reviews are removed dynamically.                                    | ✅ Successful  |
| **Favorites**                |                                                                                 |                |
| Add to Favorites            | Ensure that movies are added to favorites and the UI updates accordingly.         | ✅ Successful  |
| Remove from Favorites       | Verify that removing movies from favorites is reflected in the UI.               | ✅ Successful  |
| Favorites Page              | Confirm that added movies appear correctly on the favorites page.                | ✅ Successful  |
| **Responsiveness**           |                                                                                 |                |
| Mobile and Tablet Testing   | Ensure that the application is fully responsive across mobile and tablet devices. | ✅ Successful  |
| Browser Compatibility       | Verify consistency and functionality across Chrome, Firefox, and Edge browsers.  | ✅ Successful  |
| **Dark Mode Toggle**         |                                                                                 |                |
| Theme Toggle                | Ensure that switching themes updates page colors and images dynamically.         | ✅ Successful  |

---

## Static Analysis Reports

This project incorporates static analysis to ensure code quality and adherence to best practices. The following reports were generated and are available in the `docs` directory for review:

* [PEP 8 Linter Report](docs/cinemate-pep8-linter-report.pdf)
* [HTML Markup Validation Report](docs/cinemtate-html-markup-validation-report.pdf)
* [CSS Markup Validation Report](docs/cinemate-css-markup-validation-report.pdf)
* [JavaScript JSHint Report](docs/cinemate-jshint-report.pdf)

Additionally:

* [Entity-Relationship Diagram (ERD)](docs/cinemate-erd.pdf)
* [Wireframes](docs/cinemate-wireframes.pdf)
* [Data Flow Diagram](docs/data-flow-diagram.pdf)

---

## Future Enhancements

| Feature             | Description                                                         | Status      |
| :------------------ | :------------------------------------------------------------------- | :---------- |
| Bookmark Movies     | Include bookmarking movies besides adding to favorites              | 🔄 Planned  |

---

## Credits

* Developed with the assistance of AI tools like ChatGPT and Gemini, which played a crucial role in debugging and resolving complex coding challenges, significantly expediting the development process.

---

## License

* This project is open-source and available under the MIT License.
