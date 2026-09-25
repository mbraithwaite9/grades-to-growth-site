#!/usr/bin/env python3
"""
From Grades to Growth — static site generator.

Run:  python3 build.py
Out:  ./site/   (this is the folder Netlify publishes)

Single-page site. Everything the page says lives in this file (or in
assets/), so a change here rebuilds the page. Edit the data below, re-run,
commit.

The "Stay Updated" form submits straight to Netlify Forms (data-netlify
on the <form>, plus an AJAX POST to "/" so the page doesn't reload).
Submissions land in the Netlify dashboard for this site, with optional
email notifications — no database needed. (An earlier version of this
form also wrote to a Supabase table that Lovable had auto-provisioned
for the original site; that write was removed since nobody had confirmed
access to that Supabase project.)
"""

import os, shutil, hashlib, datetime

# ---------------------------------------------------------------- SETTINGS
BASE = "https://fromgradestogrowth.com"   # change here if the domain changes
OUT = "site"
SITE_NAME = "From Grades to Growth"
REGISTER_URL = "https://txoasdni.formester.com/f/6oq4lOZ4D"
BUILT = datetime.date.today().isoformat()

CSS_SRC = os.path.join("assets", "css", "site.css")


def css_name():
    h = hashlib.sha256(open(CSS_SRC, "rb").read()).hexdigest()[:10]
    return f"site.{h}.css"


# ---------------------------------------------------------------- ICONS
# Minimal inline SVGs, sized to match lucide-react's 24x24/stroke-2 look.
def icon(name, cls=""):
    paths = {
        "users": '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>',
        "arrow-right": '<path d="M5 12h14"/><path d="m12 5 7 7-7 7"/>',
        "arrow-down": '<path d="M12 5v14"/><path d="m19 12-7 7-7-7"/>',
        "brain": '<path d="M12 5a3 3 0 1 0-5.997.125 4 4 0 0 0-2.526 5.77 4 4 0 0 0 .556 6.588A4 4 0 1 0 12 18Z"/><path d="M12 5a3 3 0 1 1 5.997.125 4 4 0 0 1 2.526 5.77 4 4 0 0 1-.556 6.588A4 4 0 1 1 12 18Z"/>',
        "target": '<circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/>',
        "book-open-check": '<path d="M8 3H2v15h7c1.7 0 3 1.3 3 3V7c0-2.2-1.8-4-4-4Z"/><path d="m16 12 2 2 4-4"/><path d="M22 6V3h-6c-2.2 0-4 1.8-4 4"/><path d="M22 18h-7a3 3 0 0 0-3 3"/>',
        "sparkles": '<path d="M9.937 15.5A2 2 0 0 0 8.5 14.063l-6.135-1.582a.5.5 0 0 1 0-.962L8.5 9.936A2 2 0 0 0 9.937 8.5l1.582-6.135a.5.5 0 0 1 .963 0L14.063 8.5A2 2 0 0 0 15.5 9.937l6.135 1.581a.5.5 0 0 1 0 .964L15.5 14.063a2 2 0 0 0-1.437 1.437l-1.582 6.135a.5.5 0 0 1-.963 0z"/><path d="M20 3v4"/><path d="M22 5h-4"/><path d="M4 17v2"/><path d="M5 18H3"/>',
        "calendar-days": '<rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4"/><path d="M8 2v4"/><path d="M3 10h18"/><path d="M8 14h.01"/><path d="M12 14h.01"/><path d="M16 14h.01"/><path d="M8 18h.01"/><path d="M12 18h.01"/><path d="M16 18h.01"/>',
        "map-pin": '<path d="M20 10c0 4.993-5.539 10.193-7.399 11.799a1 1 0 0 1-1.202 0C9.539 20.193 4 14.993 4 10a8 8 0 0 1 16 0"/><circle cx="12" cy="10" r="3"/>',
        "lightbulb": '<path d="M15 14c.2-1 .7-1.7 1.5-2.5 1-.9 1.5-2.2 1.5-3.5A6 6 0 0 0 6 8c0 1 .2 2.2 1.5 3.5.7.7 1.3 1.5 1.5 2.5"/><path d="M9 18h6"/><path d="M10 22h4"/>',
        "lock-keyhole": '<circle cx="12" cy="16" r="1"/><rect x="3" y="10" width="18" height="12" rx="2"/><path d="M7 10V7a5 5 0 0 1 10 0v3"/>',
        "check": '<path d="M20 6 9 17l-5-5"/>',
        "menu": '<path d="M4 12h16"/><path d="M4 6h16"/><path d="M4 18h16"/>',
        "x": '<path d="M18 6 6 18"/><path d="m6 6 12 12"/>',
    }
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" '
        f'stroke="currentColor" stroke-width="2" stroke-linecap="round" '
        f'stroke-linejoin="round" class="icon {cls}" aria-hidden="true">{paths[name]}</svg>'
    )


# ---------------------------------------------------------------- DATA
NAV_LINKS = [
    ("About the Series", "#about"),
    ("Future Seminars", "#journey"),
    ("Upcoming Seminar", "#seminar"),
    ("Facilitator", "#facilitator"),
    ("Stay Updated", "#updates"),
]

BENEFITS = [
    ("brain", "Learn more effectively", "Replace ineffective habits with strategies that build durable learning."),
    ("target", "Improve academic performance", "Identify practical, often overlooked factors that influence grades."),
    ("book-open-check", "Differentiation skills", "Tell the difference between remembering information and understanding concepts."),
    ("sparkles", "Develop beyond school", "Connect academic success with purpose, responsibility, and personal growth."),
]

QUESTIONS = [
    "Which popular study habits waste time, even when they feel productive?",
    "How can I tell whether I actually know something?",
    "With the same number of study hours, how can I learn twice as much?",
    "What factors are easy but often overlooked for achieving good grades?",
    "What is the difference between information and concepts—and why does it matter?",
]

SEMINARS = [
    dict(number="01", label="Seminar 1 · Registration Closed",
         title="Grades, Learning, and Study Skills That Actually Work",
         text="Retrieval practice, spacing, test preparation, attendance, communicating with teachers, and the difference between memorizing information and understanding concepts.",
         active=True),
    dict(number="02", label="Seminar 2 · Coming Next",
         title="Memory Techniques: Remember More, For Longer",
         text="Visualization, association, chaining, storytelling, memory palaces, mnemonics, retrieval practice—with a section on French vocabulary",
         requirement="Requires Seminar 1"),
    dict(number="03–04", label="Seminars 3 & 4 · Future Sessions",
         title="Learning With Purpose",
         text="Mindset, purpose, critical and scientific thinking, recognizing misinformation, and using technology effectively.",
         requirement="Requires Seminar 2"),
]

DIFFERENCES = [
    ("Evidence-informed, not fad-driven", "Students learn strategies supported by research—not just whatever feels productive in the moment."),
    ("Honest about effort", "Effective learning often feels harder than rereading or cramming, but it leads to better retention and stronger results."),
    ("Focused on the whole student", "Grades matter, but so does learning, finding meaning, and nurturing curiosity and interests."),
]

REFERRAL_OPTIONS = ["Friend or family member", "School or teacher", "Community group", "Social media", "Other"]


# ---------------------------------------------------------------- HELPERS
def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def head(css_href):
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>From Grades to Growth | Ottawa Workshops for Grades 6–12</title>
<meta name="description" content="Hands-on, research-backed workshops in Ottawa for Grades 6–12 — practical study, memory, and mindset strategies that boost grades and durable learning. Register now.">
<link rel="canonical" href="{BASE}/">
<meta property="og:title" content="From Grades to Growth | Ottawa Workshops for Grades 6–12">
<meta property="og:description" content="Practical, research-informed workshops in Ottawa for Grade 6–12 students. Students practise retrieval, spacing, memory techniques, and mindset tools to improve grades and learning that lasts. Space is limited — register today.">
<meta property="og:type" content="website">
<meta property="og:url" content="{BASE}/">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/assets/img/favicon-32.png" sizes="32x32">
<link rel="apple-touch-icon" href="/assets/img/favicon-180.png">
<link rel="stylesheet" href="/assets/css/{css_href}">
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-2R8999RJ0R"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());

  gtag('config', 'G-2R8999RJ0R');
</script>
</head>
"""


def header_html():
    nav_items = "".join(f'<a href="{href}">{esc(label)}</a>' for label, href in NAV_LINKS)
    mobile_items = "".join(f'<a href="{href}" data-close-menu>{esc(label)}</a>' for label, href in NAV_LINKS)
    return f"""<header class="site-header">
  <div class="container">
    <a href="#top" aria-label="From Grades to Growth home" class="brand">
      <img src="/assets/img/logo.png" alt="" width="360" height="240" />
      <span>From Grades to Growth</span>
    </a>
    <nav aria-label="Main navigation" class="main-nav">{nav_items}</nav>
    <div class="header-actions">
      <a class="btn btn-primary" href="#updates">Register for Info</a>
      <button type="button" class="menu-toggle" id="menu-toggle" aria-expanded="false" aria-controls="mobile-nav" aria-label="Open menu">
        {icon("menu")}
      </button>
    </div>
  </div>
  <nav aria-label="Mobile navigation" class="mobile-nav" id="mobile-nav">{mobile_items}</nav>
</header>
"""


def section_heading(eyebrow, title, text=None, light=False, extra_class=""):
    dark = " on-dark" if light else ""
    out = f'<div class="section-heading {extra_class}">'
    if eyebrow:
        out += f'<p class="eyebrow{dark}">{esc(eyebrow)}</p>'
    out += f'<h2 class="heading{dark}">{title}</h2>'
    if text:
        out += f'<p class="lede{dark}">{esc(text)}</p>'
    out += "</div>"
    return out


def hero_html():
    return f"""<section class="hero">
  <img class="hero-photo" src="/assets/img/learning-path-hero.jpg" width="1028" height="1530"
       alt="A student walking along a sunlit learning path toward a growing tree" fetchpriority="high" />
  <div class="scrim"></div>
  <div class="container hero-inner">
    <div class="hero-copy">
      <p class="pill">{icon("users", "icon-xs")} For Grade 6–12 students</p>
      <h1>From Grades<br>to <span class="accent">Growth</span></h1>
      <p class="hero-sub">Practical workshops that help students<br>improve their grades, learn and think more deeply,<br>and develop habits for school and life.</p>
      <p class="hero-body">This series gives students practical,<br>research-informed strategies<br>they can use immediately.</p>
      <div class="hero-actions">
        <a class="btn btn-primary btn-lg" href="#updates">Register for Info {icon("arrow-right", "icon-xs")}</a>
      </div>
    </div>
  </div>
</section>
"""


def about_html():
    cards = "".join(
        f'<article class="card"><span class="icon-badge">{icon(ic, "icon-sm")}</span>'
        f'<h3>{esc(title)}</h3><p>{esc(text)}</p></article>'
        for ic, title, text in BENEFITS
    )
    return f"""<section id="about">
  <div class="container">
    <div class="grid grid-about">
      {section_heading("A better way to learn", "Better grades matter. So does learning that lasts.")}
      <div class="lede-block">
        <p>Students can spend hours studying and still walk into a test unsure of what they know. Often, the issue is not effort or intelligence—it is method.</p>
        <p>From Grades to Growth combines practical academic strategies with deeper questions about purpose, motivation, mindset, technology, and how to think clearly in a complicated world.</p>
        <p><strong>This is not a lecture about “being more organized.” Students actively practise strategies, ask questions, and leave with approaches they can use right away.</strong></p>
      </div>
    </div>
    <div class="benefit-grid">{cards}</div>
  </div>
</section>
"""


def seminar_html():
    return f"""<section id="seminar" class="bg-primary">
  <div class="container">
    <div class="seminar-grid">
      <div>
        {section_heading("Upcoming session · Seminar 1", "Study Skills That Actually Work", light=True)}
        <p class="seminar-kicker">Grades, Learning, and How to Learn More Deeply</p>
        <p class="hero-sub on-dark" style="margin-top:2rem;">Study less blindly. Learn more deeply.</p>
        <div class="seminar-callout">{icon("lightbulb", "icon-sm")}<p>Students will practise the methods in the room—not just hear about them.</p></div>
      </div>
      <aside class="seminar-card">
        <div class="seminar-row">{icon("calendar-days", "icon-sm")}<div><strong>Friday, September 25, 2026</strong><p class="muted">Pizza Dinner: 5:00–5:30 p.m.<br>Seminar: 5:30–8:00 p.m.</p></div></div>
        <div class="divider"></div>
        <div class="seminar-row">{icon("map-pin", "icon-sm")}<div><strong>McArthur Ave, Ottawa</strong></div></div>
        <div class="divider"></div>
        <div class="seminar-row"><span class="fee-badge">$</span><div><strong>Fee: $10</strong><p class="muted">Includes pizza, snacks, and materials.</p></div></div>
        <div class="bring-box"><strong>What to bring:</strong> A pen, notebook, and something firm to write on. Everything else is provided.</div>
        <a class="btn btn-primary btn-lg btn-block" style="margin-top:1.75rem;" href="#updates">Register for Info {icon("arrow-right", "icon-xs")}</a>
        <p class="seminar-fine">Space is limited. Registration includes pizza, snacks, and workshop materials.</p>
      </aside>
    </div>
  </div>
</section>
"""


def questions_html():
    cards = ""
    for i, q in enumerate(QUESTIONS):
        cls = "question-card full" if i == len(QUESTIONS) - 1 else "question-card"
        cards += f'<div class="{cls}"><span class="question-num">{i + 1}</span><p>{esc(q)}</p></div>'
    return f"""<section class="bg-sage">
  <div class="container">
    {section_heading("Practical clarity", "Students will leave able to answer:")}
    <div class="question-grid">{cards}</div>
    <p class="lede" style="max-width:56rem;">Students will not simply receive a list of tips. They will learn why certain strategies work, practise them during the workshop, and create a clearer approach to their own learning.</p>
  </div>
</section>
"""


def journey_html():
    cards = ""
    for s in SEMINARS:
        active = s.get("active")
        cls = "journey-card active" if active else "journey-card"
        top_right = (
            '<span class="journey-badge">Registration Closed</span>'
            if active
            else f'<span class="lock">{icon("lock-keyhole", "icon-sm")}</span>'
        )
        cta = (
            f'<a class="btn btn-primary" href="#updates">Register for Info {icon("arrow-right", "icon-xs")}</a>'
            if active
            else f'<button class="btn btn-disabled" disabled>{icon("lock-keyhole", "icon-xs")} {esc(s["requirement"])}</button>'
        )
        cards += (
            f'<article class="{cls}">'
            f'<div class="journey-top"><span class="journey-number">{s["number"]}</span>{top_right}</div>'
            f'<p class="journey-label">{esc(s["label"])}</p>'
            f'<h3>{esc(s["title"])}</h3>'
            f'<p class="body">{esc(s["text"])}</p>'
            f"{cta}"
            f"</article>"
        )
    return f"""<section id="journey">
  <div class="container">
    {section_heading("The workshop journey", "A learning journey, not just a one-time workshop", "The workshops are designed as a sequence. Each session builds on the ideas, language, and practical tools introduced in the previous one.")}
    <div class="journey-grid">{cards}</div>
    <div class="prereq-note">{icon("lock-keyhole", "icon-sm")}<p><strong>Why prerequisites?</strong> The series builds a shared foundation. Students who begin with Seminar 1 will be better prepared to get the most from later sessions.</p></div>
  </div>
</section>
"""


def difference_html():
    items = "".join(
        f'<div class="difference-item"><span class="difference-check">{icon("check", "icon-xs")}</span>'
        f'<div><h3>{esc(title)}</h3><p>{esc(text)}</p></div></div>'
        for title, text in DIFFERENCES
    )
    return f"""<section class="bg-sage">
  <div class="parallax-banner" style="background-image:url('/assets/img/workshop-session.jpg')" role="img" aria-label="Martin leading a seminar with a group of students seated in a circle"></div>
  <div class="container difference-content">
    {section_heading("What makes this different", "More than productivity tips")}
    <div class="difference-list">{items}</div>
  </div>
</section>
"""


def facilitator_html():
    return f"""<section id="facilitator">
  <div class="container-narrow">
    <div class="facilitator-grid">
      <div class="facilitator-portrait">
        <img src="/assets/img/facilitator.jpg" width="480" height="600" alt="Martin Braithwaite, Workshop Facilitator" loading="lazy" />
      </div>
      <div>
        {section_heading("Meet the facilitator", "Martin Braithwaite")}
        <p class="facilitator-role">Workshop Facilitator</p>
        <div class="facilitator-bio">
          <p>Martin is an experienced educator and mentor dedicated to helping young people thrive both academically and personally. Over the past decade, he has guided students across Canada, Mainland China, and Macau, teaching within both public and private systems across local and international (IB) curricula. He has taught IB Psychology, university-level business and computer science, and moral empowerment and character development programs.</p>
          <p>Having benefited from study skills workshops firsthand as a student, Martin is passionate about facilitating this series to help learners connect practical academic strategies with deeper questions of personal growth and purpose.</p>
        </div>
        <blockquote class="facilitator-quote">“This is a collaborative process where students are the protagonists of their own learning. They connect daily study habits with a deeper sense of purpose, not just for better results at school but to improve their ability to shape their future.”</blockquote>
      </div>
    </div>
  </div>
</section>
"""


def updates_html():
    referral_opts = "".join(f"<option>{esc(o)}</option>" for o in REFERRAL_OPTIONS)
    return f"""<section id="updates" class="bg-primary">
  <div class="container">
    <div class="updates-grid">
      <div class="updates-sticky">
        {section_heading("Stay connected", "Want to hear about future sessions?", "Seminars 2, 3, and 4 will be announced after Seminar 1. Complete the form to receive upcoming dates, registration details, and future opportunities.", light=True)}
      </div>
      <div class="form-card">
        <div id="updates-success" class="form-success" hidden>
          <span class="check">{icon("check", "icon-lg")}</span>
          <h3>Thank you!</h3>
          <p>We’ll keep you informed about upcoming From Grades to Growth seminars.</p>
        </div>
        <form id="updates-form" class="updates-form" name="parent-interest" method="POST" data-netlify="true" netlify-honeypot="company-website">
          <input type="hidden" name="form-name" value="parent-interest">
          <p class="hp"><label>Do not fill this in: <input name="company-website" tabindex="-1" autocomplete="off"></label></p>
          <label class="field">Parent / Guardian Name<input name="parentName" type="text" required maxlength="100"></label>
          <label class="field">Parent / Guardian Email Address<input name="email" type="email" required maxlength="255"></label>
          <label class="field">Children’s Names and Grades<textarea name="childrenGrades" required maxlength="1000" rows="3" placeholder="e.g., Maya — Grade 7; Daniel — Grade 10"></textarea></label>
          <label class="field">How did you hear about this workshop series?
            <select name="referralSource"><option value="">Select an option (optional)</option>{referral_opts}</select>
          </label>
          <label class="field">Comments or questions<textarea name="comments" maxlength="2000" rows="3"></textarea></label>
          <p id="updates-error" class="form-error" role="alert" hidden></p>
          <button type="submit" class="btn btn-primary btn-lg form-submit" id="updates-submit">Keep Me Updated</button>
          <p class="form-note">We will use this information only to share updates about this workshop series and related student learning opportunities. We will not sell or share your contact information.</p>
        </form>
      </div>
    </div>
  </div>
</section>
"""


def footer_html():
    return f"""<footer class="site-footer bg-navy-deep">
  <div class="container footer-grid">
    <div>
      <p class="brand-name">From Grades to Growth</p>
      <p class="tagline">Practical learning workshops for students in Grades 6–12.</p>
    </div>
    <div><p class="footer-hosted">Hosted in Ottawa, Canada</p></div>
    <div class="footer-col-right">
      <p class="footer-contact-label">Reach out:</p>
      <a class="footer-contact-link" href="mailto:mbraithwaite2026@gmail.com">mbraithwaite2026@gmail.com</a>
      <a class="footer-contact-link" href="tel:+13433224841">+1 (343) 322-4841</a>
    </div>
  </div>
  <div class="container footer-bottom">© 2026 From Grades to Growth. All rights reserved.</div>
</footer>
"""


def form_script():
    return f"""<script>
(function () {{
  var toggle = document.getElementById("menu-toggle");
  var nav = document.getElementById("mobile-nav");
  if (toggle && nav) {{
    toggle.addEventListener("click", function () {{
      var open = nav.classList.toggle("open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
      toggle.innerHTML = open
        ? {icon("x")!r}
        : {icon("menu")!r};
    }});
    nav.querySelectorAll("[data-close-menu]").forEach(function (a) {{
      a.addEventListener("click", function () {{
        nav.classList.remove("open");
        toggle.setAttribute("aria-expanded", "false");
        toggle.innerHTML = {icon("menu")!r};
      }});
    }});
  }}

  var form = document.getElementById("updates-form");
  var success = document.getElementById("updates-success");
  var errorEl = document.getElementById("updates-error");
  var submitBtn = document.getElementById("updates-submit");
  if (!form) return;

  function encodeForm(data) {{
    return Object.keys(data)
      .map(function (k) {{ return encodeURIComponent(k) + "=" + encodeURIComponent(data[k] == null ? "" : data[k]); }})
      .join("&");
  }}

  form.addEventListener("submit", function (event) {{
    event.preventDefault();
    errorEl.hidden = true;

    var data = new FormData(form);

    // Honeypot: real visitors never fill this in. If it's filled, quietly
    // pretend success without writing anywhere, instead of tipping off the bot.
    if (String(data.get("company-website") || "").trim()) {{
      form.hidden = true;
      success.hidden = false;
      return;
    }}

    submitBtn.disabled = true;
    submitBtn.textContent = "Sending\\u2026";

    var parentName = String(data.get("parentName") || "").trim();
    var email = String(data.get("email") || "").trim();
    var childrenGrades = String(data.get("childrenGrades") || "").trim();
    var referralSource = String(data.get("referralSource") || "").trim();
    var comments = String(data.get("comments") || "").trim();

    // Netlify Forms is the only backend: this AJAX POST is what saves the
    // submission (visible in the Netlify dashboard, with optional email
    // notifications) — it's what preventDefault above stopped a normal
    // browser form submission from doing automatically.
    fetch("/", {{
      method: "POST",
      headers: {{ "Content-Type": "application/x-www-form-urlencoded" }},
      body: encodeForm({{
        "form-name": "parent-interest",
        "company-website": "",
        parentName: parentName,
        email: email,
        childrenGrades: childrenGrades,
        referralSource: referralSource,
        comments: comments,
      }}),
    }})
      .then(function (res) {{
        if (!res.ok) throw new Error("We couldn\\u2019t save your details. Please try again.");
        form.hidden = true;
        success.hidden = false;
      }})
      .catch(function (err) {{
        errorEl.textContent = err.message || "Please try again.";
        errorEl.hidden = false;
      }})
      .finally(function () {{
        submitBtn.disabled = false;
        submitBtn.textContent = "Keep Me Updated";
      }});
  }});
}})();
</script>
"""


def page(css_href):
    body = (
        header_html()
        + hero_html()
        + about_html()
        + questions_html()
        + journey_html()
        + seminar_html()
        + difference_html()
        + facilitator_html()
        + updates_html()
        + footer_html()
        + form_script()
    )
    return head(css_href) + f'<body>\n<main id="top">\n{body}\n</main>\n</body>\n</html>\n'


# ---------------------------------------------------------------- WRITE
def write(path, content):
    full = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)


def main():
    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)

    hashed_css = css_name()
    shutil.copytree("assets", os.path.join(OUT, "assets"))
    os.rename(os.path.join(OUT, "assets", "css", "site.css"), os.path.join(OUT, "assets", "css", hashed_css))

    write("index.html", page(hashed_css))

    write(
        "robots.txt",
        f"User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n",
    )
    write(
        "sitemap.xml",
        f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>{BASE}/</loc><lastmod>{BUILT}</lastmod></url>
</urlset>
""",
    )
    write(
        "_headers",
        """/*
  X-Frame-Options: SAMEORIGIN
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: geolocation=(), microphone=(), camera=()

/assets/*
  Cache-Control: public, max-age=31536000, immutable
""",
    )
    write(
        "_redirects",
        "# Tidy up stray .html requests\n/index.html   /   301\n",
    )
    write(
        "404.html",
        head(hashed_css).replace("</head>", "") + """</head>
<body>
<main style="display:flex;min-height:70vh;align-items:center;justify-content:center;text-align:center;padding:2rem;">
  <div>
    <h1 style="font-size:2rem;color:var(--primary);">Page not found</h1>
    <p style="margin-top:1rem;"><a href="/" style="color:var(--leaf);font-weight:700;">Back to From Grades to Growth</a></p>
  </div>
</main>
</body>
</html>
""",
    )

    print(f"Built {OUT}/ ({hashed_css})")


if __name__ == "__main__":
    main()
