# online_shop_backend
Django backend for a furniture shop: catalog, cart, orders, accounts, Stripe payments. Env-safe, ready for local dev &amp; deployment.


# Furniture Shop (Django)

Backend for an online furniture store: products, categories, cart, orders, accounts, and Stripe payments.  
Clean `.env` support, simple local setup, and production-ready structure.

## Features
- 🛍️ Catalog with categories
- 🛒 Session-based cart
- 🧾 Orders & checkout flow
- 👤 Accounts (login/logout/password reset)
- 💳 Stripe integration (test-ready)
- 🖼️ Static & media handling
- ⚙️ Env-based configuration (no secrets in code)

## Tech Stack
- Python 3.10+, Django 5.x
- SQLite (dev) / Postgres (prod)
- Stripe
- Jazzmin (Admin UI)
- widget-tweaks (templates)

## Quick Start (Local)
```bash
# 1) Clone
git clone https://github.com/<your-username>/furniture_shop_backend.git
cd furniture_shop_backend

# 2) Virtualenv (Windows PowerShell)
python -m venv .venv
.venv\Scripts\activate

# 3) Install deps
pip install -r requirements.txt

# 4) Configure environment
  # (create manually)

# 5) DB & run
python manage.py migrate
python manage.py runserver
