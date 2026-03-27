from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class SiteConfig(db.Model):
    """Key-value store for all site text (business details, section headings, etc.)"""
    __tablename__ = "site_config"
    key   = db.Column(db.String(120), primary_key=True)
    value = db.Column(db.Text, nullable=True, default="")

    def __repr__(self):
        return f"<SiteConfig {self.key}>"


class Service(db.Model):
    __tablename__ = "services"
    id          = db.Column(db.Integer, primary_key=True)
    icon        = db.Column(db.String(10),  nullable=False, default="📒")
    title       = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text,        nullable=False, default="")
    order       = db.Column(db.Integer,     nullable=False, default=0)
    active      = db.Column(db.Boolean,     nullable=False, default=True)


class Testimonial(db.Model):
    __tablename__ = "testimonials"
    id    = db.Column(db.Integer, primary_key=True)
    name  = db.Column(db.String(100), nullable=False)
    role  = db.Column(db.String(200), nullable=False, default="")
    stars = db.Column(db.Integer,     nullable=False, default=5)
    text  = db.Column(db.Text,        nullable=False, default="")
    order = db.Column(db.Integer,     nullable=False, default=0)
    active = db.Column(db.Boolean,    nullable=False, default=True)


class FaqItem(db.Model):
    __tablename__ = "faq_items"
    id       = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text, nullable=False)
    answer   = db.Column(db.Text, nullable=False, default="")
    order    = db.Column(db.Integer, nullable=False, default=0)
    active   = db.Column(db.Boolean, nullable=False, default=True)


class HowItWorksStep(db.Model):
    __tablename__ = "how_it_works_steps"
    id          = db.Column(db.Integer, primary_key=True)
    number      = db.Column(db.String(5),   nullable=False, default="1")
    title       = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text,        nullable=False, default="")
    order       = db.Column(db.Integer,     nullable=False, default=0)


class AboutPoint(db.Model):
    __tablename__ = "about_points"
    id          = db.Column(db.Integer, primary_key=True)
    icon        = db.Column(db.String(10),  nullable=False, default="✅")
    title       = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text,        nullable=False, default="")
    order       = db.Column(db.Integer,     nullable=False, default=0)
