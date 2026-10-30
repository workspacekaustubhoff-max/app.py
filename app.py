import streamlit as st
import streamlit.components.v1 as components
import urllib.parse
import urllib.request
import json
import re
import io
import uuid
import html
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from difflib import SequenceMatcher
from datetime import date, timedelta

st.set_page_config(page_title="PageNest | Books & Learning", page_icon="📚", layout="wide")

# ----------------------- STYLE -----------------------
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Playfair+Display:wght@500;600;700&display=swap');
:root{--bg:#FBF8F3;--ink:#1B2A22;--muted:#6B6F68;--line:#E7DFD0;--forest:#1F3A2E;--forest-d:#152A20;--gold:#B8955A;--cream:#F3ECDF}
html{scroll-behavior:smooth}
html,body,.stApp,[data-testid="stAppViewContainer"],[data-testid="stMain"],[data-testid="stHeader"]{
 background:var(--bg)!important;color:var(--ink)!important;font-family:'Inter',sans-serif}
.block-container{max-width:1280px;padding-top:1rem;padding-bottom:3rem}
h1,h2,h3,h4{font-family:'Playfair Display',serif!important;color:var(--ink)!important;letter-spacing:-.01em}
p,label,li,[data-testid="stMarkdownContainer"],[data-testid="stWidgetLabel"],[data-testid="stCaptionContainer"]{color:var(--ink)!important}
[data-testid="stCaptionContainer"]{color:var(--muted)!important}
footer{visibility:hidden}

/* sidebar */
[data-testid="stSidebar"]{background:#fff!important;border-right:1px solid var(--line)}
[data-testid="stSidebar"] *{color:var(--ink)!important}
[data-testid="stSidebar"] [data-testid="stMetric"]{border:none;padding:6px 0;background:transparent!important}

/* inputs */
.stTextInput input,.stTextArea textarea,.stNumberInput input{
 background:#fff!important;color:var(--ink)!important;-webkit-text-fill-color:var(--ink)!important;
 border:1px solid #D8D0BF!important;border-radius:8px!important;caret-color:var(--forest)!important}
.stTextInput input:focus,.stTextArea textarea:focus{border-color:var(--forest)!important;box-shadow:0 0 0 2px rgba(31,58,46,.18)!important}
.stTextInput input::placeholder,.stTextArea textarea::placeholder{color:#8A8F88!important;-webkit-text-fill-color:#8A8F88!important;opacity:1!important}
[data-baseweb="select"]>div{background:#fff!important;color:var(--ink)!important;border-color:#D8D0BF!important;border-radius:8px!important}
[data-baseweb="select"] input{color:var(--ink)!important;-webkit-text-fill-color:var(--ink)!important}
[data-baseweb="popover"],[data-baseweb="menu"],[role="listbox"],[role="option"]{background:#fff!important;color:var(--ink)!important}

/* buttons */
.stButton>button,.stFormSubmitButton>button,.stDownloadButton>button{
 background:var(--forest)!important;color:#fff!important;border:1px solid var(--forest)!important;
 border-radius:6px!important;font-weight:600!important;min-height:2.5rem;letter-spacing:.02em}
.stButton>button *,.stFormSubmitButton>button *,.stDownloadButton>button *{color:#fff!important}
.stButton>button:hover,.stFormSubmitButton>button:hover,.stDownloadButton>button:hover{background:var(--forest-d)!important;border-color:var(--forest-d)!important}
.stButton>button:focus-visible{outline:3px solid var(--gold)!important;outline-offset:2px}

/* cards, forms, metrics */
[data-testid="stVerticalBlockBorderWrapper"]{background:#fff!important;border:1px solid var(--line)!important;border-radius:14px!important;
 box-shadow:0 6px 20px rgba(27,42,34,.05)}
[data-testid="stForm"]{background:#fff!important;border:1px solid var(--line)!important;border-radius:14px!important;padding:22px!important}
[data-testid="stForm"] label,[data-testid="stForm"] [data-testid="stWidgetLabel"],
[data-testid="stForm"] [data-testid="stMarkdownContainer"]{color:var(--ink)!important}
[data-testid="stMetric"]{background:#fff!important;padding:14px;border:1px solid var(--line);border-radius:12px}
[data-testid="stMetricLabel"],[data-testid="stMetricValue"]{color:var(--ink)!important}
[data-testid="stChatMessage"]{background:var(--bg)!important;border:1px solid var(--line);border-radius:12px}
[data-testid="stImage"] img{width:100%;aspect-ratio:2/3;object-fit:cover;border-radius:3px 8px 8px 3px;
 box-shadow:-3px 0 0 rgba(0,0,0,.12),0 8px 18px rgba(27,42,34,.2)}
hr{border-color:var(--line)!important}

/* announcement bar */
.announce{display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap;background:var(--forest);border-radius:10px;
 padding:9px 20px;margin-bottom:10px}
.announce span{color:#fff!important;font-size:12.5px;letter-spacing:.02em}

/* top navigation (real buttons, styled as text links) */
[data-testid="stHorizontalBlock"]:has(.topnav-marker){align-items:center;background:#fff;border:1px solid var(--line);
 border-radius:12px;padding:6px 14px;margin-bottom:14px}
[data-testid="stHorizontalBlock"]:has(.topnav-marker) .stButton>button{
 background:transparent!important;border:none!important;box-shadow:none!important;color:var(--ink)!important;
 font-size:12px!important;letter-spacing:.1em;text-transform:uppercase;font-weight:600!important;min-height:2.2rem;border-radius:0!important}
[data-testid="stHorizontalBlock"]:has(.topnav-marker) .stButton>button *{color:var(--ink)!important}
[data-testid="stHorizontalBlock"]:has(.topnav-marker) .stButton>button:hover{background:transparent!important;
 border-bottom:2px solid var(--gold)!important}
.brand{font-family:'Playfair Display',serif;font-size:22px;font-weight:700;letter-spacing:.14em;color:var(--ink)!important;line-height:1.1}
.brand small{display:block;font-family:'Inter',sans-serif;font-size:9.5px;letter-spacing:.32em;font-weight:500;color:var(--muted)!important}

/* hero */
.hero{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);align-items:stretch;
 background:linear-gradient(100deg,#FBF8F3 0%,#F4EBDA 48%,#E3CDA6 100%);border-radius:20px;overflow:hidden;margin:4px 0 22px;min-height:400px}
.hero-copy{padding:46px 40px;display:flex;flex-direction:column;justify-content:center}
.eyebrow{color:var(--gold)!important;font-size:11.5px;font-weight:600;letter-spacing:.18em;text-transform:uppercase}
.hero h1{font-size:clamp(34px,4.6vw,56px);line-height:1.07;margin:12px 0 16px}
.hero p{color:#3C4A41!important;font-size:16px;max-width:40ch;margin:0 0 24px;line-height:1.6}
.hero-cta{display:flex;gap:12px;flex-wrap:wrap;margin-bottom:26px}
.btn-solid,.btn-line{display:inline-block;padding:13px 26px;border-radius:6px;font-weight:600;font-size:12.5px;letter-spacing:.1em;
 text-transform:uppercase;text-decoration:none!important}
.btn-solid{background:var(--forest);color:#fff!important}
.btn-line{border:1px solid var(--ink);color:var(--ink)!important;background:rgba(255,255,255,.4)}
.hero-facts{display:flex;gap:26px;flex-wrap:wrap}
.hero-facts span{color:var(--ink)!important;font-size:13px}
.hero-facts b{color:var(--forest)!important;font-family:'Playfair Display',serif;font-size:22px;margin-right:6px}
.hero-art{position:relative;display:flex;flex-direction:column;align-items:center;justify-content:flex-end;padding:30px 20px 26px;
 background:radial-gradient(circle at 60% 40%,rgba(255,255,255,.55),rgba(255,255,255,0) 60%)}
.stand{width:150px;height:216px;background:linear-gradient(160deg,#18294F,#0A1530);border-radius:3px 7px 7px 3px;
 box-shadow:-7px 0 0 rgba(0,0,0,.28),0 16px 30px rgba(0,0,0,.35);display:flex;flex-direction:column;align-items:center;
 justify-content:center;text-align:center;padding:14px;transform:rotate(-2deg);margin-bottom:-2px;position:relative;z-index:2}
.stand .star{color:#F2D9A0!important;font-size:14px;margin-bottom:10px}
.stand .t{font-family:'Playfair Display',serif;color:#F2D9A0!important;font-size:23px;line-height:1.1}
.stand .a{color:#F2D9A0!important;font-size:10px;letter-spacing:.22em;margin-top:16px}
.stack{display:flex;flex-direction:column;align-items:center;gap:3px;position:relative;z-index:1}
.bk{height:44px;display:flex;align-items:center;justify-content:space-between;gap:12px;padding:0 18px;border-radius:2px;
 font-family:'Playfair Display',serif;font-size:15px;box-shadow:0 4px 10px rgba(0,0,0,.22)}
.bk i{font-family:'Inter',sans-serif;font-size:10.5px;font-style:normal;opacity:.85}
.new-badge{position:absolute;right:7%;top:40%;width:104px;height:104px;border-radius:50%;background:var(--forest);
 display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;
 box-shadow:0 8px 20px rgba(0,0,0,.25);z-index:3;border:3px solid rgba(255,255,255,.7)}
.new-badge b{font-family:'Playfair Display',serif;color:#fff!important;font-size:17px;line-height:1.1}
.new-badge small{color:#fff!important;font-size:10.5px;margin-top:4px}
@media(max-width:800px){.hero{grid-template-columns:1fr}.new-badge{right:3%;top:30%;width:84px;height:84px}.hero-copy{padding:30px 22px}}

/* feature strip */
.features{display:grid;grid-template-columns:repeat(4,1fr);background:#fff;border:1px solid var(--line);border-radius:14px;
 padding:16px 6px;margin:0 0 6px;box-shadow:0 10px 26px rgba(27,42,34,.07)}
.feat{display:flex;gap:12px;align-items:center;padding:4px 18px;border-right:1px solid var(--line)}
.feat:last-child{border-right:none}
.feat .ico{font-size:24px}
.feat b{display:block;font-size:11.5px;letter-spacing:.08em;text-transform:uppercase;color:var(--ink)!important}
.feat span{font-size:12.5px;color:var(--muted)!important}
@media(max-width:800px){.features{grid-template-columns:1fr 1fr;row-gap:12px}.feat{border-right:none}}

/* section titles */
.sec{display:flex;justify-content:space-between;align-items:flex-end;gap:12px;margin:30px 0 14px}
.sec h2{margin:2px 0 0;font-size:30px}
.sec small{color:var(--muted)!important;font-size:13.5px}

/* category tiles */
.cat-tile{height:150px;border-radius:12px;padding:14px 10px;display:flex;flex-direction:column;align-items:center;
 justify-content:flex-start;text-align:center;box-shadow:0 8px 18px rgba(27,42,34,.18)}
.cat-ico{width:46px;height:46px;border-radius:50%;background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.4);
 display:flex;align-items:center;justify-content:center;font-size:21px;margin:4px 0 auto}
.cat-name{font-family:'Playfair Display',serif;font-size:13px;letter-spacing:.07em;font-weight:700;text-transform:uppercase;color:#fff!important;line-height:1.2}
.cat-sub{font-size:11px;color:rgba(255,255,255,.8)!important;margin-top:3px}

/* designed fallback cover (used only when no real cover image is found) */
.gen-cover{aspect-ratio:2/3;width:100%;box-sizing:border-box;border-radius:3px 8px 8px 3px;display:flex;flex-direction:column;
 align-items:center;justify-content:center;text-align:center;padding:18px 14px;
 box-shadow:-3px 0 0 rgba(0,0,0,.18),0 8px 18px rgba(27,42,34,.2)}
.gc-title{font-family:'Playfair Display',serif;color:#F2D9A0!important;font-weight:700;line-height:1.15;margin:14px 0}
.gc-rule{width:46px;height:2px;background:#B8955A}
.gc-author{color:#EBDDBB!important;font-size:11px;letter-spacing:.18em;font-weight:600}

/* book card text */
.meta-top{display:flex;justify-content:space-between;align-items:center;gap:6px;margin:6px 0 4px}
.pill{display:inline-block;background:var(--cream);color:var(--forest)!important;border-radius:6px;padding:3px 8px;font-size:11.5px;font-weight:600}
.badge{font-size:11.5px;font-weight:600;border-radius:6px;padding:3px 8px;display:inline-block}
.badge.ok{background:#E3EDE5;color:#1F3A2E!important}
.badge.low{background:#F8E8C8;color:#7A4B00!important}
.badge.out{background:#F4DAD2;color:#8A2D17!important}
.book-title{color:var(--ink)!important;font-family:'Playfair Display',serif;font-size:17px;font-weight:600;line-height:1.25;min-height:44px}
.book-author{color:var(--muted)!important;font-size:13px;min-height:34px}
.book-price{color:var(--forest)!important;font-size:21px;font-weight:700;margin:4px 0 6px}

/* order summary rows */
.sumrow{display:flex;justify-content:space-between;gap:12px;padding:6px 0;border-bottom:1px solid var(--line);font-size:14px}
.sumrow.total{border-bottom:none;border-top:2px solid var(--ink);margin-top:6px;padding-top:10px;font-size:17px;font-weight:700}

/* newsletter banner (a real form, styled) */
[data-testid="stForm"]:has(.nl-marker){background:linear-gradient(100deg,#1F3A2E 0%,#2B4A3B 60%,#5C5A3E 100%)!important;border:none!important;
 border-radius:16px!important;padding:30px 34px!important;margin-top:30px}
[data-testid="stForm"]:has(.nl-marker) [data-testid="stMarkdownContainer"] *{color:#fff!important}
[data-testid="stForm"]:has(.nl-marker) .nl-eyebrow{color:#E0C48C!important}
[data-testid="stForm"]:has(.nl-marker) .stFormSubmitButton>button{background:var(--gold)!important;border-color:var(--gold)!important;color:#1B2A22!important}
[data-testid="stForm"]:has(.nl-marker) .stFormSubmitButton>button *{color:#1B2A22!important}

/* trust strip + footer */
.trust{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin:30px 0 0;padding:22px 0;border-top:1px solid var(--line)}
.trust div{text-align:center;font-size:13.5px;font-weight:600;color:var(--ink)!important}
.trust small{display:block;font-weight:400;color:var(--muted)!important;font-size:12px;margin-top:2px}
@media(max-width:800px){.trust{grid-template-columns:1fr 1fr}}
.footer{margin-top:14px;padding:34px;border-radius:16px;background:var(--forest);color:#fff!important}
.footer *{color:#fff!important}
.foot-grid{display:grid;grid-template-columns:1.5fr 1fr 1fr 1fr;gap:28px}
.foot-grid h5{font-family:'Inter',sans-serif;font-size:11.5px;letter-spacing:.16em;text-transform:uppercase;margin:0 0 10px;color:#E0C48C!important}
.foot-grid div div{font-size:13px;opacity:.85;margin:4px 0}
.foot-brand{font-family:'Playfair Display',serif;font-size:22px;font-weight:700;letter-spacing:.14em}
.foot-bottom{margin-top:24px;padding-top:14px;border-top:1px solid rgba(255,255,255,.18);text-align:center;font-size:12px;opacity:.8}
@media(max-width:800px){.foot-grid{grid-template-columns:1fr 1fr}}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# Category tiles shown on the home page: (subject, icon, tagline, background)
CATEGORY_TILES = [
    ("Fiction & Classics", "📖", "Explore Stories", "linear-gradient(145deg,#3B2F2A,#14100E)"),
    ("Self-help & Ideas", "🌿", "Better Yourself", "linear-gradient(145deg,#2E4A3C,#101E17)"),
    ("Business & Management", "💼", "Build Your Future", "linear-gradient(145deg,#2C3A55,#0F1626)"),
    ("Thrillers & Mystery", "🔍", "Pulse-Racing Reads", "linear-gradient(145deg,#4A2A33,#170C10)"),
    ("Fantasy & Young Adult", "🐉", "Worlds Beyond", "linear-gradient(145deg,#4A3A22,#1A1309)"),
    ("Economics", "🏛️", "Timeless Thinking", "linear-gradient(145deg,#38403A,#121614)"),
]


def flat(s):
    """Collapse multi-line HTML into one line. Markdown treats blank lines followed by
    indented text as a code block, which is what made raw <div> text appear on screen."""
    return "".join(line.strip() for line in s.splitlines())


def announce_html():
    return ('<div class="announce"><span>🚚 Free standard delivery on every order</span>'
            '<span>✦ Books that inspire, stories that stay.</span>'
            '<span>💬 PageNest Help is in the sidebar</span></div>')


def hero_html(book_count, subject_count, cart_total, show_cta):
    cta = ""
    if show_cta:
        cta = ('<div class="hero-cta"><a class="btn-solid" href="#browse-all">Shop now &rarr;</a>'
               '<a class="btn-line" href="#categories">Explore collection</a></div>')
    return flat(f"""
<div class="hero">
  <div class="hero-copy">
    <div class="eyebrow">Discover. Read. Grow.</div>
    <h1>Books for every<br>mind &amp; moment.</h1>
    <p>Textbooks, exam guides, business classics and bestsellers. Your next favourite story is just a page away.</p>
    {cta}
    <div class="hero-facts">
      <span><b>{book_count}</b>books</span>
      <span><b>{subject_count}</b>subjects</span>
      <span><b>{cart_total}</b>in your cart</span>
    </div>
  </div>
  <div class="hero-art">
    <div class="stand"><div class="star">★</div><div class="t">The Midnight Library</div><div class="a">MATT HAIG</div></div>
    <div class="stack">
      <div class="bk" style="width:270px;background:#EFE3CC;color:#1B2A22"><span>Atomic Habits</span><i>James Clear</i></div>
      <div class="bk" style="width:290px;background:#1B2A22;color:#EBDDBB"><span>The Alchemist</span><i>Paulo Coelho</i></div>
      <div class="bk" style="width:262px;background:#E4CFA4;color:#1B2A22"><span>Ikigai</span><i>García &amp; Miralles</i></div>
      <div class="bk" style="width:280px;background:#14213D;color:#F2D9A0"><span>The Psychology of Money</span><i>Morgan Housel</i></div>
    </div>
    <div class="new-badge"><b>New<br>Arrivals</b><small>This Week!</small></div>
  </div>
</div>""")


def features_html():
    items = [
        ("🚚", "Free Delivery", "Standard shipping is free"),
        ("🎁", "Bundle Savings", "10% off every bundle"),
        ("🛡️", "Demo Checkout", "No real payments taken"),
        ("🏷️", "Exclusive Offers", "Use code PAGENEST10"),
    ]
    cells = "".join(f'<div class="feat"><div class="ico">{i}</div><div><b>{html.escape(t)}</b><span>{html.escape(s)}</span></div></div>'
                    for i, t, s in items)
    return f'<div class="features">{cells}</div>'


def section_title(title, note="", eyebrow="", anchor=""):
    small = f"<small>{html.escape(note)}</small>" if note else ""
    eb = f'<div class="eyebrow">{html.escape(eyebrow)}</div>' if eyebrow else ""
    aid = f' id="{html.escape(anchor)}"' if anchor else ""
    return f'<div class="sec"{aid}><div>{eb}<h2>{html.escape(title)}</h2></div>{small}</div>'


def trust_html():
    items = [("Handpicked Books", "Chosen for students and readers"), ("Easy Browsing", "Search, filter and sort"),
             ("Student Bundles", "Starter packs for every course"), ("Stories That Stay", "Books worth finishing")]
    cells = "".join(f'<div>{html.escape(t)}<small>{html.escape(s)}</small></div>' for t, s in items)
    return f'<div class="trust">{cells}</div>'


def footer_html():
    return flat("""<div class="footer">
  <div class="foot-grid">
    <div><div class="foot-brand">PAGENEST</div><div style="font-size:13px;opacity:.85;margin-top:8px">We believe books have the power to change lives.<br>Find your next idea. Discover your next chapter.</div></div>
    <div><h5>Shop</h5><div><div>Catalogue</div><div>Book Bundles</div><div>Bestsellers</div><div>Shopping Cart</div></div></div>
    <div><h5>Help</h5><div><div>Delivery options</div><div>Discount code PAGENEST10</div><div>Find a Book</div><div>PageNest Help (sidebar)</div></div></div>
    <div><h5>About</h5><div><div>About PageNest</div><div>Demo bookstore</div><div>Sample prices and inventory</div></div></div>
  </div>
  <div class="foot-bottom">PageNest | Books &amp; Learning · Demo bookstore · No real payments processed</div>
</div>""")


def stock_badge(stock):
    if stock == 0:
        return '<span class="badge out">Out of stock</span>'
    if stock <= 3:
        return f'<span class="badge low">Only {stock} left</span>'
    return '<span class="badge ok">In stock</span>'


def card_meta_html(book):
    return (
        f'<div class="meta-top"><span class="pill">{html.escape(book["category"])}</span>{stock_badge(book["stock"])}</div>'
        f'<div class="book-title">{html.escape(book["title"])}</div>'
        f'<div class="book-author">by {html.escape(book["author"])}</div>'
        f'<div class="book-price">₹{book["price"]:,}</div>'
    )

# ----------------------- CATALOGUE -----------------------
RAW_BOOKS = [
("Principles of Economics","N. Gregory Mankiw","Economics",899,8),
("Principles of Microeconomics","N. Gregory Mankiw","Economics",799,7),
("Principles of Macroeconomics","N. Gregory Mankiw","Economics",799,6),
("Microeconomics","Robert Pindyck and Daniel Rubinfeld","Economics",1199,5),
("Intermediate Microeconomics","Hal R. Varian","Economics",999,4),
("Macroeconomics","N. Gregory Mankiw","Economics",1099,6),
("Economics","Paul A. Samuelson and William D. Nordhaus","Economics",1299,3),
("Development Economics","Debraj Ray","Economics",999,4),
("International Economics","Dominick Salvatore","Economics",899,5),
("The Wealth of Nations","Adam Smith","Economics",499,9),
("Principles of Management","Harold Koontz and Heinz Weihrich","Business & Management",799,7),
("Management","Stephen P. Robbins and Mary Coulter","Business & Management",999,5),
("Organizational Behavior","Stephen P. Robbins and Timothy Judge","Business & Management",1099,5),
("Marketing Management","Philip Kotler and Kevin Lane Keller","Business & Management",1299,4),
("Human Resource Management","Gary Dessler","Business & Management",999,4),
("Operations Management","Jay Heizer and Barry Render","Business & Management",1099,5),
("Competitive Strategy","Michael E. Porter","Business & Management",899,4),
("The Lean Startup","Eric Ries","Business & Management",499,8),
("Good to Great","Jim Collins","Business & Management",499,6),
("The Personal MBA","Josh Kaufman","Business & Management",599,5),
("Business Model Generation","Alexander Osterwalder and Yves Pigneur","Business & Management",899,3),
("Financial Accounting","Jerry J. Weygandt, Paul D. Kimmel and Donald E. Kieso","Accounting & Finance",999,5),
("Accounting Principles","Jerry J. Weygandt, Paul D. Kimmel and Donald E. Kieso","Accounting & Finance",899,4),
("Fundamentals of Corporate Finance","Stephen A. Ross and others","Accounting & Finance",1199,4),
("Corporate Finance","Jonathan Berk and Peter DeMarzo","Accounting & Finance",1299,3),
("Financial Management","I. M. Pandey","Accounting & Finance",899,6),
("The Intelligent Investor","Benjamin Graham","Accounting & Finance",599,7),
("A Random Walk Down Wall Street","Burton G. Malkiel","Accounting & Finance",599,5),
("Business Mathematics","J. K. Sharma","Mathematics & Statistics",599,7),
("Business Statistics","J. K. Sharma","Mathematics & Statistics",699,6),
("Statistics for Business and Economics","Paul Newbold and others","Mathematics & Statistics",999,4),
("Fundamentals of Mathematical Statistics","S. C. Gupta and V. K. Kapoor","Mathematics & Statistics",899,5),
("Introduction to Probability","Joseph K. Blitzstein and Jessica Hwang","Mathematics & Statistics",999,4),
("Calculus","James Stewart","Mathematics & Statistics",1099,5),
("Linear Algebra and Its Applications","David C. Lay","Mathematics & Statistics",999,4),
("A Brief History of Time","Stephen Hawking","Science & Technology",399,7),
("Cosmos","Carl Sagan","Science & Technology",499,5),
("The Selfish Gene","Richard Dawkins","Science & Technology",599,4),
("The Origin of Species","Charles Darwin","Science & Technology",499,6),
("Concepts of Physics Volume 1","H. C. Verma","Science & Technology",499,8),
("Concepts of Physics Volume 2","H. C. Verma","Science & Technology",499,7),
("Fundamentals of Physics","David Halliday and others","Science & Technology",1199,4),
("Campbell Biology","Lisa A. Urry and others","Science & Technology",1499,3),
("How to Prepare for Quantitative Aptitude for CAT","Arun Sharma","CAT & MBA Entrance",699,8),
("How to Prepare for Data Interpretation for CAT","Arun Sharma","CAT & MBA Entrance",599,7),
("How to Prepare for Verbal Ability and Reading Comprehension for CAT","Arun Sharma","CAT & MBA Entrance",699,8),
("Quantitative Aptitude for CAT","Nishit K. Sinha","CAT & MBA Entrance",699,6),
("Verbal Ability and Reading Comprehension for CAT","Nishit K. Sinha","CAT & MBA Entrance",599,5),
("Word Power Made Easy","Norman Lewis","CAT & MBA Entrance",199,10),
("A Modern Approach to Verbal and Non-Verbal Reasoning","R. S. Aggarwal","CAT & MBA Entrance",499,8),
("Problems in General Physics","I. E. Irodov","JEE Preparation",499,5),
("Physical Chemistry","O. P. Tandon","JEE Preparation",699,6),
("Organic Chemistry","Morrison and Boyd","JEE Preparation",999,3),
("Concise Inorganic Chemistry","J. D. Lee","JEE Preparation",799,4),
("IIT Mathematics","M. L. Khanna","JEE Preparation",799,5),
("Objective Biology","Dinesh","NEET Preparation",699,6),
("Trueman's Elementary Biology","M. P. Tyagi","NEET Preparation",799,5),
("Objective Physics for NEET","D. C. Pandey","NEET Preparation",699,6),
("Objective Chemistry for NEET","D. C. Pandey","NEET Preparation",699,6),
("Indian Polity","M. Laxmikanth","UPSC & Civil Services",799,8),
("Certificate Physical and Human Geography","Goh Cheng Leong","UPSC & Civil Services",499,7),
("A Brief History of Modern India","Rajiv Ahir","UPSC & Civil Services",499,8),
("India's Struggle for Independence","Bipan Chandra","UPSC & Civil Services",599,6),
("Indian Economy","Ramesh Singh","UPSC & Civil Services",899,5),
("Environment","Shankar IAS Academy","UPSC & Civil Services",699,6),
("Introduction to the Constitution of India","D. D. Basu","UPSC & Civil Services",699,4),
("Business Law","Robert W. Emerson","Law & Communication",899,4),
("Business Law Including Company Law","P. C. Tulsian","Law & Communication",799,5),
("Business Communication Today","Courtland L. Bovee and John V. Thill","Law & Communication",999,3),
("The Elements of Style","William Strunk Jr. and E. B. White","Law & Communication",299,7),
("On Writing Well","William Zinsser","Law & Communication",399,5),
("Python Crash Course","Eric Matthes","Programming & Research",799,6),
("Automate the Boring Stuff with Python","Al Sweigart","Programming & Research",699,5),
("Learning Python","Mark Lutz","Programming & Research",1199,3),
("Think Python","Allen B. Downey","Programming & Research",599,5),
("Research Design","John W. Creswell and J. David Creswell","Programming & Research",999,4),
("The Craft of Research","Wayne C. Booth and others","Programming & Research",699,5),
("Research Methodology","C. R. Kothari","Programming & Research",599,7),
# Popular bestsellers and widely read classics
("Rich Dad Poor Dad","Robert T. Kiyosaki","Personal Development & Fiction",399,10),
("Ikigai","Héctor García and Francesc Miralles","Personal Development & Fiction",299,10),
("Atomic Habits","James Clear","Personal Development & Fiction",499,10),
("The Psychology of Money","Morgan Housel","Personal Development & Fiction",399,10),
("The Alchemist","Paulo Coelho","Personal Development & Fiction",299,9),
("The 7 Habits of Highly Effective People","Stephen R. Covey","Personal Development & Fiction",499,7),
("How to Win Friends and Influence People","Dale Carnegie","Personal Development & Fiction",299,9),
("Think and Grow Rich","Napoleon Hill","Personal Development & Fiction",249,8),
("The Subtle Art of Not Giving a F*ck","Mark Manson","Personal Development & Fiction",399,8),
("Deep Work","Cal Newport","Personal Development & Fiction",399,7),
("The 48 Laws of Power","Robert Greene","Personal Development & Fiction",599,6),
("The Power of Your Subconscious Mind","Joseph Murphy","Personal Development & Fiction",199,8),
("The Four Agreements","Don Miguel Ruiz","Personal Development & Fiction",299,6),
("Man's Search for Meaning","Viktor E. Frankl","Personal Development & Fiction",299,7),
("Sapiens: A Brief History of Humankind","Yuval Noah Harari","Personal Development & Fiction",599,7),
("Homo Deus","Yuval Noah Harari","Personal Development & Fiction",599,5),
("The Kite Runner","Khaled Hosseini","Personal Development & Fiction",399,6),
("A Thousand Splendid Suns","Khaled Hosseini","Personal Development & Fiction",399,6),
("1984","George Orwell","Personal Development & Fiction",249,8),
("Animal Farm","George Orwell","Personal Development & Fiction",199,8),
("The Great Gatsby","F. Scott Fitzgerald","Personal Development & Fiction",199,7),
("To Kill a Mockingbird","Harper Lee","Personal Development & Fiction",299,6),
("The Book Thief","Markus Zusak","Personal Development & Fiction",399,5),
("The Silent Patient","Alex Michaelides","Personal Development & Fiction",399,6),
("The Midnight Library","Matt Haig","Personal Development & Fiction",399,6),
("The 5 AM Club","Robin Sharma","Personal Development & Fiction",399,7),
("Can't Hurt Me","David Goggins","Personal Development & Fiction",499,5),
("Start With Why","Simon Sinek","Business & Management",399,6),
("Zero to One","Peter Thiel and Blake Masters","Business & Management",399,7),
("The 4-Hour Workweek","Timothy Ferriss","Business & Management",499,5),
("The Millionaire Next Door","Thomas J. Stanley and William D. Danko","Accounting & Finance",399,5),
("Principles: Life and Work","Ray Dalio","Business & Management",699,4),
("The Hard Thing About Hard Things","Ben Horowitz","Business & Management",499,5),
("Shoe Dog","Phil Knight","Business & Management",499,5),
("The Design of Everyday Things","Don Norman","Science & Technology",499,4),
# Ten additional famous books
("The Monk Who Sold His Ferrari","Robin Sharma","Personal Development & Fiction",349,8),
("The Richest Man in Babylon","George S. Clason","Accounting & Finance",249,8),
("The Power of Now","Eckhart Tolle","Personal Development & Fiction",399,7),
("The Secret","Rhonda Byrne","Personal Development & Fiction",299,7),
("The Courage to Be Disliked","Ichiro Kishimi and Fumitake Koga","Personal Development & Fiction",399,6),
("Tuesdays with Morrie","Mitch Albom","Personal Development & Fiction",299,7),
("The Diary of a CEO","Steven Bartlett","Business & Management",499,6),
("The One Thing","Gary Keller and Jay Papasan","Business & Management",399,6),
("The Mountain Is You","Brianna Wiest","Personal Development & Fiction",399,7),
("The Art of War","Sun Tzu","Business & Management",199,8),
# Twenty more international and contemporary bestsellers
("The Housemaid","Freida McFadden","Personal Development & Fiction",449,7),
("The Housemaid's Secret","Freida McFadden","Personal Development & Fiction",449,6),
("The Housemaid Is Watching","Freida McFadden","Personal Development & Fiction",449,5),
("Never Lie","Freida McFadden","Personal Development & Fiction",399,6),
("The Let Them Theory","Mel Robbins","Personal Development & Fiction",499,8),
("Project Hail Mary","Andy Weir","Science & Technology",499,6),
("Onyx Storm","Rebecca Yarros","Personal Development & Fiction",699,4),
("Sunrise on the Reaping","Suzanne Collins","Personal Development & Fiction",599,5),
("The Secret of Secrets","Dan Brown","Personal Development & Fiction",799,4),
("The Thursday Murder Club","Richard Osman","Personal Development & Fiction",399,5),
("Harry Potter and the Philosopher's Stone","J. K. Rowling","Personal Development & Fiction",399,8),
("The Little Prince","Antoine de Saint-Exupéry","Personal Development & Fiction",199,8),
("Where the Crawdads Sing","Delia Owens","Personal Development & Fiction",399,6),
("It Ends with Us","Colleen Hoover","Personal Development & Fiction",399,6),
("The Hunger Games","Suzanne Collins","Personal Development & Fiction",349,7),
("The Hobbit","J. R. R. Tolkien","Personal Development & Fiction",399,6),
("The Lord of the Rings","J. R. R. Tolkien","Personal Development & Fiction",899,4),
("The Girl on the Train","Paula Hawkins","Personal Development & Fiction",349,6),
("The Da Vinci Code","Dan Brown","Personal Development & Fiction",399,7),
("The Fault in Our Stars","John Green","Personal Development & Fiction",349,6),
# Thirty more self-help and ideas bestsellers
("Thinking, Fast and Slow","Daniel Kahneman","Personal Development & Fiction",599,6),
("Mindset: The New Psychology of Success","Carol S. Dweck","Personal Development & Fiction",449,7),
("Grit","Angela Duckworth","Personal Development & Fiction",449,6),
("The Power of Habit","Charles Duhigg","Personal Development & Fiction",449,8),
("Tiny Habits","B. J. Fogg","Personal Development & Fiction",449,6),
("Make Your Bed","William H. McRaven","Personal Development & Fiction",299,7),
("Awaken the Giant Within","Tony Robbins","Personal Development & Fiction",499,5),
("You Are a Badass","Jen Sincero","Personal Development & Fiction",399,7),
("Daring Greatly","Brené Brown","Personal Development & Fiction",449,6),
("The Gifts of Imperfection","Brené Brown","Personal Development & Fiction",399,6),
("Big Magic","Elizabeth Gilbert","Personal Development & Fiction",399,5),
("Essentialism","Greg McKeown","Personal Development & Fiction",449,7),
("Drive","Daniel H. Pink","Personal Development & Fiction",399,6),
("Outliers","Malcolm Gladwell","Personal Development & Fiction",449,7),
("Emotional Intelligence","Daniel Goleman","Personal Development & Fiction",499,5),
("Influence: The Psychology of Persuasion","Robert B. Cialdini","Personal Development & Fiction",549,6),
("The Magic of Thinking Big","David J. Schwartz","Personal Development & Fiction",349,7),
("Eat That Frog!","Brian Tracy","Personal Development & Fiction",299,8),
("Getting Things Done","David Allen","Personal Development & Fiction",499,5),
("The Compound Effect","Darren Hardy","Personal Development & Fiction",349,7),
("The Obstacle Is the Way","Ryan Holiday","Personal Development & Fiction",399,6),
("Ego Is the Enemy","Ryan Holiday","Personal Development & Fiction",399,6),
("Meditations","Marcus Aurelius","Personal Development & Fiction",249,9),
("The Untethered Soul","Michael A. Singer","Personal Development & Fiction",399,6),
("Quiet","Susan Cain","Personal Development & Fiction",449,5),
("Never Split the Difference","Chris Voss","Personal Development & Fiction",449,7),
("12 Rules for Life","Jordan B. Peterson","Personal Development & Fiction",499,6),
("The Miracle Morning","Hal Elrod","Personal Development & Fiction",349,7),
("Designing Your Life","Bill Burnett and Dave Evans","Personal Development & Fiction",449,5),
("How to Stop Worrying and Start Living","Dale Carnegie","Personal Development & Fiction",299,8),
]

# The old "Personal Development & Fiction" shelf is split into four clearer subjects.
THRILLERS = {"The Silent Patient","The Housemaid","The Housemaid's Secret","The Housemaid Is Watching","Never Lie",
             "The Secret of Secrets","The Thursday Murder Club","The Girl on the Train","The Da Vinci Code"}
FANTASY_YA = {"Harry Potter and the Philosopher's Stone","The Hobbit","The Lord of the Rings","The Hunger Games",
              "Sunrise on the Reaping","Onyx Storm","The Fault in Our Stars"}
FICTION = {"The Alchemist","The Kite Runner","A Thousand Splendid Suns","1984","Animal Farm","The Great Gatsby",
           "To Kill a Mockingbird","The Book Thief","The Midnight Library","The Little Prince",
           "Where the Crawdads Sing","It Ends with Us"}

def better_category(title, category):
    if category != "Personal Development & Fiction": return category
    if title in THRILLERS: return "Thrillers & Mystery"
    if title in FANTASY_YA: return "Fantasy & Young Adult"
    if title in FICTION: return "Fiction & Classics"
    return "Self-help & Ideas"

BOOKS = [{"id":i+1,"title":r[0],"author":r[1],"category":better_category(r[0],r[2]),"price":r[3],"stock":r[4]} for i,r in enumerate(RAW_BOOKS)]
PAGES = ["Catalogue","Book Bundles","Shopping Cart","Checkout","Find a Book","About PageNest"]
ALL_PAGES = PAGES + ["Book Details"]
PER_PAGE = 12
STATES = ["Andhra Pradesh","Arunachal Pradesh","Assam","Bihar","Chhattisgarh","Goa","Gujarat","Haryana","Himachal Pradesh",
          "Jharkhand","Karnataka","Kerala","Madhya Pradesh","Maharashtra","Manipur","Meghalaya","Mizoram","Nagaland","Odisha",
          "Punjab","Rajasthan","Sikkim","Tamil Nadu","Telangana","Tripura","Uttar Pradesh","Uttarakhand","West Bengal",
          "Andaman and Nicobar Islands","Chandigarh","Dadra and Nagar Haveli and Daman and Diu","Delhi","Jammu and Kashmir",
          "Ladakh","Lakshadweep","Puducherry"]

# ----------------------- SESSION -----------------------
if "page" not in st.session_state or st.session_state.page not in ALL_PAGES:
    st.session_state.page = "Catalogue"
if "cart" not in st.session_state: st.session_state.cart = {}
if "bundles" not in st.session_state: st.session_state.bundles = []
if "wishlist" not in st.session_state: st.session_state.wishlist = []
if "stock" not in st.session_state: st.session_state.stock = {b["id"]: b["stock"] for b in BOOKS}
if "detail_id" not in st.session_state: st.session_state.detail_id = None
if "catalogue_page" not in st.session_state: st.session_state.catalogue_page = 0
if "last_order" not in st.session_state: st.session_state.last_order = None
if "completed_order" not in st.session_state: st.session_state.completed_order = None
if "find_book_title" not in st.session_state: st.session_state.find_book_title = ""
if "tile_cat" not in st.session_state: st.session_state.tile_cat = None
if "support_messages" not in st.session_state:
    st.session_state.support_messages = [{"role":"assistant","content":"Hi! I'm PageNest Help. Ask me about books, bundles, discounts, checkout, or unavailable titles. This demo doesn't process payments."}]

# Stock shown in the shop follows what is left after confirmed orders in this session.
for _b in BOOKS:
    _b["stock"] = st.session_state.stock.get(_b["id"], _b["stock"])

def go(page):
    # Update only the app page state. Do not mutate a widget key after its widget
    # has been instantiated in this run; that causes StreamlitWidgetAlreadyInstantiatedError.
    if page in ALL_PAGES:
        st.session_state.page = page
    st.rerun()

def open_book(book_id):
    st.session_state.detail_id = book_id
    go("Book Details")

def get_book(book_id):
    return next(b for b in BOOKS if b["id"] == book_id)

def cart_count():
    return sum(st.session_state.cart.values())

def subtotal():
    return sum(get_book(i)["price"] * q for i,q in st.session_state.cart.items())

def bundle_discount():
    """10% off each bundle, but only while every book of that bundle is still in the cart."""
    total = 0.0
    kept = []
    for ids in st.session_state.bundles:
        if all(i in st.session_state.cart for i in ids):
            total += round(sum(get_book(i)["price"] for i in ids) * 0.1, 2)
            kept.append(ids)
    st.session_state.bundles = kept
    return min(total, subtotal())

def norm(value):
    return " ".join(re.sub(r"[^a-zA-Z0-9 ]"," ",str(value).lower()).split())

def similarity(a,b):
    return SequenceMatcher(None,norm(a),norm(b)).ratio()

def add_to_cart(book_id, quantity=1):
    book=get_book(book_id)
    current=st.session_state.cart.get(book_id,0)
    if current+quantity>book["stock"]:
        st.warning("Sorry, that is more than the available demo stock.")
        return False
    st.session_state.cart[book_id]=current+quantity
    st.toast("Added to your cart!")
    return True

# ----------------------- COVERS -----------------------
# Want to pin a cover yourself? Add  "Exact Book Title": "https://link-to-image.jpg"  below.
# Pinned covers are always used first.
COVER_OVERRIDES = {}

# Words that mark study guides, summaries, graphic novels etc. so they are never used as a cover.
BAD_COVER_WORDS = ("summary","study guide","graphic novel","workbook","analysis","sparknotes","cliffsnotes",
                   "companion","trivia","coloring","colouring","notes on","a day with","for dummies","journal",
                   "planner","box set","teacher","lesson plan","quicklet","instaread","audio")

@st.cache_resource
def cover_store():
    """Shared across visitors: found covers are remembered; misses are retried after 10 minutes."""
    return {"hit": {}, "miss": {}}

def cover_title_score(want, got):
    w, g = norm(want), norm(got)
    if not g: return 0.0
    for bad in BAD_COVER_WORDS:
        if bad in g and bad not in w: return 0.0
    return max(similarity(w, g), similarity(norm(want.split(":")[0]), norm(got.split(":")[0])))

def cover_author_ok(author, names):
    if not names: return True
    tokens = [t for t in norm(author).split() if len(t) > 2]
    if not tokens: return True
    words = norm(" ".join(names)).split()
    return any(t in words for t in tokens)

def cover_image_ok(url):
    """Download the image and make sure it is a real picture (not a 404 or a tiny 'no image' placeholder)."""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "PageNestBookstore/1.0 (demo bookstore)"})
        with urllib.request.urlopen(req, timeout=6) as r:
            ctype = r.headers.get("Content-Type", "")
            data = r.read(300000)
        return ctype.startswith("image") and len(data) > 3000
    except Exception:
        return False

def fetch_cover(title, author):
    """Try Open Library and Google Books several ways. Returns (image_url or None, number_of_failed_requests)."""
    def get_json(url):
        req = urllib.request.Request(url, headers={"User-Agent": "PageNestBookstore/1.0 (demo bookstore)"})
        with urllib.request.urlopen(req, timeout=6) as r:
            return json.loads(r.read().decode("utf-8"))
    candidates, errors = [], 0
    last_name = (norm(author).split() or [""])[-1]
    ol_fields = "title,author_name,cover_i"

    def open_library(params):
        params = dict(params, limit=10, fields=ol_fields)
        for item in get_json("https://openlibrary.org/search.json?" + urllib.parse.urlencode(params)).get("docs", []):
            cid = item.get("cover_i")
            if not cid or not cover_author_ok(author, item.get("author_name", [])): continue
            candidates.append((cover_title_score(title, item.get("title", "")),
                               f"https://covers.openlibrary.org/b/id/{cid}-L.jpg?default=false"))

    def google_books(query):
        url = "https://www.googleapis.com/books/v1/volumes?" + urllib.parse.urlencode(
            {"q": query, "maxResults": 10, "printType": "books"})
        for item in get_json(url).get("items", []):
            info = item.get("volumeInfo", {})
            links = info.get("imageLinks", {})
            image = (links.get("extraLarge") or links.get("large") or links.get("medium")
                     or links.get("thumbnail") or links.get("smallThumbnail"))
            if not image or not cover_author_ok(author, info.get("authors", [])): continue
            candidates.append((cover_title_score(title, info.get("title", "")) - 0.02,
                               image.replace("http://", "https://").replace("&edge=curl", "")))

    lookups = [
        lambda: open_library({"title": title, "author": author}),
        lambda: google_books(f'intitle:"{title}" inauthor:{last_name}'),
        lambda: open_library({"q": f"{title} {author}"}),
        lambda: google_books(f"{title} {author}"),
        lambda: open_library({"title": title}),
    ]
    tried = set()
    for lookup in lookups:
        try: lookup()
        except Exception: errors += 1
        for score, url in sorted(candidates, key=lambda c: -c[0]):
            if score < 0.72 or url in tried: continue
            tried.add(url)
            if cover_image_ok(url): return url, errors
    return None, errors

def remember_cover(book, url, errors):
    store = cover_store()
    key = (book["title"], book["author"])
    if url: store["hit"][key] = url
    else: store["miss"][key] = time.time() - (540 if errors else 0)  # after network errors retry in ~1 minute

def prefetch_covers(books):
    """Look up several covers at once so pages load quickly."""
    store, now = cover_store(), time.time()
    todo = [b for b in books if b["title"] not in COVER_OVERRIDES
            and (b["title"], b["author"]) not in store["hit"]
            and now - store["miss"].get((b["title"], b["author"]), 0) >= 600]
    if not todo: return
    with ThreadPoolExecutor(max_workers=8) as pool:
        futures = {pool.submit(fetch_cover, b["title"], b["author"]): b for b in todo}
        for future in as_completed(futures):
            try: url, errors = future.result()
            except Exception: url, errors = None, 1
            remember_cover(futures[future], url, errors)

def book_cover(title, author):
    if title in COVER_OVERRIDES: return COVER_OVERRIDES[title]
    store, key = cover_store(), (title, author)
    if key in store["hit"]: return store["hit"][key]
    if time.time() - store["miss"].get(key, 0) < 600: return None
    url, errors = fetch_cover(title, author)
    remember_cover({"title": title, "author": author}, url, errors)
    return url

COVER_GRADIENTS = [("#14213D","#2F4858"),("#1F3A2E","#3F6B55"),("#5B3A5E","#2F2540"),("#8C3B2E","#3E1713"),
                   ("#3D5A80","#16263D"),("#6B5A2E","#2B230E"),("#2F4858","#0F1E27"),("#7A4E3A","#2E1A12")]

def generated_cover_html(book):
    """A designed cover (title + author) used only when no real cover image could be found."""
    a, b = COVER_GRADIENTS[sum(map(ord, book["title"])) % len(COVER_GRADIENTS)]
    n = len(book["title"])
    size = 22 if n <= 20 else 18 if n <= 40 else 15
    return (f'<div class="gen-cover" style="background:linear-gradient(160deg,{a},{b})"><div class="gc-rule"></div>'
            f'<div class="gc-title" style="font-size:{size}px">{html.escape(book["title"])}</div><div class="gc-rule"></div>'
            f'<div class="gc-author" style="margin-top:14px">{html.escape(book["author"]).upper()}</div></div>')

def show_cover(book, search_link=False):
    cover = book_cover(book["title"], book["author"])
    if cover:
        st.image(cover, use_container_width=True)
    else:
        st.markdown(generated_cover_html(book), unsafe_allow_html=True)
        if search_link:
            q = urllib.parse.quote(f'{book["title"]} {book["author"]} book cover')
            st.markdown(f"[Find a cover image](https://www.google.com/search?tbm=isch&q={q})")

def render_book_card(book,prefix="book"):
    with st.container(border=True):
        show_cover(book, True)
        st.markdown(card_meta_html(book),unsafe_allow_html=True)
        b1,b2=st.columns([3,2])
        if book["stock"]>0:
            if b1.button("＋ Add to Cart",key=f"{prefix}_add_{book['id']}",use_container_width=True):
                add_to_cart(book["id"])
                st.rerun()
        else:
            if b1.button("Find this book",key=f"{prefix}_find_{book['id']}",use_container_width=True):
                st.session_state.find_book_title=book["title"]
                go("Find a Book")
        if b2.button("Details",key=f"{prefix}_det_{book['id']}",use_container_width=True):
            open_book(book["id"])

def scroll_to(anchor):
    """Smoothly scroll the page to an element id (used after Browse / paging)."""
    components.html(
        '<script>setTimeout(function(){var d=window.parent.document;var el=d.getElementById("'+anchor+'");'
        'if(el){el.scrollIntoView({behavior:"smooth",block:"start"});}},350);</script>', height=0)

# ----------------------- ONLINE READING -----------------------
def find_online_editions(title, author):
    """Look for a readable online edition via Google Books and Open Library / Internet Archive.
    Results are remembered for this session; failed lookups are not cached so they can be retried."""
    cache = st.session_state.setdefault("edition_cache", {})
    key = (title, author)
    if key in cache: return cache[key]
    def get_json(url):
        req=urllib.request.Request(url,headers={"User-Agent":"PageNestBookstore/1.0"})
        with urllib.request.urlopen(req,timeout=6) as response:
            return json.loads(response.read().decode("utf-8"))
    found={"google":None,"archive":None}
    errors=0
    try:
        url="https://www.googleapis.com/books/v1/volumes?"+urllib.parse.urlencode({
            "q":f'intitle:"{title}" inauthor:"{author}"',"maxResults":10,"printType":"books"})
        partial=None
        for item in get_json(url).get("items",[]):
            info=item.get("volumeInfo",{})
            if similarity(title,info.get("title",""))<0.58: continue
            authors=info.get("authors",[])
            if authors and not any(similarity(author,n)>0.45 for n in authors): continue
            acc=item.get("accessInfo",{})
            view=acc.get("viewability")
            if view not in ("ALL_PAGES","PARTIAL"): continue
            cand={"id":item.get("id"),"view":view,"embeddable":bool(acc.get("embeddable")),
                  "link":info.get("previewLink") or acc.get("webReaderLink")}
            if view=="ALL_PAGES":
                found["google"]=cand; break
            if partial is None: partial=cand
        if found["google"] is None: found["google"]=partial
    except Exception:
        errors+=1
    try:
        url="https://openlibrary.org/search.json?"+urllib.parse.urlencode({
            "title":title,"author":author,"limit":10,"fields":"key,title,author_name,ia,ebook_access"})
        for item in get_json(url).get("docs",[]):
            if similarity(title,item.get("title",""))<0.58: continue
            authors=item.get("author_name",[])
            if authors and not any(similarity(author,n)>0.45 for n in authors): continue
            ia=item.get("ia") or []
            access=item.get("ebook_access")
            if ia and access in ("public","borrowable"):
                if found["archive"] is None or access=="public":
                    found["archive"]={"ia":ia[0],"access":access,"url":"https://openlibrary.org"+item.get("key","")}
                if access=="public": break
    except Exception:
        errors+=1
    if errors==0: cache[key]=found
    return found

def reader_frame(src):
    components.html(
        f'<iframe src="{html.escape(src)}" style="width:100%;height:740px;border:1px solid #E7DFD0;'
        'border-radius:12px;background:#fff" allowfullscreen></iframe>', height=750)

def render_online_reader(book):
    st.markdown(section_title("Read online","Read in your browser, no download needed",eyebrow="Digital edition"),unsafe_allow_html=True)
    with st.spinner("Looking for an online edition..."):
        ed=find_online_editions(book["title"],book["author"])
    g,a=ed["google"],ed["archive"]
    shown=False
    if g and g["view"]=="ALL_PAGES" and g["embeddable"]:
        st.success("The full book is available to read free online (public-domain edition).")
        reader_frame(f"https://books.google.com/books?id={urllib.parse.quote(g['id'])}&pg=PP1&output=embed"); shown=True
    elif a and a["access"]=="public":
        st.success("A free full-text edition is available from the Internet Archive.")
        reader_frame(f"https://archive.org/embed/{urllib.parse.quote(a['ia'])}"); shown=True
    elif g and g["embeddable"]:
        st.info("Preview available: for this title the publisher allows only a limited number of pages to be read online.")
        reader_frame(f"https://books.google.com/books?id={urllib.parse.quote(g['id'])}&pg=PP1&output=embed"); shown=True
    if a and a["access"]=="borrowable":
        st.info("This title can be borrowed digitally for free from Open Library (a free account is needed).")
    if not shown and not a and not (g and g.get("link")):
        st.warning("No free online edition was found for this title. A Kindle or other e-book edition may still exist; see the links below.")
    q=urllib.parse.quote(f'{book["title"]} {book["author"]} kindle ebook')
    links=[]
    if g and g.get("link"): links.append(f"[Open in Google Books]({g['link']})")
    if a: links.append(f"[Open on Open Library]({a['url']})")
    links.append(f"[Search for a Kindle / e-book edition](https://www.google.com/search?q={q})")
    st.markdown("  ·  ".join(links))
    st.caption("Online editions come from Google Books and Open Library / Internet Archive and are not part of this demo order. "
               "Most recent books offer a preview only; older public-domain books can be read in full.")

# ----------------------- PDF INVOICE -----------------------
def create_invoice_pdf(order, cart_snapshot):
    """Create a clean A4 invoice with supported currency text and non-overlapping totals."""
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_CENTER, TA_RIGHT
    from reportlab.lib.units import mm
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=A4, rightMargin=17*mm, leftMargin=17*mm,
        topMargin=15*mm, bottomMargin=17*mm
    )
    navy = colors.HexColor("#17345E")
    blue = colors.HexColor("#2458A6")
    pale = colors.HexColor("#EAF1FB")
    gray = colors.HexColor("#65728A")
    border = colors.HexColor("#D4DEEC")

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="Brand", parent=styles["Title"], fontName="Helvetica-Bold", fontSize=24, leading=28, textColor=navy, alignment=0, spaceAfter=4))
    styles.add(ParagraphStyle(name="SmallMuted", parent=styles["Normal"], fontSize=8.5, leading=12, textColor=gray))
    styles.add(ParagraphStyle(name="SectionHead", parent=styles["Heading2"], fontSize=11, leading=14, textColor=navy, spaceBefore=6, spaceAfter=5))
    styles.add(ParagraphStyle(name="Right", parent=styles["Normal"], alignment=TA_RIGHT, fontSize=9, leading=12))
    styles.add(ParagraphStyle(name="Tiny", parent=styles["Normal"], fontSize=8.5, leading=11))
    styles.add(ParagraphStyle(name="CenterSmall", parent=styles["Normal"], alignment=TA_CENTER, fontSize=8, leading=11, textColor=gray))

    story = []
    header_left = [Paragraph("PageNest", styles["Brand"]), Paragraph("BOOKS &amp; LEARNING", styles["SmallMuted"]), Paragraph("Digital order invoice", styles["SmallMuted"])]
    header_right = [
        Paragraph(f"<b>INVOICE</b><br/>{order['invoice_id']}", styles["Right"]),
        Paragraph(f"<b>Date:</b> {order['order_date']}", styles["Right"]),
        Paragraph("<b>Status:</b> Demo order", styles["Right"]),
    ]
    head = Table([[header_left, header_right]], colWidths=[105*mm, 65*mm])
    head.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), pale), ("BOX", (0,0), (-1,-1), 0.6, border),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"), ("LEFTPADDING", (0,0), (-1,-1), 10),
        ("RIGHTPADDING", (0,0), (-1,-1), 10), ("TOPPADDING", (0,0), (-1,-1), 10),
        ("BOTTOMPADDING", (0,0), (-1,-1), 10)
    ]))
    story += [head, Spacer(1, 7*mm)]

    customer = [
        Paragraph("<b>BILLED TO</b>", styles["SectionHead"]),
        Paragraph(order["name"].replace("&", "&amp;"), styles["Tiny"]),
        Paragraph(order["email"].replace("&", "&amp;"), styles["Tiny"]),
        Paragraph(order["phone"], styles["Tiny"]),
        Paragraph(order["address"].replace("&", "&amp;").replace("\n", "<br/>"), styles["Tiny"]),
        Paragraph(f"{order['city']}, {order['state']} {order['pincode']}", styles["Tiny"]),
        Paragraph(f"Customer GSTIN: {order['gstin'] or 'Not provided'}", styles["SmallMuted"])
    ]
    seller = [
        Paragraph("<b>SELLER DETAILS</b>", styles["SectionHead"]),
        Paragraph("PageNest Books &amp; Learning", styles["Tiny"]),
        Paragraph("Online demo bookstore", styles["Tiny"]),
        Paragraph("Seller GSTIN: Not configured", styles["SmallMuted"]),
        Paragraph("This is a demonstration invoice.", styles["SmallMuted"]),
        Paragraph("No payment has been collected.", styles["SmallMuted"])
    ]
    parties = Table([[customer, seller]], colWidths=[88*mm, 82*mm])
    parties.setStyle(TableStyle([
        ("VALIGN", (0,0), (-1,-1), "TOP"), ("BOX", (0,0), (-1,-1), 0.5, border),
        ("INNERGRID", (0,0), (-1,-1), 0.4, colors.HexColor("#E0E6EF")),
        ("LEFTPADDING", (0,0), (-1,-1), 9), ("RIGHTPADDING", (0,0), (-1,-1), 9),
        ("TOPPADDING", (0,0), (-1,-1), 6), ("BOTTOMPADDING", (0,0), (-1,-1), 8)
    ]))
    story += [parties, Spacer(1, 6*mm), Paragraph("ORDER ITEMS", styles["SectionHead"])]

    data = [["S.No.", "Book / Description", "Qty", "Unit Price", "Amount"]]
    for idx, item in enumerate(cart_snapshot, 1):
        title = item["title"].replace("&", "&amp;")
        data.append([str(idx), Paragraph(title, styles["Tiny"]), str(item["quantity"]), f"INR {item['price']:,.2f}", f"INR {item['price']*item['quantity']:,.2f}"])

    items = Table(data, colWidths=[13*mm, 79*mm, 13*mm, 31*mm, 34*mm], repeatRows=1, hAlign="LEFT")
    items.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), navy), ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"), ("FONTSIZE", (0,0), (-1,0), 8),
        ("FONTSIZE", (0,1), (-1,-1), 8), ("ALIGN", (0,0), (0,-1), "CENTER"),
        ("ALIGN", (2,1), (-1,-1), "RIGHT"), ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("GRID", (0,0), (-1,-1), 0.4, border), ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, pale]),
        ("LEFTPADDING", (0,0), (-1,-1), 5), ("RIGHTPADDING", (0,0), (-1,-1), 5),
        ("TOPPADDING", (0,0), (-1,-1), 7), ("BOTTOMPADDING", (0,0), (-1,-1), 7)
    ]))
    story += [items, Spacer(1, 5*mm)]

    delivery_payment = [
        Paragraph(f"<b>Delivery option:</b> {order['delivery_option']}", styles["Tiny"]),
        Paragraph(f"<b>Estimated arrival:</b> {order['delivery_eta']}", styles["Tiny"]),
        Paragraph(f"<b>Payment method:</b> {order['payment_method']} (demo selection only)", styles["Tiny"])
    ]
    story += [KeepTogether(delivery_payment), Spacer(1, 4*mm)]

    totals = [
        ["Subtotal", f"INR {order['subtotal']:,.2f}"],
        ["Bundle discount", f"- INR {order['bundle_discount']:,.2f}"],
        ["Discount code", f"- INR {order['code_discount']:,.2f}"],
        ["Delivery fee", f"INR {order['delivery_fee']:,.2f}"],
        ["Total discount", f"- INR {order['discount']:,.2f}"],
        ["AMOUNT DUE", f"INR {order['total']:,.2f}"]
    ]
    total_table = Table(totals, colWidths=[47*mm, 38*mm], hAlign="RIGHT")
    total_table.setStyle(TableStyle([
        ("ALIGN", (1,0), (1,-1), "RIGHT"), ("FONTNAME", (0,0), (-1,-2), "Helvetica"),
        ("FONTSIZE", (0,0), (-1,-1), 8.5), ("LINEABOVE", (0,-1), (-1,-1), 1, blue),
        ("BACKGROUND", (0,-1), (-1,-1), navy), ("TEXTCOLOR", (0,-1), (-1,-1), colors.white),
        ("FONTNAME", (0,-1), (-1,-1), "Helvetica-Bold"), ("FONTSIZE", (0,-1), (-1,-1), 10),
        ("LEFTPADDING", (0,0), (-1,-1), 7), ("RIGHTPADDING", (0,0), (-1,-1), 7),
        ("TOPPADDING", (0,0), (-1,-1), 6), ("BOTTOMPADDING", (0,0), (-1,-1), 6)
    ]))
    story += [total_table, Spacer(1, 7*mm)]
    story.append(Paragraph("Demo invoice only. No payment processed. Tax is not charged or represented in this sample bill. Configure verified seller and tax details before commercial use.", styles["CenterSmall"]))
    story.append(Spacer(1, 3*mm))
    story.append(Paragraph("Thank you for shopping with PageNest.", ParagraphStyle(name="Thanks", parent=styles["Normal"], fontSize=12, leading=16, textColor=navy, alignment=TA_CENTER)))

    def draw_footer(canvas, doc):
        canvas.saveState()
        canvas.setStrokeColor(border)
        canvas.line(17*mm, 12*mm, A4[0]-17*mm, 12*mm)
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(gray)
        canvas.drawString(17*mm, 7*mm, "PageNest | Books & Learning")
        canvas.drawRightString(A4[0]-17*mm, 7*mm, f"Page {doc.page}")
        canvas.restoreState()

    doc.build(story, onFirstPage=draw_footer, onLaterPages=draw_footer)
    return buffer.getvalue()

# ----------------------- SIDEBAR -----------------------
with st.sidebar:
    st.markdown("## 📚 PageNest")
    st.caption("Your personal bookstore")
    # A page-specific key keeps the radio aligned with button-based navigation
    # without changing an already-instantiated widget's state.
    current_page = st.session_state.page
    nav_key = f"navigation_radio_{current_page}"
    selected_nav = st.radio("Navigate", PAGES, index=PAGES.index(current_page) if current_page in PAGES else None, key=nav_key)
    if selected_nav is not None and selected_nav != current_page:
        st.session_state.page = selected_nav
        st.rerun()
    st.divider()
    st.markdown("### 🔎 Find your next book")
    search_query=st.text_input("Search title or author",placeholder="e.g. mankiw economics",key="sidebar_search")
    categories=["All Subjects"]+sorted(set(b["category"] for b in BOOKS))
    selected_category=st.selectbox("Subject",categories,key="sidebar_subject")
    price_limit=st.slider("Maximum price (₹)",100,1500,1500,100,key="sidebar_price")
    availability=st.selectbox("Availability",["All Books","In Stock","Out of Stock"],key="sidebar_availability")
    st.divider()
    st.markdown("### 🛒 Your Cart")
    st.metric("Items",cart_count())
    st.metric("Subtotal",f"₹{subtotal():,.2f}")
    if st.button("View Cart",use_container_width=True): go("Shopping Cart")
    st.divider()
    st.markdown("### 💬 PageNest Help")
    st.caption("Ask about books, bundles, discounts or checkout.")
    for message in st.session_state.support_messages[-4:]:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    prompt=st.chat_input("Ask PageNest Help...",key="help_chat_input")
    if prompt:
        st.session_state.support_messages.append({"role":"user","content":prompt})
        q=prompt.lower()
        if any(w in q for w in ["discount","coupon","code","offer"]):
            reply="Use PAGENEST10 at checkout for 10% off after bundle savings. Bundles show their own 10% savings."
        elif any(w in q for w in ["cart","checkout","pay","payment","gst","gstin"]):
            reply="Add books to your cart, open Shopping Cart and click Proceed to Checkout. Fill in the required delivery fields; GSTIN is optional. This demo does not process real payments."
        elif any(w in q for w in ["unavailable","out of stock","restock","store","nearby"]):
            reply="Open Find a Book, enter the title and your area, then click Find Book & Stores. The seven-day estimate is illustrative, not live supplier data."
        elif any(w in q for w in ["bundle","class","course","semester"]):
            reply="Open Book Bundles for Commerce & BBA, BBA/MBA, CAT, UPSC, Python & Research, JEE and NEET."
        else:
            reply="I can help with catalogue search, bundles, PAGENEST10, checkout, GSTIN and unavailable books."
        st.session_state.support_messages.append({"role":"assistant","content":reply})
        st.rerun()

with st.sidebar:
    st.divider()
    with st.expander("🔧 Cover checker"):
        st.caption("Looks up a cover for every book and lists any that are still missing. This can take a minute or two.")
        if st.button("Check all covers",key="cover_check_btn",use_container_width=True):
            _store=cover_store()
            _store["miss"].clear()
            _bar=st.progress(0.0,text="Checking covers...")
            for _start in range(0,len(BOOKS),24):
                prefetch_covers(BOOKS[_start:_start+24])
                _done=min(_start+24,len(BOOKS))
                _bar.progress(_done/len(BOOKS),text=f"Checked {_done} of {len(BOOKS)}")
            _bar.empty()
            st.session_state.cover_report=[f'{b["title"]} — {b["author"]}' for b in BOOKS
                                           if (b["title"],b["author"]) not in _store["hit"] and b["title"] not in COVER_OVERRIDES]
        _report=st.session_state.get("cover_report")
        if _report is not None:
            if not _report:
                st.success("Every book has a cover image.")
            else:
                st.warning(f"{len(_report)} book(s) have no cover image yet. They show a designed cover instead. "
                           "To pin a picture, add the title and an image link to COVER_OVERRIDES in the code.")
                st.write("\n".join(f"- {line}" for line in _report))

# ----------------------- TOP BAR, NAV & HERO -----------------------
st.markdown(announce_html(), unsafe_allow_html=True)

nav_cols = st.columns([2.4, 1, 1, 1.3, 1, 1.4])
with nav_cols[0]:
    st.markdown('<span class="topnav-marker"></span><div class="brand">PAGENEST<small>BOOKS &amp; LEARNING</small></div>', unsafe_allow_html=True)
for _col, (_label, _target) in zip(nav_cols[1:5], [("Home","Catalogue"),("Bundles","Book Bundles"),("Find a Book","Find a Book"),("About","About PageNest")]):
    if _col.button(_label, key=f"topnav_{_target}", use_container_width=True): go(_target)
if nav_cols[5].button(f"🛒 Cart ({cart_count()})", key="topnav_cart", use_container_width=True): go("Shopping Cart")

st.markdown(hero_html(len(BOOKS), len(set(b["category"] for b in BOOKS)), cart_count(), st.session_state.page=="Catalogue"), unsafe_allow_html=True)

# ----------------------- FILTERED CATALOGUE -----------------------
filtered=BOOKS.copy()
search_tokens=norm(search_query).split()
if search_tokens:
    filtered=[b for b in filtered if all(t in norm(b["title"]+" "+b["author"]+" "+b["category"]) for t in search_tokens)]
if selected_category!="All Subjects": filtered=[b for b in filtered if b["category"]==selected_category]
if st.session_state.tile_cat: filtered=[b for b in filtered if b["category"]==st.session_state.tile_cat]
filtered=[b for b in filtered if b["price"]<=price_limit]
if availability=="In Stock": filtered=[b for b in filtered if b["stock"]>0]
elif availability=="Out of Stock": filtered=[b for b in filtered if b["stock"]==0]

# ----------------------- CATALOGUE PAGE -----------------------
if st.session_state.page=="Catalogue":
    st.markdown(features_html(), unsafe_allow_html=True)

    # Browse by category tiles
    st.markdown(section_title("Find your next read","Pick a subject to filter the catalogue",eyebrow="Browse by category",anchor="categories"),unsafe_allow_html=True)
    tile_cols=st.columns(6)
    for idx,(col,(tname,ticon,ttag,tbg)) in enumerate(zip(tile_cols,CATEGORY_TILES)):
        n=sum(1 for b in BOOKS if b["category"]==tname)
        with col:
            st.markdown(
                f'<div class="cat-tile" style="background:{tbg}"><div class="cat-ico">{ticon}</div>'
                f'<div class="cat-name">{html.escape(tname)}</div><div class="cat-sub">{html.escape(ttag)} · {n} books</div></div>',
                unsafe_allow_html=True)
            if st.button("Browse",key=f"tile_{idx}",use_container_width=True):
                st.session_state.tile_cat=tname
                st.session_state.catalogue_page=0
                st.session_state.scroll_to_browse=True
                st.rerun()

    st.markdown(section_title("Readers' all-time favourites","Reader favourites right now",eyebrow="Bestsellers",anchor="bestsellers"),unsafe_allow_html=True)

    featured_titles = [
        ("Rich Dad Poor Dad", "Build your financial mindset", "Money & Personal Finance"),
        ("Ikigai", "Discover your reason for being", "Mindfulness & Wellbeing"),
        ("Atomic Habits", "Small habits. Remarkable results.", "Habits & Productivity"),
        ("The Psychology of Money", "Understand how people think about money", "Money & Behaviour"),
        ("The Alchemist", "A journey about dreams and purpose", "Fiction & Inspiration"),
        ("How to Win Friends and Influence People", "Build stronger relationships", "Communication"),
        ("The 7 Habits of Highly Effective People", "Principles for personal effectiveness", "Personal Growth"),
        ("The 48 Laws of Power", "Strategy, influence and power", "Strategy"),
        ("The Monk Who Sold His Ferrari", "A story about purpose and balance", "Mindfulness"),
        ("The Richest Man in Babylon", "Classic lessons about money", "Personal Finance"),
        ("The Power of Now", "Focus on the present moment", "Mindfulness"),
        ("The Secret", "A popular book on mindset", "Personal Development"),
        ("The Courage to Be Disliked", "A different perspective on happiness", "Psychology"),
        ("The Diary of a CEO", "Lessons on business and life", "Business"),
        ("The Housemaid", "A twist-filled psychological thriller", "Global Bestseller"),
        ("The Housemaid's Secret", "A gripping domestic thriller", "Thriller"),
        ("The Housemaid Is Watching", "Suspense from Freida McFadden", "Thriller"),
        ("Never Lie", "A tense psychological mystery", "Mystery"),
        ("The Let Them Theory", "Focus on what you can control", "Personal Growth"),
        ("Project Hail Mary", "A science-fiction mission to save Earth", "Science Fiction"),
        ("Onyx Storm", "Epic fantasy and dragon riders", "Fantasy"),
        ("Sunrise on the Reaping", "Return to the world of Panem", "Young Adult"),
        ("The Secret of Secrets", "A Robert Langdon mystery", "Thriller"),
        ("The Thursday Murder Club", "A cosy mystery with clever detectives", "Mystery"),
        ("Harry Potter and the Philosopher's Stone", "The beginning of a magical adventure", "Fantasy Classic"),
        ("The Little Prince", "A timeless tale about life and love", "Classic"),
        ("Where the Crawdads Sing", "A mystery set in the marshlands", "Literary Fiction"),
        ("It Ends with Us", "A contemporary story of love and resilience", "Contemporary Fiction"),
        ("The Hunger Games", "Survival, courage and rebellion", "Dystopian Fiction"),
        ("The Hobbit", "An adventure through Middle-earth", "Fantasy Classic"),
        ("The Lord of the Rings", "An epic quest through Middle-earth", "Fantasy Classic"),
        ("The Girl on the Train", "A psychological thriller full of secrets", "Thriller"),
        ("The Da Vinci Code", "A fast-paced mystery of codes and history", "Thriller"),
        ("The Fault in Our Stars", "A moving story of love and hope", "Young Adult"),
    ]
    # Only the first 8 are shown up front so the page loads quickly; every title is still in Browse All Books.
    shown_featured = featured_titles[:8]
    prefetch_covers([b for b in BOOKS if b["title"] in {t[0] for t in shown_featured}])
    for row_start in range(0, len(shown_featured), 4):
        featured_cols = st.columns(4)
        for featured_col, (featured_title, tagline, banner_label) in zip(featured_cols, shown_featured[row_start:row_start + 4]):
            featured_book = next((b for b in BOOKS if b["title"] == featured_title), None)
            with featured_col:
                with st.container(border=True):
                    if featured_book:
                        show_cover(featured_book)
                        st.markdown(f'<div class="book-title">{html.escape(featured_title)}</div>', unsafe_allow_html=True)
                        st.caption(tagline)
                        st.markdown(f'<div class="book-price">₹{featured_book["price"]:,}</div><span class="pill">{html.escape(banner_label)}</span>', unsafe_allow_html=True)
                        f1, f2 = st.columns([3, 2])
                        if f1.button("Shop now", key=f"feature_{featured_book['id']}", use_container_width=True):
                            if add_to_cart(featured_book["id"]): st.rerun()
                        if f2.button("Details", key=f"feature_det_{featured_book['id']}", use_container_width=True):
                            open_book(featured_book["id"])

    # Sorting + page reset whenever any filter changes
    sort_by=st.selectbox("Sort by",["Recommended","Price: Low to High","Price: High to Low","Title A–Z"],key="sort_catalogue")
    filter_sig=(search_query,selected_category,price_limit,availability,sort_by,st.session_state.tile_cat)
    if st.session_state.get("filter_sig")!=filter_sig:
        st.session_state.filter_sig=filter_sig
        st.session_state.catalogue_page=0
    if sort_by=="Price: Low to High": filtered.sort(key=lambda b:b["price"])
    elif sort_by=="Price: High to Low": filtered.sort(key=lambda b:b["price"],reverse=True)
    elif sort_by=="Title A–Z": filtered.sort(key=lambda b:b["title"].lower())

    total_pages=max(1,-(-len(filtered)//PER_PAGE))
    st.session_state.catalogue_page=min(st.session_state.catalogue_page,total_pages-1)
    cur=st.session_state.catalogue_page
    first=cur*PER_PAGE
    page_books=filtered[first:first+PER_PAGE]
    note=f"Showing {first+1}–{first+len(page_books)} of {len(filtered)} books" if filtered else "No matching books"
    st.markdown(section_title("Browse all books",note,eyebrow="The full collection",anchor="browse-all"),unsafe_allow_html=True)

    if st.session_state.tile_cat:
        t1,t2=st.columns([4,1])
        t1.info(f"Showing subject: {st.session_state.tile_cat}")
        if t2.button("Show all subjects",key="clear_tile",use_container_width=True):
            st.session_state.tile_cat=None
            st.session_state.catalogue_page=0
            st.session_state.scroll_to_browse=True
            st.rerun()

    def pager(key):
        if total_pages<=1: return
        p1,p2,p3=st.columns([1,2,1])
        if p1.button("← Previous",key=f"prev_{key}",disabled=cur==0,use_container_width=True):
            st.session_state.catalogue_page=cur-1; st.session_state.scroll_to_browse=True; st.rerun()
        p2.markdown(f'<div style="text-align:center;padding-top:8px">Page {cur+1} of {total_pages}</div>',unsafe_allow_html=True)
        if p3.button("Next →",key=f"next_{key}",disabled=cur>=total_pages-1,use_container_width=True):
            st.session_state.catalogue_page=cur+1; st.session_state.scroll_to_browse=True; st.rerun()

    if not filtered:
        st.info("No books match these filters. Try a different subject or price, or look for it elsewhere.")
        if search_query.strip() and st.button("Look for this book in Find a Book",use_container_width=True):
            st.session_state.find_book_title=search_query.strip()
            go("Find a Book")
    pager("top")
    prefetch_covers(page_books)
    for start in range(0,len(page_books),3):
        cols=st.columns(3)
        for col,book in zip(cols,page_books[start:start+3]):
            with col: render_book_card(book,"catalogue")
    pager("bottom")
    if st.session_state.pop("scroll_to_browse",False): scroll_to("browse-all")

    # Newsletter banner (demo: nothing is stored or sent)
    with st.form("newsletter_form",clear_on_submit=True):
        st.markdown('<span class="nl-marker"></span><div class="eyebrow nl-eyebrow">Be part of our reading community</div>'
                    '<h3>Get updates, exclusive deals &amp; book picks</h3>'
                    '<p>Subscribe to hear about new arrivals and offers. This is a demo; your email is not stored.</p>',unsafe_allow_html=True)
        nl1,nl2=st.columns([3,1])
        nl_email=nl1.text_input("Email",placeholder="Enter your email",label_visibility="collapsed")
        nl_submit=nl2.form_submit_button("Subscribe",use_container_width=True)
    if nl_submit:
        if re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+",nl_email.strip()):
            st.success("Thanks for subscribing! (Demo only: no email was saved.)")
        else:
            st.error("Please enter a valid email address.")

# ----------------------- BOOK DETAILS -----------------------
elif st.session_state.page=="Book Details":
    if st.session_state.detail_id is None:
        go("Catalogue")
    book=get_book(st.session_state.detail_id)
    if st.button("← Back to catalogue"): go("Catalogue")
    d1,d2=st.columns([1,3])
    with d1:
        show_cover(book, True)
    with d2:
        st.markdown(f'<span class="pill">{html.escape(book["category"])}</span> {stock_badge(book["stock"])}',unsafe_allow_html=True)
        st.markdown(f"# {book['title']}")
        st.markdown(f"##### by {book['author']}")
        st.markdown(f'<div class="book-price" style="font-size:30px">₹{book["price"]:,}</div>',unsafe_allow_html=True)
        if book["stock"]>0:
            in_cart=st.session_state.cart.get(book["id"],0)
            st.caption(f"{book['stock']} copies in demo stock" + (f" · {in_cart} already in your cart" if in_cart else ""))
            qty=st.number_input("Quantity",min_value=1,max_value=book["stock"],value=1,step=1,key=f"detail_qty_{book['id']}")
            if st.button("＋ Add to Cart",key=f"detail_add_{book['id']}"):
                if add_to_cart(book["id"],int(qty)): st.rerun()
        else:
            st.warning("Currently unavailable")
            if st.button("Find this book",key=f"detail_find_{book['id']}"):
                st.session_state.find_book_title=book["title"]
                go("Find a Book")
        saved=book["id"] in st.session_state.wishlist
        if st.button("♥ Remove from saved" if saved else "♡ Save for later",key=f"detail_wish_{book['id']}"):
            if saved: st.session_state.wishlist.remove(book["id"])
            else: st.session_state.wishlist.append(book["id"])
            st.rerun()
        if st.session_state.get("reader_open")==book["id"]:
            if st.button("✕ Close online reader",key=f"reader_close_{book['id']}"):
                st.session_state.reader_open=None
                st.rerun()
        elif st.button("📖 Read online",key=f"reader_open_btn_{book['id']}"):
            st.session_state.reader_open=book["id"]
            st.rerun()
    if st.session_state.get("reader_open")==book["id"]:
        render_online_reader(book)
    related=[b for b in BOOKS if b["id"]!=book["id"] and (b["author"]==book["author"] or b["category"]==book["category"])]
    related.sort(key=lambda b:(b["author"]!=book["author"],b["title"]))
    related=related[:3]
    if related:
        st.markdown(section_title("You may also like","Same author or subject"),unsafe_allow_html=True)
        rcols=st.columns(3)
        for col,rb in zip(rcols,related):
            with col: render_book_card(rb,"related")

# ----------------------- BUNDLES -----------------------
elif st.session_state.page=="Book Bundles":
    st.markdown(section_title("Curated book bundles","Each bundle gets 10% off",eyebrow="Starter packs"),unsafe_allow_html=True)
    st.write("Useful starter packs for different courses and exams. Each bundle gets 10% off its listed individual prices.")
    bundles=[
      ("Commerce & BBA Starter Bundle","For introductory commerce and BBA courses",["Principles of Economics","Principles of Management","Financial Accounting","Business Mathematics"]),
      ("BBA/MBA Core Bundle","Management, marketing and MBA foundations",["Management","Marketing Management","Organizational Behavior","Business Statistics"]),
      ("CAT Starter Bundle","Quantitative, verbal and vocabulary preparation",["How to Prepare for Quantitative Aptitude for CAT","How to Prepare for Verbal Ability and Reading Comprehension for CAT","Word Power Made Easy"]),
      ("UPSC Foundation Bundle","Polity, geography and modern history",["Indian Polity","Certificate Physical and Human Geography","A Brief History of Modern India"]),
      ("Python & Research Bundle","Coding basics and research methods",["Python Crash Course","Think Python","Research Methodology"]),
      ("JEE Physics & Chemistry Bundle","Foundational physics and chemistry",["Concepts of Physics Volume 1","Physical Chemistry","IIT Mathematics"]),
      ("NEET Biology & Chemistry Bundle","Biology and chemistry preparation",["Objective Biology","Trueman's Elementary Biology","Objective Chemistry for NEET"])
    ]
    for start in range(0,len(bundles),2):
        cols=st.columns(2)
        for col,bundle in zip(cols,bundles[start:start+2]):
            title,desc,titles=bundle
            books=[next((b for b in BOOKS if b["title"]==t),None) for t in titles]
            books=[b for b in books if b]
            total=sum(b["price"] for b in books)
            discounted=round(total*.9,2)
            with col:
                with st.container(border=True):
                    st.markdown(f"### {title}")
                    st.write(desc)
                    for b in books: st.write(f"• {b['title']} — ₹{b['price']:,}")
                    st.write(f"Individual total: ₹{total:,.2f}")
                    st.markdown(f'<div class="book-price">Bundle price: ₹{discounted:,.2f}</div>',unsafe_allow_html=True)
                    if st.button("Add bundle to cart",key="bundle_"+norm(title).replace(" ","_"),use_container_width=True):
                        if all(st.session_state.cart.get(b["id"],0)+1<=b["stock"] for b in books):
                            for b in books: st.session_state.cart[b["id"]]=st.session_state.cart.get(b["id"],0)+1
                            st.session_state.bundles.append([b["id"] for b in books])
                            st.toast("Bundle added with 10% bundle savings.")
                            st.rerun()
                        else: st.error("A title in this bundle does not have enough demo stock.")

# ----------------------- CART -----------------------
elif st.session_state.page=="Shopping Cart":
    st.markdown(section_title("Your shopping cart"),unsafe_allow_html=True)
    if not st.session_state.cart:
        st.info("Your cart is empty.")
        if st.button("Continue Shopping",use_container_width=True): go("Catalogue")
    else:
        for book_id in list(st.session_state.cart):
            book=get_book(book_id); qty=st.session_state.cart[book_id]
            with st.container(border=True):
                c0,c1,c2,c3,c4=st.columns([1,5,1,2,1])
                with c0: show_cover(book)
                c1.markdown(f"**{book['title']}**"); c1.caption(f"{book['author']} · {book['category']}")
                c2.write(f"Qty: {qty}"); c3.write(f"₹{book['price']*qty:,.2f}")
                if c4.button("Remove",key=f"remove_{book_id}"):
                    del st.session_state.cart[book_id]
                    st.rerun()
                q1,q2,_=c1.columns([1,1,3])
                if q1.button("−",key=f"minus_{book_id}"):
                    if qty<=1: del st.session_state.cart[book_id]
                    else: st.session_state.cart[book_id]=qty-1
                    st.rerun()
                if q2.button("+",key=f"plus_{book_id}"):
                    if qty<book["stock"]: st.session_state.cart[book_id]=qty+1; st.rerun()
                    else: st.warning("Maximum demo stock reached.")
        st.divider()
        amount=subtotal()
        bd=bundle_discount()
        st.markdown(f"### Subtotal: ₹{amount:,.2f}")
        if bd: st.write(f"Bundle discount: −₹{bd:,.2f}")
        c1,c2=st.columns(2)
        if c1.button("Continue Shopping",use_container_width=True): go("Catalogue")
        if c2.button("Proceed to Checkout",use_container_width=True): go("Checkout")

    if st.session_state.wishlist:
        st.markdown(section_title("Saved for later"),unsafe_allow_html=True)
        for wid in list(st.session_state.wishlist):
            wb=get_book(wid)
            with st.container(border=True):
                w1,w2,w3,w4=st.columns([5,2,2,1])
                w1.markdown(f"**{wb['title']}**"); w1.caption(wb["author"])
                w2.write(f"₹{wb['price']:,}")
                if wb["stock"]>0:
                    if w3.button("Move to cart",key=f"wmove_{wid}",use_container_width=True):
                        if add_to_cart(wid):
                            st.session_state.wishlist.remove(wid); st.rerun()
                else:
                    w3.caption("Currently unavailable")
                if w4.button("✕",key=f"wdel_{wid}"):
                    st.session_state.wishlist.remove(wid); st.rerun()

# ----------------------- CHECKOUT -----------------------
elif st.session_state.page=="Checkout":
    st.markdown(section_title("Checkout & digital invoice"),unsafe_allow_html=True)
    if not st.session_state.cart:
        completed = st.session_state.get("completed_order")
        if completed:
            st.success("Your demo order has been confirmed!")
            st.markdown(f"### Order number: {completed['invoice_id']}")
            st.write(f"**Customer:** {completed['name']} · {completed['email']}")
            st.write(f"**Delivery:** {completed['delivery_option']} · {completed['delivery_eta']}")
            st.write(f"**Payment preference:** {completed['payment_method']} (demo only; no payment processed)")
            st.metric("Order total", f"INR {completed['total']:,.2f}")
            try:
                completed_pdf = create_invoice_pdf(completed, completed["cart_snapshot"])
                st.download_button(
                    "⬇ Download Order Invoice PDF",
                    data=completed_pdf,
                    file_name=f"{completed['invoice_id']}.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
            except Exception:
                st.error("Could not create the PDF. Check that reportlab is listed in requirements.txt.")
            if st.button("Start a New Order", use_container_width=True):
                st.session_state.completed_order = None
                go("Catalogue")
        else:
            st.info("Your cart is empty.")
            if st.button("Browse Books",use_container_width=True): go("Catalogue")
    else:
        amount=subtotal()
        bd=bundle_discount()
        form_col,sum_col=st.columns([2,1])
        with sum_col:
            with st.container(border=True):
                st.markdown("### Order summary")
                for i,q in st.session_state.cart.items():
                    b=get_book(i)
                    st.markdown(f'<div class="sumrow"><span>{html.escape(b["title"])} × {q}</span><b>₹{b["price"]*q:,}</b></div>',unsafe_allow_html=True)
                st.markdown(f'<div class="sumrow"><span>Subtotal</span><b>₹{amount:,.2f}</b></div>',unsafe_allow_html=True)
                if bd:
                    st.markdown(f'<div class="sumrow"><span>Bundle discount</span><b>−₹{bd:,.2f}</b></div>',unsafe_allow_html=True)
                st.markdown(f'<div class="sumrow total"><span>Before delivery & code</span><span>₹{max(0,amount-bd):,.2f}</span></div>',unsafe_allow_html=True)
                st.caption("Delivery fee and discount code are added in the review step.")
        with form_col:
            with st.form("checkout_form"):
                st.markdown("### Delivery Details")
                full_name=st.text_input("Full Name *")
                email=st.text_input("Email Address *")
                phone=st.text_input("Phone Number *")
                address=st.text_area("Delivery Address *")
                city=st.text_input("City *")
                state=st.selectbox("State *",STATES,index=None,placeholder="Choose your state") or ""
                pincode=st.text_input("PIN Code *",placeholder="6 digits")
                st.markdown("### 🚚 Delivery Options")
                delivery_option=st.radio(
                    "Choose how you want to receive your books",
                    ["Standard Delivery — Free (5–7 business days)", "Express Delivery — ₹99 (2–3 business days)", "Store Pickup — Free (ready in 1–2 business days)"],
                    index=0,
                    help="Delivery times are estimates for this demo and are not live courier commitments."
                )
                delivery_fee=99.0 if delivery_option.startswith("Express Delivery") else 0.0
                delivery_eta=("2–3 business days" if delivery_option.startswith("Express Delivery") else "ready in 1–2 business days" if delivery_option.startswith("Store Pickup") else "5–7 business days")
                st.markdown("### 💳 Payment Options")
                payment_method=st.radio(
                    "Choose a payment method",
                    ["UPI", "Credit / Debit Card", "Net Banking", "Cash on Delivery (COD)"],
                    horizontal=True,
                    help="These are demo selections only. No payment will be collected or processed."
                )
                st.markdown("### Invoice Details")
                gstin=st.text_input("Customer GSTIN (optional)",placeholder="Enter GSTIN if applicable")
                discount_code=st.text_input("Discount Code",placeholder="Try PAGENEST10")
                st.caption("PAGENEST10 gives 10% off after bundle savings. Taxes are not calculated in this demo invoice.")
                submitted=st.form_submit_button("Review order",use_container_width=True)
        if submitted:
            required=[full_name,email,phone,address,city,state,pincode]
            if not all(x.strip() for x in required): st.error("Please complete all required delivery fields.")
            elif not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+",email.strip()): st.error("Please enter a valid email address.")
            elif not re.fullmatch(r"[0-9+\-\s()]{7,20}",phone.strip()): st.error("Please enter a valid phone number.")
            elif not re.fullmatch(r"[1-9][0-9]{5}",pincode.strip()): st.error("PIN code must be 6 digits.")
            elif gstin.strip() and not re.fullmatch(r"[0-9A-Z]{15}",gstin.strip().upper()): st.error("GSTIN should contain 15 alphanumeric characters.")
            else:
                after_bundle=max(0,amount-bd)
                code_discount=round(after_bundle*.10,2) if discount_code.strip().upper()=="PAGENEST10" else 0
                if discount_code.strip() and discount_code.strip().upper()!="PAGENEST10":
                    st.warning("Discount code not recognised. Bundle savings remain applied.")
                total_discount=bd+code_discount
                cart_snapshot=[{"title":get_book(i)["title"],"quantity":q,"price":get_book(i)["price"]} for i,q in st.session_state.cart.items()]
                st.session_state.last_order={
                    "name":full_name.strip(),"email":email.strip(),"phone":phone.strip(),
                    "address":address.strip(),"city":city.strip(),"state":state.strip(),"pincode":pincode.strip(),
                    "gstin":gstin.strip().upper(),"subtotal":amount,"bundle_discount":bd,
                    "code_discount":code_discount,"discount":total_discount,
                    "delivery_option":delivery_option,"delivery_fee":delivery_fee,"delivery_eta":delivery_eta,
                    "payment_method":payment_method,"total":max(0,amount-total_discount+delivery_fee),
                    "order_date":date.today().strftime("%d %B %Y"),"invoice_id":"PN-"+date.today().strftime("%Y%m%d")+"-"+uuid.uuid4().hex[:6].upper(),
                    "cart_snapshot":cart_snapshot
                }
                st.success("Order summary calculated. Review the delivery, payment and final total below.")
        order=st.session_state.last_order
        if order:
            st.markdown(section_title("Review your order"),unsafe_allow_html=True)
            st.write(f"**Invoice:** {order['invoice_id']}  ·  **Date:** {order['order_date']}")
            st.write(f"**Billed to:** {order['name']} · {order['email']}")
            st.write(f"**Delivery:** {order['delivery_option']} · Estimated: {order['delivery_eta']}")
            st.write(f"**Payment method:** {order['payment_method']} · Demo selection only; no payment processed")
            lines=[]
            for item in order["cart_snapshot"]:
                lines.append({"Book":item["title"],"Qty":item["quantity"],"Rate":f"₹{item['price']:,.2f}","Amount":f"₹{item['price']*item['quantity']:,.2f}"})
            st.dataframe(lines,use_container_width=True,hide_index=True)
            a,b,c,d=st.columns(4)
            a.metric("Subtotal",f"₹{order['subtotal']:,.2f}")
            b.metric("Discount",f"−₹{order['discount']:,.2f}")
            c.metric("Delivery",f"₹{order['delivery_fee']:,.2f}")
            d.metric("Final Amount",f"₹{order['total']:,.2f}")
            try:
                pdf=create_invoice_pdf(order,order["cart_snapshot"])
                st.download_button("⬇ Download Professional PDF Invoice",data=pdf,file_name=f"{order['invoice_id']}.pdf",mime="application/pdf",use_container_width=True)
            except Exception as exc:
                st.error("Could not create PDF invoice. Check that reportlab is installed in requirements.txt.")
            if st.button("Place demo order",use_container_width=True):
                for i,q in st.session_state.cart.items():
                    st.session_state.stock[i]=max(0,st.session_state.stock.get(i,0)-q)
                st.session_state.completed_order=order
                st.session_state.cart={}
                st.session_state.bundles=[]
                st.session_state.last_order=None
                st.rerun()

# ----------------------- FIND BOOK -----------------------
elif st.session_state.page=="Find a Book":
    st.markdown(section_title("Find a book","Search online sellers or nearby stores"),unsafe_allow_html=True)
    find_title=st.text_input("Book title",value=st.session_state.find_book_title,key="find_title_input")
    find_author=st.text_input("Author (optional)",key="find_author_input")
    search_city=st.text_input("City or area",placeholder="e.g. Sonipat, Haryana",key="find_city_input")
    if st.button("Find Book & Stores",use_container_width=True):
        if not find_title.strip(): st.error("Enter the book title first.")
        else:
            term=" ".join(x for x in [find_title.strip(),find_author.strip()] if x)
            online=urllib.parse.quote(term+" buy book India")
            cover=urllib.parse.quote(term+" book cover")
            place=urllib.parse.quote("bookstores near "+search_city.strip() if search_city.strip() else "bookstores near me")
            st.markdown("### Where to look")
            st.markdown(f"[Search online sellers](https://www.google.com/search?q={online})")
            st.markdown(f"[Search book cover images](https://www.google.com/search?tbm=isch&q={cover})")
            st.markdown(f"[Find bookstores on Google Maps](https://www.google.com/maps/search/?api=1&query={place})")
            eta=date.today()+timedelta(days=7)
            st.markdown("### Estimated restock")
            st.write(f"Illustrative 7-day estimate: **{eta.strftime('%d %B %Y')}**.")
            st.caption("This is not live supplier inventory or a confirmed delivery date. Contact the seller to verify.")

# ----------------------- ABOUT -----------------------
elif st.session_state.page=="About PageNest":
    st.markdown(section_title("About PageNest","A demo bookstore for students and curious readers",eyebrow="Our story"),unsafe_allow_html=True)
    st.write("PageNest brings textbooks, competitive exam guides, business classics and popular reads into one place. Prices and stock are sample data, and no real payments are processed.")
    a1,a2,a3=st.columns(3)
    with a1:
        with st.container(border=True):
            st.markdown("### How ordering works")
            st.write("Add books to your cart, fill in your delivery details at checkout, review the total and place your demo order. You can download a PDF invoice for every order.")
    with a2:
        with st.container(border=True):
            st.markdown("### Delivery options")
            st.write("Standard delivery is free and takes 5–7 business days. Express costs ₹99 and takes 2–3 business days. Store pickup is free and ready in 1–2 business days. These are estimates for this demo.")
    with a3:
        with st.container(border=True):
            st.markdown("### Savings")
            st.write("Every bundle is 10% off its individual prices. Use the code PAGENEST10 at checkout for another 10% off after bundle savings.")
    with st.container(border=True):
        st.markdown("### Can't find a book?")
        st.write("Use Find a Book to search online sellers and nearby bookstores, or ask PageNest Help in the sidebar.")
        if st.button("Go to Find a Book"): go("Find a Book")

# ----------------------- TRUST STRIP & FOOTER -----------------------
st.markdown(trust_html(), unsafe_allow_html=True)
st.markdown(footer_html(), unsafe_allow_html=True)
