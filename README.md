# Furniture Shop — Django Backend

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-5.2-092E20?logo=django&logoColor=white)
![Stripe](https://img.shields.io/badge/Stripe-payments-635BFF?logo=stripe&logoColor=white)
![License](https://img.shields.io/badge/license-MPL--2.0-brightgreen)

Backend for an online furniture store: product catalog, categories, session cart, orders and checkout, user accounts, and Stripe payments. All configuration comes from environment variables, with no secrets in the code.

## Features

- 🛍️ Catalog with categories and product images
- 🛒 Session-based cart
- 🧾 Orders and checkout flow (delivery & payment method)
- 👤 Accounts: sign up, login/logout, profile, password reset
- 💳 Stripe integration (test mode ready)
- 🎨 Jazzmin admin theme
- ⚙️ `.env`-based configuration via `django-environ`

## Tech stack

Python 3.10+ · Django 5.2 · SQLite (dev) / PostgreSQL (prod) · Stripe · Jazzmin · django-widget-tweaks

## Getting started

```bash
git clone https://github.com/jafarallaberdiyev/online_shop_backend.git
cd online_shop_backend

python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # macOS / Linux

pip install -r requirements.txt
cp .env.example .env            # then fill in your own values

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open http://127.0.0.1:8000/ for the shop and http://127.0.0.1:8000/admin/ for the admin panel.

Password-reset emails are sent over SMTP. Set the `EMAIL_*` variables in `.env`; for Gmail, use an [app password](https://support.google.com/accounts/answer/185833), not your account password.

## Environment variables

See [`.env.example`](.env.example) for the full list: `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`, Stripe keys (`STRIPE_PUBLIC_KEY`, `STRIPE_SECRET_KEY`, `STRIPE_WEBHOOK_SECRET`) and SMTP settings. Use Stripe **test** keys for local development.

## Project structure

```
accounts/        # registration, login, profile
catalog/         # categories and products
cart/            # session cart
templates/orders # orders and checkout
furniture_shop/  # project settings and URLs
deps/            # static assets (CSS, favicons)
```

## License

[Mozilla Public License 2.0](LICENSE)
