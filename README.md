# LibMate-Manager

Welcome to **LibMate-Manager**! This is a beginner-friendly command-line application built with **Python** to help you manage your small library like a pro. Say goodbye to lots of paperwork or messy notebooks! With LibMate-Manager, tracking books, authors, borrowers, and loans becomes simple and stress-free.

---

## Features You’ll Love

* **Effortless Data Management:** Easily add, view, and delete authors, books, and borrowers.
* **Smart Loan Tracking:** Track book loans and returns automatically, and know which books are available or currently borrowed.
* **Quick & Easy Search:** Instantly search for books by title or borrowers by phone number.
* **Data Integrity Built-In:** Prevents accidental deletions of books that are currently on loan.
* **Clear Relationships:** See which author wrote which books and which borrower has borrowed what.
* **Automatic Clean-Up (Cascade Deletes):** When you delete an author or borrower, their associated books and loans are automatically deleted – keeping your database clean and consistent.

## Getting Started

Follow these simple steps to run **LibMate-Manager** on your local machine:

### 1. Clone the repository

```bash
git clone git@github.com:biomdoian/LibMate-Manager.git
cd LibMate-Manager
2. Set up the environment
We use Pipenv to manage dependencies and isolate the environment:

Bash
pipenv install
pipenv shell

3. Prepare the database
Apply the database schema using Alembic migrations:

Bash
alembic upgrade 

4. Optional: Add sample data
Load some sample books, authors, and borrowers for testing and fun:

Bash
pipenv run python lib/seed.py
How to Use
You're ready to launch!

Bash
pipenv run python lib/cli.py
Just follow the interactive menu – it's user-friendly and guides you every step of the way.

Project Structure
LibMate-Manager/
├── alembic/              # Database migration scripts managed by Alembic
├── lib/
│   ├── cli.py            # The main Command-Line Interface (CLI) application
│   └── db/
│       ├── models.py     # SQLAlchemy ORM models (Author, Genre, Book, Borrower, Loan)
│       └── seed.py       # Script to populate the database with initial data
└── README.md             # This readme file!

Final Thoughts
LibMate-Manager was built to be a learning-friendly but powerful CLI tool for managing small library systems using Python, SQLAlchemy, and Alembic. It showcases practical database interaction and ORM concepts.

Author
Created by: Ian Biomdo

Contributing
Pull requests, ideas, and suggestions are always welcome! If you'd like to contribute:

Fork the repository.
Create your feature branch:
git checkout -b <your-feature-name>
Commit your changes:
git commit -m "feat: Add your commit message here"
Push to the branch:
git push origin <your-feature-name>
Open a pull request on GitHub!