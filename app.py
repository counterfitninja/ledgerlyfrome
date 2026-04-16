import os
import json
from collections import defaultdict
from urllib import error as urllib_error
from urllib import parse as urllib_parse
from urllib import request as urllib_request

from flask import (
    Flask, render_template, request, redirect,
    url_for, flash, abort, session,
)
from flask_mail import Mail, Message
from models import (
    db, SiteConfig, Service, Testimonial,
    FaqItem, HowItWorksStep, AboutPoint,
)

app = Flask(__name__)

# ── Database path — reads DATABASE_PATH env var (set by Pelican) ──────────────
_db_path = os.environ.get("DATABASE_PATH", "site.db")
if not os.path.isabs(_db_path):
    _db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), _db_path)
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{_db_path}"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-change-me")
app.config["FREEZER_DESTINATION"] = "_static"
app.config["FREEZER_RELATIVE_URLS"] = True
app.config["STATIC_MODE"] = False  # set to True in freeze.py

# ── Mail (Flask-Mail) ─────────────────────────────────────────────────────────
app.config["MAIL_PROVIDER"] = os.environ.get("MAIL_PROVIDER", "smtp").strip().lower()
app.config["MAIL_SERVER"]   = os.environ.get("MAIL_SERVER", "smtp.office365.com")
app.config["MAIL_PORT"]     = int(os.environ.get("MAIL_PORT", 587))
app.config["MAIL_USE_TLS"]  = os.environ.get("MAIL_USE_TLS", "true").lower() == "true"
app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME", "")
app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD", "")

# Microsoft 365 Graph app auth (recommended when SMTP AUTH is disabled).
app.config["M365_TENANT_ID"] = os.environ.get("M365_TENANT_ID", "")
app.config["M365_CLIENT_ID"] = os.environ.get("M365_CLIENT_ID", "")
app.config["M365_CLIENT_SECRET"] = os.environ.get("M365_CLIENT_SECRET", "")
app.config["M365_SENDER"] = os.environ.get("M365_SENDER", "")

mail = Mail(app)

# ── Admin auth ────────────────────────────────────────────────────────────────
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "")


@app.before_request
def check_admin_auth():
    """Protect all /admin/ routes. Skipped when ADMIN_PASSWORD env var is not set (local dev)."""
    if (
        request.path.startswith("/admin/")
        and request.endpoint not in ("admin_login", "admin_logout")
        and ADMIN_PASSWORD
        and not session.get("admin_logged_in")
    ):
        return redirect(url_for("admin_login", next=request.path))

db.init_app(app)


# ── Helpers ───────────────────────────────────────────────────────────────────

def get_cfg():
    """Return all site config as a defaultdict (missing keys → empty string)."""
    cfg = defaultdict(str)
    for row in SiteConfig.query.all():
        cfg[row.key] = row.value or ""
    return cfg


def set_cfg(key, value):
    row = db.session.get(SiteConfig, key)
    if row:
        row.value = value
    else:
        db.session.add(SiteConfig(key=key, value=value))


def site_context():
    """Build the full context dict used by the public site template."""
    cfg = get_cfg()
    return dict(
        cfg=cfg,
        services=Service.query.filter_by(active=True).order_by(Service.order).all(),
        testimonials=Testimonial.query.filter_by(active=True).order_by(Testimonial.order).all(),
        faq_items=FaqItem.query.filter_by(active=True).order_by(FaqItem.order).all(),
        steps=HowItWorksStep.query.order_by(HowItWorksStep.order).all(),
        about_points=AboutPoint.query.order_by(AboutPoint.order).all(),
    )


def _can_send_email():
    provider = app.config.get("MAIL_PROVIDER", "smtp")
    if provider == "m365_graph":
        return all([
            app.config.get("M365_TENANT_ID"),
            app.config.get("M365_CLIENT_ID"),
            app.config.get("M365_CLIENT_SECRET"),
            app.config.get("M365_SENDER"),
        ])
    return bool(app.config.get("MAIL_USERNAME"))


def _missing_mail_requirements():
    provider = app.config.get("MAIL_PROVIDER", "smtp")
    if provider == "m365_graph":
        required = ["M365_TENANT_ID", "M365_CLIENT_ID", "M365_CLIENT_SECRET", "M365_SENDER"]
    else:
        required = ["MAIL_USERNAME", "MAIL_PASSWORD", "MAIL_SERVER", "MAIL_PORT"]
    return [key for key in required if not app.config.get(key)]


def _log_mail_config_health():
    provider = app.config.get("MAIL_PROVIDER", "smtp")
    missing = _missing_mail_requirements()
    if missing:
        app.logger.warning(
            "Mail config incomplete for provider '%s'; missing: %s",
            provider,
            ", ".join(missing),
        )
    else:
        app.logger.info("Mail config ready for provider '%s'", provider)


def _send_via_graph(subject, body, to_addr, reply_to):
    tenant_id = app.config["M365_TENANT_ID"]
    client_id = app.config["M365_CLIENT_ID"]
    client_secret = app.config["M365_CLIENT_SECRET"]
    sender = app.config["M365_SENDER"]

    token_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
    token_payload = urllib_parse.urlencode({
        "client_id": client_id,
        "client_secret": client_secret,
        "scope": "https://graph.microsoft.com/.default",
        "grant_type": "client_credentials",
    }).encode("utf-8")
    token_request = urllib_request.Request(
        token_url,
        data=token_payload,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        method="POST",
    )

    try:
        with urllib_request.urlopen(token_request, timeout=15) as token_response:
            token_json = json.loads(token_response.read().decode("utf-8"))
    except urllib_error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Failed to fetch Graph token: {detail}") from exc

    access_token = token_json.get("access_token")
    if not access_token:
        raise RuntimeError("Failed to fetch Graph token: access_token missing")

    graph_url = f"https://graph.microsoft.com/v1.0/users/{urllib_parse.quote(sender)}/sendMail"
    graph_payload = {
        "message": {
            "subject": subject,
            "body": {"contentType": "Text", "content": body},
            "toRecipients": [{"emailAddress": {"address": to_addr}}],
            "replyTo": [{"emailAddress": {"address": reply_to}}],
        },
        "saveToSentItems": True,
    }
    graph_request = urllib_request.Request(
        graph_url,
        data=json.dumps(graph_payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urllib_request.urlopen(graph_request, timeout=15):
            return
    except urllib_error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Graph sendMail failed: {detail}") from exc


def send_contact_email(name, email, phone, business, message, to_addr):
    subject = f"New enquiry from {name}"
    body = (
        f"New enquiry from {name}\n\n"
        f"Email:    {email}\n"
        f"Phone:    {phone or '—'}\n"
        f"Business: {business or '—'}\n\n"
        f"Message:\n{message or '(none)'}"
    )

    provider = app.config.get("MAIL_PROVIDER", "smtp")
    if provider == "m365_graph":
        _send_via_graph(subject=subject, body=body, to_addr=to_addr, reply_to=email)
        return

    msg = Message(
        subject=subject,
        sender=app.config["MAIL_USERNAME"],
        recipients=[to_addr],
        reply_to=email,
        body=body,
    )
    mail.send(msg)


# ── Public site ───────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("site/index.html", **site_context())


@app.route("/contact/submit/", methods=["GET", "POST"])
def contact_submit():
    if request.method == "GET":
        return redirect(url_for("index") + "#contact")
    name     = request.form.get("name", "").strip()
    email    = request.form.get("email", "").strip()
    phone    = request.form.get("phone", "").strip()
    business = request.form.get("business", "").strip()
    message  = request.form.get("message", "").strip()

    if not name or not email:
        flash("Please fill in your name and email address.", "error")
        return redirect(url_for("index") + "#contact")

    cfg = get_cfg()
    to_addr = cfg["email"]

    if to_addr and _can_send_email():
        try:
            send_contact_email(
                name=name,
                email=email,
                phone=phone,
                business=business,
                message=message,
                to_addr=to_addr,
            )
        except Exception as exc:
            app.logger.error("Contact form mail failed: %s", exc)
            flash("Sorry, there was a problem sending your message. Please email us directly.", "error")
            return redirect(url_for("index") + "#contact")
    else:
        if not to_addr:
            app.logger.warning("Contact form mail skipped: business email recipient is not configured")
        missing = _missing_mail_requirements()
        if missing:
            app.logger.warning(
                "Contact form mail skipped: provider '%s' missing: %s",
                app.config.get("MAIL_PROVIDER", "smtp"),
                ", ".join(missing),
            )

    flash(f"Thanks {name}! We'll be in touch within one business day.", "success")
    return redirect(url_for("index") + "#contact")


# ── Admin — dashboard ─────────────────────────────────────────────────────────

@app.route("/admin/login/", methods=["GET", "POST"])
def admin_login():
    if not ADMIN_PASSWORD:
        return redirect(url_for("admin_dashboard"))
    if request.method == "POST":
        if request.form.get("password") == ADMIN_PASSWORD:
            session["admin_logged_in"] = True
            return redirect(request.args.get("next") or url_for("admin_dashboard"))
        flash("Incorrect password.", "error")
    return render_template("admin/login.html")


@app.route("/admin/logout/")
def admin_logout():
    session.pop("admin_logged_in", None)
    return redirect(url_for("admin_login"))


@app.route("/admin/")
def admin_dashboard():
    counts = {
        "services":     Service.query.count(),
        "testimonials": Testimonial.query.count(),
        "faq":          FaqItem.query.count(),
        "steps":        HowItWorksStep.query.count(),
        "about_points": AboutPoint.query.count(),
    }
    return render_template("admin/dashboard.html", counts=counts)


# ── Admin — business settings ─────────────────────────────────────────────────

BUSINESS_FIELDS = [
    # (key, label, type, help_text)
    ("business_name",     "Business Name",        "text",     ""),
    ("meta_title",        "Page Title (SEO)",     "text",     "Shown in Google results and browser tab"),
    ("meta_description",  "Meta Description",     "textarea", "1–2 sentence summary for Google"),
    ("tagline",           "Tagline",              "text",     "Short phrase shown in footer"),
    ("phone",             "Phone",                "text",     ""),
    ("email",             "Email",                "text",     ""),
    ("hours",             "Office Hours",         "text",     "e.g. Mon–Fri, 9am–5pm"),
    ("location",          "Location / Area",      "text",     "e.g. Frome, Somerset — serving clients UK-wide"),
    ("hero_heading",      "Hero Heading",         "text",     "HTML allowed — use <br> for line break"),
    ("hero_sub",          "Hero Sub-heading",     "textarea", ""),
    ("hero_badges",       "Hero Badges",          "text",     "Comma-separated, e.g. 100% Remote,UK-wide"),
    ("services_heading",  "Services Heading",     "text",     ""),
    ("services_sub",      "Services Sub-heading", "text",     ""),
    ("about_heading",     "About Heading",        "text",     ""),
    ("about_sub",         "About Sub-heading",    "text",     ""),
    ("about_body",        "About Body Text",      "textarea", ""),
    ("hiw_heading",       "How It Works Heading", "text",     ""),
    ("hiw_sub",           "How It Works Sub",     "text",     ""),
    ("reviews_heading",   "Reviews Heading",      "text",     ""),
    ("reviews_sub",       "Reviews Sub-heading",  "text",     ""),
    ("faq_heading",       "FAQ Heading",          "text",     ""),
    ("faq_sub",           "FAQ Sub-heading",      "text",     ""),
    ("contact_heading",   "Contact Heading",      "text",     ""),
    ("contact_sub",       "Contact Sub-heading",  "text",     ""),
    ("footer_copy",       "Footer Copyright",     "text",     ""),
    ("formspree_url",     "Formspree URL",        "text",     "Paste your Formspree form URL here for static-site contact form support (e.g. https://formspree.io/f/abc123)"),
]


@app.route("/admin/business/", methods=["GET", "POST"])
def admin_business():
    if request.method == "POST":
        for key, *_ in BUSINESS_FIELDS:
            set_cfg(key, request.form.get(key, ""))
        db.session.commit()
        flash("Business settings saved.", "success")
        return redirect(url_for("admin_business"))
    cfg = get_cfg()
    return render_template("admin/business.html", cfg=cfg, fields=BUSINESS_FIELDS)


# ── Admin — services ──────────────────────────────────────────────────────────

@app.route("/admin/services/")
def admin_services():
    items = Service.query.order_by(Service.order).all()
    return render_template("admin/services.html", items=items)


@app.route("/admin/services/new/", methods=["GET", "POST"])
def admin_service_new():
    if request.method == "POST":
        db.session.add(Service(
            icon=request.form.get("icon", "📒"),
            title=request.form["title"],
            description=request.form.get("description", ""),
            order=int(request.form.get("order", 0)),
            active="active" in request.form,
        ))
        db.session.commit()
        flash("Service added.", "success")
        return redirect(url_for("admin_services"))
    return render_template("admin/item_form.html",
        section="services", section_label="Service",
        item=None, back_url=url_for("admin_services"),
        fields=_service_fields(),
    )


@app.route("/admin/services/<int:item_id>/", methods=["GET", "POST"])
def admin_service_edit(item_id):
    item = Service.query.get_or_404(item_id)
    if request.method == "POST":
        item.icon        = request.form.get("icon", "📒")
        item.title       = request.form["title"]
        item.description = request.form.get("description", "")
        item.order       = int(request.form.get("order", 0))
        item.active      = "active" in request.form
        db.session.commit()
        flash("Service updated.", "success")
        return redirect(url_for("admin_services"))
    return render_template("admin/item_form.html",
        section="services", section_label="Service",
        item=item, back_url=url_for("admin_services"),
        delete_url=url_for("admin_service_delete", item_id=item_id),
        fields=_service_fields(item),
    )


@app.route("/admin/services/<int:item_id>/delete/", methods=["POST"])
def admin_service_delete(item_id):
    db.session.delete(Service.query.get_or_404(item_id))
    db.session.commit()
    flash("Service deleted.", "success")
    return redirect(url_for("admin_services"))


def _service_fields(item=None):
    return [
        {"name": "icon",        "label": "Icon (emoji)",   "type": "text",     "value": getattr(item, "icon", "📒"),  "help": "Paste an emoji"},
        {"name": "title",       "label": "Title",          "type": "text",     "value": getattr(item, "title", ""),   "help": "", "required": True},
        {"name": "description", "label": "Description",    "type": "textarea", "value": getattr(item, "description", ""), "help": ""},
        {"name": "order",       "label": "Display Order",  "type": "number",   "value": getattr(item, "order", 0),   "help": "Lower = shown first"},
        {"name": "active",      "label": "Visible on site","type": "checkbox", "value": getattr(item, "active", True), "help": ""},
    ]


# ── Admin — testimonials ──────────────────────────────────────────────────────

@app.route("/admin/testimonials/")
def admin_testimonials():
    items = Testimonial.query.order_by(Testimonial.order).all()
    return render_template("admin/testimonials.html", items=items)


@app.route("/admin/testimonials/new/", methods=["GET", "POST"])
def admin_testimonial_new():
    if request.method == "POST":
        db.session.add(Testimonial(
            name=request.form["name"],
            role=request.form.get("role", ""),
            stars=int(request.form.get("stars", 5)),
            text=request.form.get("text", ""),
            order=int(request.form.get("order", 0)),
            active="active" in request.form,
        ))
        db.session.commit()
        flash("Testimonial added.", "success")
        return redirect(url_for("admin_testimonials"))
    return render_template("admin/item_form.html",
        section="testimonials", section_label="Testimonial",
        item=None, back_url=url_for("admin_testimonials"),
        fields=_testimonial_fields(),
    )


@app.route("/admin/testimonials/<int:item_id>/", methods=["GET", "POST"])
def admin_testimonial_edit(item_id):
    item = Testimonial.query.get_or_404(item_id)
    if request.method == "POST":
        item.name   = request.form["name"]
        item.role   = request.form.get("role", "")
        item.stars  = int(request.form.get("stars", 5))
        item.text   = request.form.get("text", "")
        item.order  = int(request.form.get("order", 0))
        item.active = "active" in request.form
        db.session.commit()
        flash("Testimonial updated.", "success")
        return redirect(url_for("admin_testimonials"))
    return render_template("admin/item_form.html",
        section="testimonials", section_label="Testimonial",
        item=item, back_url=url_for("admin_testimonials"),
        delete_url=url_for("admin_testimonial_delete", item_id=item_id),
        fields=_testimonial_fields(item),
    )


@app.route("/admin/testimonials/<int:item_id>/delete/", methods=["POST"])
def admin_testimonial_delete(item_id):
    db.session.delete(Testimonial.query.get_or_404(item_id))
    db.session.commit()
    flash("Testimonial deleted.", "success")
    return redirect(url_for("admin_testimonials"))


def _testimonial_fields(item=None):
    return [
        {"name": "name",   "label": "Name",          "type": "text",     "value": getattr(item, "name", ""),   "help": "", "required": True},
        {"name": "role",   "label": "Role / Location","type": "text",     "value": getattr(item, "role", ""),   "help": "e.g. Freelance Designer, London"},
        {"name": "stars",  "label": "Star Rating",    "type": "number",   "value": getattr(item, "stars", 5),   "help": "1–5"},
        {"name": "text",   "label": "Review Text",    "type": "textarea", "value": getattr(item, "text", ""),   "help": ""},
        {"name": "order",  "label": "Display Order",  "type": "number",   "value": getattr(item, "order", 0),   "help": "Lower = shown first"},
        {"name": "active", "label": "Visible on site","type": "checkbox", "value": getattr(item, "active", True), "help": ""},
    ]


# ── Admin — FAQ ───────────────────────────────────────────────────────────────

@app.route("/admin/faq/")
def admin_faq():
    items = FaqItem.query.order_by(FaqItem.order).all()
    return render_template("admin/faq.html", items=items)


@app.route("/admin/faq/new/", methods=["GET", "POST"])
def admin_faq_new():
    if request.method == "POST":
        db.session.add(FaqItem(
            question=request.form["question"],
            answer=request.form.get("answer", ""),
            order=int(request.form.get("order", 0)),
            active="active" in request.form,
        ))
        db.session.commit()
        flash("FAQ item added.", "success")
        return redirect(url_for("admin_faq"))
    return render_template("admin/item_form.html",
        section="faq", section_label="FAQ Item",
        item=None, back_url=url_for("admin_faq"),
        fields=_faq_fields(),
    )


@app.route("/admin/faq/<int:item_id>/", methods=["GET", "POST"])
def admin_faq_edit(item_id):
    item = FaqItem.query.get_or_404(item_id)
    if request.method == "POST":
        item.question = request.form["question"]
        item.answer   = request.form.get("answer", "")
        item.order    = int(request.form.get("order", 0))
        item.active   = "active" in request.form
        db.session.commit()
        flash("FAQ item updated.", "success")
        return redirect(url_for("admin_faq"))
    return render_template("admin/item_form.html",
        section="faq", section_label="FAQ Item",
        item=item, back_url=url_for("admin_faq"),
        delete_url=url_for("admin_faq_delete", item_id=item_id),
        fields=_faq_fields(item),
    )


@app.route("/admin/faq/<int:item_id>/delete/", methods=["POST"])
def admin_faq_delete(item_id):
    db.session.delete(FaqItem.query.get_or_404(item_id))
    db.session.commit()
    flash("FAQ item deleted.", "success")
    return redirect(url_for("admin_faq"))


def _faq_fields(item=None):
    return [
        {"name": "question", "label": "Question", "type": "textarea", "value": getattr(item, "question", ""), "help": "", "required": True},
        {"name": "answer",   "label": "Answer",   "type": "textarea", "value": getattr(item, "answer", ""),   "help": ""},
        {"name": "order",    "label": "Order",    "type": "number",   "value": getattr(item, "order", 0),     "help": "Lower = shown first"},
        {"name": "active",   "label": "Visible",  "type": "checkbox", "value": getattr(item, "active", True), "help": ""},
    ]


# ── Admin — How It Works steps ────────────────────────────────────────────────

@app.route("/admin/steps/")
def admin_steps():
    items = HowItWorksStep.query.order_by(HowItWorksStep.order).all()
    return render_template("admin/steps.html", items=items)


@app.route("/admin/steps/new/", methods=["GET", "POST"])
def admin_step_new():
    if request.method == "POST":
        db.session.add(HowItWorksStep(
            number=request.form.get("number", "1"),
            title=request.form["title"],
            description=request.form.get("description", ""),
            order=int(request.form.get("order", 0)),
        ))
        db.session.commit()
        flash("Step added.", "success")
        return redirect(url_for("admin_steps"))
    return render_template("admin/item_form.html",
        section="steps", section_label="Step",
        item=None, back_url=url_for("admin_steps"),
        fields=_step_fields(),
    )


@app.route("/admin/steps/<int:item_id>/", methods=["GET", "POST"])
def admin_step_edit(item_id):
    item = HowItWorksStep.query.get_or_404(item_id)
    if request.method == "POST":
        item.number      = request.form.get("number", "1")
        item.title       = request.form["title"]
        item.description = request.form.get("description", "")
        item.order       = int(request.form.get("order", 0))
        db.session.commit()
        flash("Step updated.", "success")
        return redirect(url_for("admin_steps"))
    return render_template("admin/item_form.html",
        section="steps", section_label="Step",
        item=item, back_url=url_for("admin_steps"),
        delete_url=url_for("admin_step_delete", item_id=item_id),
        fields=_step_fields(item),
    )


@app.route("/admin/steps/<int:item_id>/delete/", methods=["POST"])
def admin_step_delete(item_id):
    db.session.delete(HowItWorksStep.query.get_or_404(item_id))
    db.session.commit()
    flash("Step deleted.", "success")
    return redirect(url_for("admin_steps"))


def _step_fields(item=None):
    return [
        {"name": "number",      "label": "Step Number", "type": "text",     "value": getattr(item, "number", "1"),      "help": "Displayed in the circle"},
        {"name": "title",       "label": "Title",       "type": "text",     "value": getattr(item, "title", ""),        "help": "", "required": True},
        {"name": "description", "label": "Description", "type": "textarea", "value": getattr(item, "description", ""),  "help": ""},
        {"name": "order",       "label": "Order",       "type": "number",   "value": getattr(item, "order", 0),         "help": "Lower = shown first"},
    ]


# ── Admin — About ─────────────────────────────────────────────────────────────

@app.route("/admin/about/")
def admin_about():
    items = AboutPoint.query.order_by(AboutPoint.order).all()
    return render_template("admin/about.html", items=items)


@app.route("/admin/about/points/new/", methods=["GET", "POST"])
def admin_about_point_new():
    if request.method == "POST":
        db.session.add(AboutPoint(
            icon=request.form.get("icon", "✅"),
            title=request.form["title"],
            description=request.form.get("description", ""),
            order=int(request.form.get("order", 0)),
        ))
        db.session.commit()
        flash("About point added.", "success")
        return redirect(url_for("admin_about"))
    return render_template("admin/item_form.html",
        section="about_points", section_label="About Point",
        item=None, back_url=url_for("admin_about"),
        fields=_about_point_fields(),
    )


@app.route("/admin/about/points/<int:item_id>/", methods=["GET", "POST"])
def admin_about_point_edit(item_id):
    item = AboutPoint.query.get_or_404(item_id)
    if request.method == "POST":
        item.icon        = request.form.get("icon", "✅")
        item.title       = request.form["title"]
        item.description = request.form.get("description", "")
        item.order       = int(request.form.get("order", 0))
        db.session.commit()
        flash("About point updated.", "success")
        return redirect(url_for("admin_about"))
    return render_template("admin/item_form.html",
        section="about_points", section_label="About Point",
        item=item, back_url=url_for("admin_about"),
        delete_url=url_for("admin_about_point_delete", item_id=item_id),
        fields=_about_point_fields(item),
    )


@app.route("/admin/about/points/<int:item_id>/delete/", methods=["POST"])
def admin_about_point_delete(item_id):
    db.session.delete(AboutPoint.query.get_or_404(item_id))
    db.session.commit()
    flash("About point deleted.", "success")
    return redirect(url_for("admin_about"))


def _about_point_fields(item=None):
    return [
        {"name": "icon",        "label": "Icon (emoji)", "type": "text",     "value": getattr(item, "icon", "✅"),       "help": ""},
        {"name": "title",       "label": "Title",        "type": "text",     "value": getattr(item, "title", ""),        "help": "", "required": True},
        {"name": "description", "label": "Description",  "type": "textarea", "value": getattr(item, "description", ""),  "help": ""},
        {"name": "order",       "label": "Order",        "type": "number",   "value": getattr(item, "order", 0),         "help": ""},
    ]


# ── Admin — generate static site ─────────────────────────────────────────────

@app.route("/admin/generate/", methods=["POST"])
def admin_generate():
    try:
        from flask_frozen import Freezer
        freezer = Freezer(app)
        with app.app_context():
            freezer.freeze()
        flash("Static site generated in the _static/ folder. You can now deploy that folder.", "success")
    except Exception as exc:
        flash(f"Error generating static site: {exc}", "error")
    return redirect(url_for("admin_dashboard"))


# ── Startup ───────────────────────────────────────────────────────────────────

def create_tables():
    with app.app_context():
        db.create_all()


create_tables()
_log_mail_config_health()

if __name__ == "__main__":
    app.run(debug=True, port=5000)
