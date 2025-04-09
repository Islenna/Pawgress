# Pawgress

A veterinary nurse skill and certification tracking app

## Table of Contents

- [Pawgress](#pawgress)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Features](#features)

## Installation

FastAPI backend, React + TypeScript frontend.

1. Clone the repo
2. Set up the backend with:
    ```bash
    cd backend
    python -m venv venv
    source venv/bin/activate  # or venv\Scripts\activate on Windows
    pip install -r requirements.txt
    ```
3. Set up the frontend with:
    ```bash
    cd frontend
    npm install
    npm run dev
    ```
4. Configure your `.env` with appropriate values for `DATABASE_URL` and CORS settings.

## Usage

This app helps veterinary hospitals track and sign off on the skill proficiency of their technicians and nurses. Log in to view your skill tree, see what’s next to learn, and keep track of your continuing education.

## Features

- Per-user dashboards and admin dashboards
- Skill CRUD (create, view, edit, delete)
- Categories to organize skills
- Role-based access (admin vs user)
- Future: Continuing Education (CE) credit tracking
- Future: Email reminders for license renewal deadlines