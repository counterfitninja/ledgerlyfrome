"""
Run once to populate the database with default content.

    python seed.py

Safe to re-run — it won't overwrite existing data.
"""
from app import app, create_tables
from models import db, SiteConfig, Service, Testimonial, FaqItem, HowItWorksStep, AboutPoint


def seed():
    create_tables()
    with app.app_context():
        _seed_config()
        _seed_services()
        _seed_testimonials()
        _seed_faq()
        _seed_steps()
        _seed_about_points()
        db.session.commit()
    print("Database seeded successfully.")


def _set(key, value):
    """Insert config key only if it doesn't already exist."""
    if not db.session.get(SiteConfig, key):
        db.session.add(SiteConfig(key=key, value=value))


def _seed_config():
    _set("business_name",    "Ledgerly")
    _set("tagline",          "Clean Books. Clear Mind.")
    _set("phone",            "01326 619114")
    _set("email",            "ledgerlyy@gmail.com")
    _set("hours",            "Mon–Fri, 9am–5pm")
    _set("location",         "Frome, Somerset — serving clients across the UK")
    _set("meta_title",       "Ledgerly — Professional Bookkeeping in Frome & across the UK")
    _set("meta_description", "Reliable, remote bookkeeping for sole traders and small limited companies. Fixed-price packages. Based in Frome, Somerset.")
    _set("hero_heading",     "Clean Books.<br>Clear Mind.")
    _set("hero_sub",         "Professional, reliable bookkeeping for UK sole traders and small limited companies.")
    _set("hero_badges",      "100% Remote,UK-wide coverage,Accountant-ready records")
    _set("hero_cta1_label",  "Get a Free Quote")
    _set("hero_cta1_href",   "#contact")
    _set("hero_cta2_label",  "See Our Services")
    _set("hero_cta2_href",   "#services")
    _set("services_heading", "What We Do")
    _set("services_sub",     "Everything your business needs to keep finances on track.")
    _set("about_heading",    "Why Ledgerly?")
    _set("about_sub",        "We take the stress out of your finances so you can focus on what you do best.")
    _set("about_body",       "Ledgerly provides reliable, efficient, and stress-free bookkeeping. We believe good bookkeeping shouldn't be complicated — plain-English communication, fixed transparent pricing, and a dedicated UK-based bookkeeper in your corner.")
    _set("hiw_heading",      "How It Works")
    _set("hiw_sub",          "Getting started is simple. Here's what to expect.")
    _set("reviews_heading",  "What Our Clients Say")
    _set("reviews_sub",      "Real feedback from real businesses across the UK.")
    _set("faq_heading",      "Frequently Asked Questions")
    _set("faq_sub",          "Can't find your answer? Just drop us a message.")
    _set("contact_heading",  "Get in Touch")
    _set("contact_sub",      "Book a free call or drop us a message — we'll get back to you within one business day.")
    _set("footer_copy",      "© 2025 Ledgerly. All rights reserved.")
    _set("formspree_url",    "")


def _seed_services():
    if Service.query.count():
        return
    items = [
        ("📒", "Day-to-Day Bookkeeping",          "Accurate recording of all income and expenses, keeping your books up to date every month."),
        ("🏦", "Bank Reconciliations",             "We match every transaction to your bank statements so nothing slips through the cracks."),
        ("🧾", "VAT Returns",                      "Preparation and submission of VAT returns, ensuring compliance and accuracy."),
        ("🏗️", "CIS Returns",                     "Full support for contractors and subcontractors with Construction Industry Scheme obligations."),
        ("💷", "Payroll Services",                 "Processing payroll and submitting RTI reports to HMRC on time, every time."),
        ("📝", "Self-Assessment Preparation",      "We gather and organise your figures so your accountant can file quickly and accurately."),
        ("🏢", "Limited Company Accounts",         "Year-end accounts preparation for small limited companies, accountant-ready."),
        ("💻", "Software Setup & Support",         "We set up and support QuickBooks, Xero, and other cloud accounting platforms."),
        ("📊", "Management Reports",               "Clear monthly reports showing exactly how your business is performing financially."),
    ]
    for i, (icon, title, desc) in enumerate(items):
        db.session.add(Service(icon=icon, title=title, description=desc, order=i, active=True))


def _seed_testimonials():
    if Testimonial.query.count():
        return
    items = [
        ("Sarah M.",  "Freelance Designer, London",       5, "My books have never been tidier. Ledgerly sorted out months of backlog and keeps everything running smoothly."),
        ("James K.",  "Sole Trader, Manchester",           5, "I dreaded doing my accounts every year. Not any more — everything is just handled."),
        ("Priya L.",  "Ltd Company Director, Birmingham",  5, "Zero stress at year end for the first time ever. My accountant noticed the difference immediately."),
        ("Alex R.",   "Consultant, Bristol",               5, "Completely transformed how organised my finances are. I actually understand my numbers now."),
        ("Emma T.",   "E-commerce Owner, Leeds",           5, "Reduced my bookkeeping headaches massively. Highly recommended for any online business."),
        ("Tom B.",    "Contractor, Edinburgh",             5, "Clear pricing, responsive communication, and they really know their stuff with CIS."),
    ]
    for i, (name, role, stars, text) in enumerate(items):
        db.session.add(Testimonial(name=name, role=role, stars=stars, text=text, order=i, active=True))


def _seed_faq():
    if FaqItem.query.count():
        return
    items = [
        ("What's the difference between a bookkeeper and an accountant?",
         "A bookkeeper records and organises your day-to-day financial transactions. An accountant typically uses that data to file tax returns and give strategic advice. We get your books in shape so your accountant can work faster (and cheaper)."),
        ("Do you work with clients outside Frome?",
         "Absolutely — we're fully remote and work with clients all across the UK. Everything is handled securely online."),
        ("Which accounting software do you use?",
         "We primarily work with QuickBooks and Xero, but we're happy to work with your existing software or help you choose the right one."),
        ("How much does it cost?",
         "Pricing is fixed and tailored to your business based on monthly transaction volume. We'll give you a clear quote before you commit — no hidden fees."),
        ("Can you help if my books are behind?",
         "Yes — catch-up bookkeeping is something we do regularly. We'll work through the backlog and bring everything up to date."),
        ("How do I get started?",
         "Simply fill in the contact form below or give us a call. We'll arrange a free, no-obligation chat to understand your needs."),
    ]
    for i, (q, a) in enumerate(items):
        db.session.add(FaqItem(question=q, answer=a, order=i, active=True))


def _seed_steps():
    if HowItWorksStep.query.count():
        return
    items = [
        ("1", "Get in Touch",     "Fill in the contact form or give us a call. No obligation."),
        ("2", "Tailored Quote",   "We'll prepare a fixed-price quote based on your transaction volume."),
        ("3", "Setup & Onboard",  "We get access to your accounts and begin organising your books."),
        ("4", "Ongoing Support",  "Monthly bookkeeping, reports, and a dedicated point of contact."),
    ]
    for i, (num, title, desc) in enumerate(items):
        db.session.add(HowItWorksStep(number=num, title=title, description=desc, order=i))


def _seed_about_points():
    if AboutPoint.query.count():
        return
    items = [
        ("✅", "No Year-End Surprises",  "Monthly maintenance means nothing piles up."),
        ("💰", "Lower Accountant Fees",  "Clean, organised records reduce your accountant's time."),
        ("🌍", "Fully Remote",           "We work with clients across the UK, all online."),
        ("💬", "Plain-English Advice",   "No jargon. We explain things in a way that makes sense."),
    ]
    for i, (icon, title, desc) in enumerate(items):
        db.session.add(AboutPoint(icon=icon, title=title, description=desc, order=i))


if __name__ == "__main__":
    seed()
