# Expense Tracker Web App

A personal finance tracking application built with Flask (Python), PostgreSQL, and JavaScript. Users can log in via Google, track income and expenses, view summaries and graphs, and export data.

---

## 🚀 Features

- Google OAuth2 login via frontend (Google Identity Services)
- Persistent sessions (secure cookies)
- Add, edit, and delete income/expense entries
- Manage custom categories (income/expense)
- View dashboard summaries and visualizations
- Export data to CSV or PDF

---

## 🗂️ Pages

- `/login` – Google login via frontend JS
- `/` – Dashboard with summaries and charts
- `/income` – Manage income entries
- `/expenses` – Manage expense entries
- `/categories` – Add/edit/delete categories
- `/reports` – Filter and export income/expense data

---

## 📦 Tech Stack

- **Backend:** Python (Flask), PostgreSQL
- **Frontend:** HTML, CSS, JavaScript, Chart.js
- **Auth:** Google Identity Services (OAuth2 via JS)
- **Exports:** CSV (built-in), PDF (reportlab)
