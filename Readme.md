# 🐾 Pawgress

A modern skill-tracking app for veterinary technicians and nurses.

Pawgress helps vet med professionals grow their skills, track proficiency, log CE credits, and provide transparency across clinics — without the spreadsheets, gatekeeping, or guesswork.

---

## 🚀 Table of Contents

- [🐾 Pawgress](#-pawgress)
  - [🚀 Table of Contents](#-table-of-contents)
  - [⚙️ Installation](#️-installation)
    - [Backend (FastAPI)](#backend-fastapi)
    - [Frontend (React + Vite + Tailwind)](#frontend-react--vite--tailwind)
  - [🐕 Usage](#-usage)
  - [✨ Features](#-features)
    - [✅ Core Features (Live)](#-core-features-live)
    - [🧪 In Progress / Planned](#-in-progress--planned)
  - [🧰 Tech Stack](#-tech-stack)
  - [👨‍💻 Contributing](#-contributing)
  - [📄 License](#-license)
  - [🙏 Acknowledgments](#-acknowledgments)

---

## ⚙️ Installation

FastAPI backend, React + TypeScript frontend.

### Backend (FastAPI)

```bash
cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

Create a `.env` file in `backend/` with:

```
DATABASE_URL=your_database_url
SECRET_KEY=your_secret_key
ALLOWED_ORIGINS=http://localhost:5173
```

Then:

```bash
uvicorn backend.main:app --reload
```

### Frontend (React + Vite + Tailwind)

```bash
cd frontend
npm install
npm run dev
```

---

## 🐕 Usage

Log in to see your dashboard with your current skill levels, signed-off tasks, and CE records. Admins can add skills, approve proficiencies, and manage clinic data.

Great for:
- Clinic onboarding
- CE tracking
- Showing your growth over time
- Preventing skill siloing or favoritism

---

## ✨ Features

### ✅ Core Features (Live)

- 🔐 JWT-based authentication with role access (user, admin, superuser)
- 🏥 Clinic-based data separation
- 🧠 Skill tracking with 1–5 level ranking system:
  - Awareness → Mentor
- ✅ Sign-off system: "Signed off by [admin] on [date]"
- 👤 User and admin dashboards
- 📋 CRUD for users, categories, skills, proficiencies
- 🗒️ Activity logging (via Loguru)
- 💅 Shadcn + Tailwind frontend with responsive components

### 🧪 In Progress / Planned

- 🗂 CE credit tracking + certificate uploads
- 📨 Email reminders for expiring licenses/CE deadlines
- 📊 CSV data export (per user or clinic)
- 🧪 Test suite for routes, uploads, auth edge cases
- 📦 Demo mode (seed dummy users & data)

---

## 🧰 Tech Stack

- **Frontend:** React + TypeScript, Vite, Tailwind CSS, Shadcn/UI
- **Backend:** FastAPI, SQLAlchemy, MySQL
- **Auth:** JWT
- **Logging:** Loguru
- **Testing:** (Coming soon) Pytest, Playwright

---

## 👨‍💻 Contributing

Pull requests welcome! Open an issue or reach out if you’d like to contribute.

If you're a vet tech or practice manager and have suggestions, I’d especially love to hear from you!

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 🙏 Acknowledgments

Built by a veterinary surgical nurse to solve real-world problems in clinical skill tracking, onboarding, and burnout prevention. Inspired by the amazing techs and nurses who keep clinics running ❤️

