# Ledgerly Bookkeeping

Ledgerly is a Flask-based bookkeeping business site with an admin CMS, SQLite storage, a contact form, and static-site generation via Frozen-Flask.

## Stack

- Flask
- Flask-SQLAlchemy
- Flask-Mail
- Frozen-Flask
- SQLite
- Gunicorn

## Local Development

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Copy `.env.example` to `.env` or set the environment variables directly.
4. Run the app:

```bash
python app.py
```

The app reads configuration from environment variables with sensible defaults for local development.

## Core Environment Variables

| Variable | Purpose | Default |
| --- | --- | --- |
| `SECRET_KEY` | Flask session secret | `dev-change-me` in code |
| `ADMIN_PASSWORD` | Password for `/admin/` | blank |
| `DATABASE_PATH` | SQLite database path | `site.db` |
| `PORT` | HTTP port for Gunicorn / hosting | `8081` |

## Contact Form Email

The contact form sends email through SMTP using Flask-Mail. Email is only attempted when both of these are present:

- a business email address is configured in the admin CMS
- `MAIL_USERNAME` is set in the environment

If SMTP is not configured, the form still accepts submissions but the app will not send mail.

### SMTP Variables

| Variable | Purpose | Typical value |
| --- | --- | --- |
| `MAIL_SERVER` | SMTP host | `smtp.office365.com` or `smtp.gmail.com` |
| `MAIL_PORT` | SMTP port | `587` |
| `MAIL_USE_TLS` | Enable TLS | `true` |
| `MAIL_USERNAME` | Mailbox login | full email address |
| `MAIL_PASSWORD` | SMTP password | account password or app password |

### Microsoft 365 Example

```env
MAIL_SERVER=smtp.office365.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=you@yourdomain.com
MAIL_PASSWORD=your-m365-password-or-app-password
```

Notes:

- The mailbox usually needs Authenticated SMTP enabled.
- Some tenants require an app password or a mailbox-specific SMTP AUTH setting.

### Gmail Example

```env
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=youraddress@gmail.com
MAIL_PASSWORD=your-google-app-password
```

Notes:

- Gmail commonly requires a Google App Password.
- A normal account password often will not work for SMTP.

## Pelican Panel / Egg Configuration

The Pelican egg definition lives in `egg-ledgerlyfrome.json`.

It now exposes these mail-related variables in the panel:

- `MAIL_SERVER`
- `MAIL_PORT`
- `MAIL_USE_TLS`
- `MAIL_USERNAME`
- `MAIL_PASSWORD`

`MAIL_PASSWORD` is marked as non-viewable in the egg so it is treated as a secret in the panel.

Other deployment variables already supported by the egg include:

- `GIT_ADDRESS`
- `BRANCH`
- `USERNAME`
- `ACCESS_TOKEN`
- `AUTO_UPDATE`
- `REQUIREMENTS_FILE`
- `USER_UPLOAD`

## Pelican Deployment Notes

The startup flow is:

1. install Python dependencies from `requirements.txt`
2. seed the SQLite database on first run if the database file does not exist
3. start Gunicorn via `startup.sh`

When deploying through Pelican, set at minimum:

- `ADMIN_PASSWORD`
- `SECRET_KEY`

Set the SMTP variables as well if you want the contact form to send email.