# Ledgerly Bookkeeping

Ledgerly is a Flask-based bookkeeping business site with an admin CMS, SQLite storage, a contact form, and static-site generation via Frozen-Flask.

## Stack

- Flask
- Flask-SQLAlchemy
- Flask-Mail
- Microsoft Graph (app auth option for M365)
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

The contact form now supports two delivery methods:

- `MAIL_PROVIDER=smtp` (default): sends via SMTP using Flask-Mail
- `MAIL_PROVIDER=m365_graph`: sends via Microsoft Graph using Entra app credentials (no SMTP AUTH)

Email is only attempted when both are true:

- a business email address is configured in the admin CMS
- the selected provider has all required environment variables

If a provider is not configured, the form still accepts submissions but no mail is sent.

### Provider Selector

| Variable | Purpose | Typical value |
| --- | --- | --- |
| `MAIL_PROVIDER` | Email backend to use | `smtp` or `m365_graph` |

### SMTP Variables

| Variable | Purpose | Typical value |
| --- | --- | --- |
| `MAIL_SERVER` | SMTP host | `smtp.office365.com` or `smtp.gmail.com` |
| `MAIL_PORT` | SMTP port | `587` |
| `MAIL_USE_TLS` | Enable TLS | `true` |
| `MAIL_USERNAME` | Mailbox login | full email address |
| `MAIL_PASSWORD` | SMTP password | account password or app password |

### Microsoft 365 Graph Variables (App Auth)

| Variable | Purpose | Typical value |
| --- | --- | --- |
| `M365_TENANT_ID` | Entra tenant ID | GUID |
| `M365_CLIENT_ID` | App registration client ID | GUID |
| `M365_CLIENT_SECRET` | App registration client secret | secret value |
| `M365_SENDER` | Mailbox to send as | `you@yourdomain.com` |

### Microsoft 365 Example

SMTP mode:

```env
MAIL_PROVIDER=smtp
MAIL_SERVER=smtp.office365.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=you@yourdomain.com
MAIL_PASSWORD=your-m365-password-or-app-password
```

Microsoft Graph app-auth mode (recommended for modern M365 tenants):

```env
MAIL_PROVIDER=m365_graph
M365_TENANT_ID=00000000-0000-0000-0000-000000000000
M365_CLIENT_ID=11111111-1111-1111-1111-111111111111
M365_CLIENT_SECRET=your-app-client-secret
M365_SENDER=you@yourdomain.com
```

Step-by-step: set up Microsoft 365 Graph app-auth (no SMTP)

1. Sign in to Azure portal with an account that can manage Entra app registrations and grant admin consent.
2. Go to Microsoft Entra ID > App registrations > New registration.
3. Enter a name (for example, `ledgerly-contact-mailer`) and create the app.
4. Open the app Overview page and copy values:
	- `Application (client) ID` -> `M365_CLIENT_ID`
	- `Directory (tenant) ID` -> `M365_TENANT_ID`
5. Go to Certificates & secrets > Client secrets > New client secret.
6. Copy the secret Value immediately and store it as `M365_CLIENT_SECRET`.
	The secret value is only shown once.
7. Go to API permissions > Add a permission > Microsoft Graph > Application permissions.
8. Add `Mail.Send`.
9. Click Grant admin consent for your tenant and confirm the permission shows as granted.
10. Choose the mailbox that should send enquiries (for example, `accounts@yourdomain.com`) and set it as `M365_SENDER`.
11. In your app environment, set:

```env
MAIL_PROVIDER=m365_graph
M365_TENANT_ID=<Directory (tenant) ID>
M365_CLIENT_ID=<Application (client) ID>
M365_CLIENT_SECRET=<Client secret Value>
M365_SENDER=<mailbox@yourdomain.com>
```

12. Restart the app so new environment variables are loaded.
13. Submit the contact form and verify delivery in the target inbox and Sent Items of `M365_SENDER`.

Troubleshooting for Graph mode:

- `401`/`invalid_client`: client ID, tenant ID, or client secret value is wrong/expired.
- `403` with Graph permission errors: admin consent has not been granted for `Mail.Send` (Application).
- `404` for user/mailbox: `M365_SENDER` is wrong or mailbox does not exist in the tenant.
- `403` send-as policy errors: Exchange policy is blocking app send-as for that mailbox.

How to get the SMTP details for Microsoft 365:

1. `MAIL_SERVER`: use `smtp.office365.com`.
2. `MAIL_PORT`: use `587`.
3. `MAIL_USE_TLS`: use `true`.
4. `MAIL_USERNAME`: use the full email address of the mailbox that will send the mail.
5. `MAIL_PASSWORD`: use the mailbox password, or an app password if your tenant still supports and requires it.

How to verify the mailbox is allowed to send via SMTP:

1. Sign in to Microsoft 365 Admin Center.
2. Go to Users > Active users.
3. Open the mailbox user.
4. Open the Mail tab.
5. Open Manage email apps.
6. Ensure Authenticated SMTP is enabled for that mailbox.

Notes:

- The mailbox usually needs Authenticated SMTP enabled.
- Some tenants require an app password or a mailbox-specific SMTP AUTH setting.
- Some organisations disable SMTP AUTH tenant-wide in Exchange Online. If the mailbox settings look correct but login still fails, check the Exchange Online SMTP AUTH policy for the tenant.

### Gmail Example

```env
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=youraddress@gmail.com
MAIL_PASSWORD=your-google-app-password
```

How to get the SMTP details for Gmail:

1. `MAIL_SERVER`: use `smtp.gmail.com`.
2. `MAIL_PORT`: use `587`.
3. `MAIL_USE_TLS`: use `true`.
4. `MAIL_USERNAME`: use the full Gmail address that will send the mail.
5. `MAIL_PASSWORD`: create and use a Google App Password.

How to create a Google App Password:

1. Sign in to the Google account that will send the mail.
2. Open Google Account settings.
3. Go to Security.
4. Enable 2-Step Verification if it is not already enabled.
5. Return to Security and open App passwords.
6. Create a new app password and use that generated value as `MAIL_PASSWORD`.

Notes:

- Gmail commonly requires a Google App Password.
- A normal account password often will not work for SMTP.
- If App passwords is not available, it is usually because 2-Step Verification is not enabled or the account is managed by a Google Workspace policy that blocks it.

## Pelican Panel / Egg Configuration

The Pelican egg definition lives in `egg-ledgerlyfrome.json`.

It now exposes these mail-related variables in the panel:

- `MAIL_PROVIDER`
- `MAIL_SERVER`
- `MAIL_PORT`
- `MAIL_USE_TLS`
- `MAIL_USERNAME`
- `MAIL_PASSWORD`
- `M365_TENANT_ID`
- `M365_CLIENT_ID`
- `M365_CLIENT_SECRET`
- `M365_SENDER`

`MAIL_PASSWORD` and `M365_CLIENT_SECRET` are marked as non-viewable in the egg so they are treated as secrets in the panel.

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