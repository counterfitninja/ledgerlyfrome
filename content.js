/**
 * ============================================================
 *  SITE CONTENT — edit this file to update your website text
 * ============================================================
 */

const SITE = {

  /* ── Business Details ────────────────────────────────── */
  business: {
    name:     "Ledgerly",
    tagline:  "Clean Books. Clear Mind.",
    subtitle: "Professional, reliable bookkeeping for UK sole traders and small limited companies",
    phone:    "01326 619114",
    email:    "ledgerlyy@gmail.com",
    hours:    "Mon–Fri, 9am–5pm",
    location: "Frome, Somerset — serving clients across the UK",
    area:     "UK-wide (remote) · Local to Frome &amp; Somerset",
  },

  /* ── Navigation ──────────────────────────────────────── */
  nav: {
    links: [
      { label: "Services",     href: "#services"    },
      { label: "About",        href: "#about"       },
      { label: "How It Works", href: "#how-it-works"},
      { label: "Reviews",      href: "#reviews"     },
      { label: "FAQ",          href: "#faq"         },
      { label: "Contact",      href: "#contact"     },
    ],
    cta: { label: "Get a Free Quote", href: "#contact" },
  },

  /* ── Hero Section ────────────────────────────────────── */
  hero: {
    heading:   "Clean Books.<br>Clear Mind.",
    sub:       "Professional, reliable bookkeeping for UK sole traders and small limited companies.",
    badges:    ["100% Remote", "UK-wide coverage", "Accountant-ready records"],
    cta1:      { label: "Get a Free Quote", href: "#contact" },
    cta2:      { label: "See Our Services", href: "#services" },
  },

  /* ── Services ────────────────────────────────────────── */
  services: {
    heading: "What We Do",
    sub:     "Everything your business needs to keep finances on track.",
    items: [
      {
        icon: "📒",
        title: "Day-to-Day Bookkeeping",
        desc:  "Accurate recording of all income and expenses, keeping your books up to date every month.",
      },
      {
        icon: "🏦",
        title: "Bank Reconciliations",
        desc:  "We match every transaction to your bank statements so nothing slips through the cracks.",
      },
      {
        icon: "🧾",
        title: "VAT Returns",
        desc:  "Preparation and submission of VAT returns, ensuring compliance and accuracy.",
      },
      {
        icon: "🏗️",
        title: "CIS Returns",
        desc:  "Full support for contractors and subcontractors with Construction Industry Scheme obligations.",
      },
      {
        icon: "💷",
        title: "Payroll Services",
        desc:  "Processing payroll and submitting RTI reports to HMRC on time, every time.",
      },
      {
        icon: "📝",
        title: "Self-Assessment Preparation",
        desc:  "We gather and organise your figures so your accountant can file quickly and accurately.",
      },
      {
        icon: "🏢",
        title: "Limited Company Accounts",
        desc:  "Year-end accounts preparation for small limited companies, accountant-ready.",
      },
      {
        icon: "💻",
        title: "Software Setup &amp; Support",
        desc:  "We set up and support QuickBooks, Xero, and other cloud accounting platforms.",
      },
      {
        icon: "📊",
        title: "Management Reports",
        desc:  "Clear monthly reports showing exactly how your business is performing financially.",
      },
    ],
  },

  /* ── About / Why Us ──────────────────────────────────── */
  about: {
    heading: "Why Ledgerly?",
    sub:     "We take the stress out of your finances so you can focus on what you do best.",
    body:    "Ledgerly provides reliable, efficient, and stress-free bookkeeping. We believe good bookkeeping shouldn't be complicated — plain-English communication, fixed transparent pricing, and a dedicated UK-based bookkeeper in your corner.",
    points: [
      { icon: "✅", title: "No Year-End Surprises",   desc: "Monthly maintenance means nothing piles up."        },
      { icon: "💰", title: "Lower Accountant Fees",   desc: "Clean, organised records reduce your accountant's time." },
      { icon: "🌍", title: "Fully Remote",            desc: "We work with clients across the UK, all online."    },
      { icon: "💬", title: "Plain-English Advice",    desc: "No jargon. We explain things in a way that makes sense." },
    ],
  },

  /* ── How It Works ────────────────────────────────────── */
  howItWorks: {
    heading: "How It Works",
    sub:     "Getting started is simple. Here's what to expect.",
    steps: [
      { num: "1", title: "Get in Touch",          desc: "Fill in the contact form or give us a call. No obligation." },
      { num: "2", title: "Tailored Quote",        desc: "We'll prepare a fixed-price quote based on your transaction volume." },
      { num: "3", title: "Setup &amp; Onboard",  desc: "We get access to your accounts and begin organising your books." },
      { num: "4", title: "Ongoing Support",       desc: "Monthly bookkeeping, reports, and a dedicated point of contact." },
    ],
  },

  /* ── Testimonials ────────────────────────────────────── */
  reviews: {
    heading: "What Our Clients Say",
    sub:     "Real feedback from real businesses across the UK.",
    items: [
      { name: "Sarah M.",  role: "Freelance Designer, London",          stars: 5, text: "My books have never been tidier. Ledgerly sorted out months of backlog and keeps everything running smoothly." },
      { name: "James K.",  role: "Sole Trader, Manchester",             stars: 5, text: "I dreaded doing my accounts every year. Not any more — everything is just handled." },
      { name: "Priya L.",  role: "Ltd Company Director, Birmingham",    stars: 5, text: "Zero stress at year end for the first time ever. My accountant noticed the difference immediately." },
      { name: "Alex R.",   role: "Consultant, Bristol",                 stars: 5, text: "Completely transformed how organised my finances are. I actually understand my numbers now." },
      { name: "Emma T.",   role: "E-commerce Owner, Leeds",             stars: 5, text: "Reduced my bookkeeping headaches massively. Highly recommended for any online business." },
      { name: "Tom B.",    role: "Contractor, Edinburgh",               stars: 5, text: "Clear pricing, responsive communication, and they really know their stuff with CIS." },
    ],
  },

  /* ── FAQ ─────────────────────────────────────────────── */
  faq: {
    heading: "Frequently Asked Questions",
    sub:     "Can't find your answer? Just drop us a message.",
    items: [
      {
        q: "What's the difference between a bookkeeper and an accountant?",
        a: "A bookkeeper records and organises your day-to-day financial transactions. An accountant typically uses that data to file tax returns and give strategic advice. We get your books in shape so your accountant can work faster (and cheaper).",
      },
      {
        q: "Do you work with clients outside Frome?",
        a: "Absolutely — we're fully remote and work with clients all across the UK. Everything is handled securely online.",
      },
      {
        q: "Which accounting software do you use?",
        a: "We primarily work with QuickBooks and Xero, but we're happy to work with your existing software or help you choose the right one.",
      },
      {
        q: "How much does it cost?",
        a: "Pricing is fixed and tailored to your business based on monthly transaction volume. We'll give you a clear quote before you commit — no hidden fees.",
      },
      {
        q: "Can you help if my books are behind?",
        a: "Yes — catch-up bookkeeping is something we do regularly. We'll work through the backlog and bring everything up to date.",
      },
      {
        q: "How do I get started?",
        a: "Simply fill in the contact form below or give us a call. We'll arrange a free, no-obligation chat to understand your needs.",
      },
    ],
  },

  /* ── Contact ─────────────────────────────────────────── */
  contact: {
    heading: "Get in Touch",
    sub:     "Book a free call or drop us a message — we'll get back to you within one business day.",
    formFields: [
      { name: "name",     label: "Your Name",     type: "text",  required: true  },
      { name: "email",    label: "Email Address", type: "email", required: true  },
      { name: "phone",    label: "Phone Number",  type: "tel",   required: false },
      { name: "business", label: "Business Type", type: "text",  required: false, placeholder: "e.g. Sole trader, Ltd company" },
      { name: "message",  label: "How can we help?", type: "textarea", required: false },
    ],
    submitLabel: "Send Message",
  },

  /* ── Footer ──────────────────────────────────────────── */
  footer: {
    tagline: "Clean Books. Clear Mind.",
    copy:    "&copy; 2025 Ledgerly. All rights reserved.",
  },

};
