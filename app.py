import streamlit as st
import urllib.parse
import urllib.request
import json
import re
import io
import uuid
from difflib import SequenceMatcher
from datetime import date, timedelta

st.set_page_config(
    page_title="PageNest | Books & Learning",
    page_icon="📚",
    layout="wide"
)

# ----------------------- STYLE -----------------------
st.markdown("""
<style>
.stApp,[data-testid="stAppViewContainer"],[data-testid="stMain"],[data-testid="stHeader"]{
 background:#F5F7FB!important;color:#172033!important}
.block-container{max-width:1450px;padding-top:1.4rem;padding-bottom:3rem}
h1,h2,h3,h4,p,label,li,[data-testid="stMarkdownContainer"],
[data-testid="stWidgetLabel"],[data-testid="stCaptionContainer"]{color:#26344B!important}
[data-testid="stSidebar"]{background:#E8EEF7!important;border-right:1px solid #D6DFEC}
[data-testid="stSidebar"] *{color:#24334B!important}
.stTextInput input,.stTextArea textarea,.stNumberInput input{
 background:#fff!important;color:#172033!important;-webkit-text-fill-color:#172033!important;
 border:1px solid #C8D3E2!important;border-radius:8px!important;caret-color:#2458A6!important}
.stTextInput input::placeholder,.stTextArea textarea::placeholder{color:#758198!important;-webkit-text-fill-color:#758198!important;opacity:1!important}
[data-baseweb="select"]>div{background:#fff!important;color:#172033!important;border-color:#C8D3E2!important}
[data-baseweb="select"] input{color:#172033!important;-webkit-text-fill-color:#172033!important}
[data-baseweb="popover"],[data-baseweb="menu"],[role="listbox"],[role="option"]{background:#fff!important;color:#172033!important}
[data-testid="stForm"]{background:#fff!important;border:1px solid #DDE5EF!important;border-radius:14px!important;padding:22px!important}
[data-testid="stForm"] label,[data-testid="stForm"] [data-testid="stWidgetLabel"],
[data-testid="stForm"] [data-testid="stMarkdownContainer"]{color:#26344B!important}
.stButton>button,.stFormSubmitButton>button,.stDownloadButton>button{
 background:#2458A6!important;color:#fff!important;border:1px solid #2458A6!important;
 border-radius:9px!important;font-weight:600!important;min-height:2.45rem}
.stButton>button *, .stFormSubmitButton>button *, .stDownloadButton>button *{color:#fff!important}
.stButton>button:hover,.stFormSubmitButton>button:hover{background:#183F7C!important}
[data-testid="stVerticalBlockBorderWrapper"]{background:#fff!important;border-color:#DDE5EF!important;border-radius:14px!important}
[data-testid="stMetric"]{background:#fff!important;padding:15px;border:1px solid #DDE5EF;border-radius:12px}
[data-testid="stMetricLabel"],[data-testid="stMetricValue"]{color:#172033!important}
.hero{background:linear-gradient(120deg,#17345E,#3268A8);border-radius:18px;padding:30px;margin-bottom:24px}
.hero h1{color:#fff!important;font-size:clamp(30px,4vw,42px);margin-bottom:8px}
.hero p{color:#EDF4FF!important}
.pill{display:inline-block;background:#EAF1FF;color:#214E91!important;border-radius:20px;padding:5px 9px;font-size:11px;font-weight:700}
.book-title{color:#172033!important;font-size:16px;font-weight:700;min-height:42px}
.book-author{color:#64718A!important;font-size:13px;min-height:35px}
.book-price{color:#173F7A!important;font-size:21px;font-weight:700;margin:8px 0}
hr{border-color:#DDE5EF!important}
.footer{margin-top:35px;padding:22px;text-align:center;border-radius:14px;background:#17345E;color:#fff!important}
.footer *{color:#fff!important}
[data-testid="stChatMessage"]{background:#fff!important;border:1px solid #DDE5EF;border-radius:12px}
</style>
""", unsafe_allow_html=True)

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
]

BOOKS = [
    {"id": i + 1, "title": r[0], "author": r[1],
     "category": r[2], "price": r[3], "stock": r[4]}
    for i, r in enumerate(RAW_BOOKS)
]

PAGES = ["Catalogue", "Book Bundles", "Shopping Cart", "Checkout", "Find a Book"]

# ----------------------- SESSION / NAVIGATION -----------------------
if "page" not in st.session_state or st.session_state.page not in PAGES:
    st.session_state.page = "Catalogue"
if "cart" not in st.session_state:
    st.session_state.cart = {}
if "last_order" not in st.session_state:
    st.session_state.last_order = None
if "completed_order" not in st.session_state:
    st.session_state.completed_order = None
if "find_book_title" not in st.session_state:
    st.session_state.find_book_title = ""
if "bundle_discount" not in st.session_state:
    st.session_state.bundle_discount = 0.0
if "support_messages" not in st.session_state:
    st.session_state.support_messages = [{
        "role": "assistant",
        "content": (
            "Hi! I'm PageNest Help. Ask me about books, bundles, discounts, "
            "checkout, or unavailable titles. This demo doesn't process payments."
        )
    }]

def go(page):
    if page in PAGES:
        st.session_state.page = page
    st.rerun()

def get_book(book_id):
    return next(b for b in BOOKS if b["id"] == book_id)

def cart_count():
    return sum(st.session_state.cart.values())

def subtotal():
    return sum(get_book(i)["price"] * q for i, q in st.session_state.cart.items())

def norm(value):
    return " ".join(re.sub(r"[^a-zA-Z0-9 ]", " ", str(value).lower()).split())

def similarity(a, b):
    return SequenceMatcher(None, norm(a), norm(b)).ratio()

def add_to_cart(book_id, quantity=1):
    book = get_book(book_id)
    current = st.session_state.cart.get(book_id, 0)
    if current + quantity > book["stock"]:
        st.warning("Sorry, that is more than the available demo stock.")
    else:
        st.session_state.cart[book_id] = current + quantity
        st.toast("Added to your cart!")

# ----------------------- BOOK COVER LOOKUP -----------------------
@st.cache_data(ttl=86400, show_spinner=False)
def book_cover(title, author):
    def get_json(url):
        req = urllib.request.Request(
            url, headers={"User-Agent": "PageNestBookstore/1.0"}
        )
        with urllib.request.urlopen(req, timeout=4) as response:
            return json.loads(response.read().decode("utf-8"))

    try:
        url = "https://www.googleapis.com/books/v1/volumes?" + urllib.parse.urlencode({
            "q": f'intitle:"{title}" inauthor:"{author}"',
            "maxResults": 8,
            "printType": "books"
        })
        for item in get_json(url).get("items", []):
            info = item.get("volumeInfo", {})
            if similarity(title, info.get("title", "")) < 0.58:
                continue
            authors = info.get("authors", [])
            if authors and not any(similarity(author, n) > 0.45 for n in authors):
                continue
            links = info.get("imageLinks", {})
            image = (
                links.get("large") or links.get("medium")
                or links.get("thumbnail") or links.get("smallThumbnail")
            )
            if image:
                return image.replace("http://", "https://")
    except Exception:
        pass

    try:
        url = "https://openlibrary.org/search.json?" + urllib.parse.urlencode({
            "title": title,
            "author": author,
            "limit": 10,
            "fields": "title,author_name,cover_i"
        })
        for item in get_json(url).get("docs", []):
            if similarity(title, item.get("title", "")) < 0.58:
                continue
            authors = item.get("author_name", [])
            if authors and not any(similarity(author, n) > 0.45 for n in authors):
                continue
            cover_id = item.get("cover_i")
            if cover_id:
                return f"https://covers.openlibrary.org/b/id/{cover_id}-L.jpg?default=false"
    except Exception:
        pass

    return None

# ----------------------- BOOK CARD -----------------------
def render_book_card(book, prefix="book"):
    with st.container(border=True):
        cover = book_cover(book["title"], book["author"])
        if cover:
            st.image(cover, use_container_width=True)
        else:
            st.markdown(
                '<div style="height:180px;display:flex;align-items:center;'
                'justify-content:center;background:#EAF1FB;border-radius:10px;'
                'font-size:48px">📚</div>',
                unsafe_allow_html=True
            )
            q = urllib.parse.quote(f'{book["title"]} {book["author"]} book cover')
            st.markdown(
                f"[Search for the actual cover](https://www.google.com/search?tbm=isch&q={q})"
            )

        st.markdown(
            f'<div class="book-title">{book["title"]}</div>',
            unsafe_allow_html=True
        )
        st.markdown(
            f'<div class="book-author">{book["author"]}</div>',
            unsafe_allow_html=True
        )
        st.markdown(
            f'<span class="pill">{book["category"]}</span>',
            unsafe_allow_html=True
        )
        st.markdown(
            f'<div class="book-price">₹{book["price"]:,}</div>',
            unsafe_allow_html=True
        )

        if book["stock"] > 0:
            st.caption(f'{book["stock"]} copies in demo stock')
            if st.button(
                "＋ Add to Cart",
                key=f"{prefix}_add_{book['id']}",
                use_container_width=True
            ):
                add_to_cart(book["id"])
                st.rerun()
        else:
            st.warning("Currently unavailable")
            if st.button(
                "Find this book",
                key=f"{prefix}_find_{book['id']}",
                use_container_width=True
            ):
                st.session_state.find_book_title = book["title"]
                go("Find a Book")

# ----------------------- PDF INVOICE -----------------------
def create_invoice_pdf(order, cart_snapshot):
    """Create a clean A4 invoice with wrapped text and non-overlapping totals."""
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_CENTER, TA_RIGHT
    from reportlab.lib.units import mm
    from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether
    )

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=17 * mm,
        leftMargin=17 * mm,
        topMargin=15 * mm,
        bottomMargin=17 * mm
    )

    navy = colors.HexColor("#17345E")
    blue = colors.HexColor("#2458A6")
    pale = colors.HexColor("#EAF1FB")
    gray = colors.HexColor("#65728A")
    border = colors.HexColor("#D4DEEC")

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        name="Brand", parent=styles["Title"], fontName="Helvetica-Bold",
        fontSize=24, leading=28, textColor=navy, alignment=0, spaceAfter=4
    ))
    styles.add(ParagraphStyle(
        name="SmallMuted", parent=styles["Normal"], fontSize=8.5,
        leading=12, textColor=gray
    ))
    styles.add(ParagraphStyle(
        name="SectionHead", parent=styles["Heading2"], fontSize=11,
        leading=14, textColor=navy, spaceBefore=6, spaceAfter=5
    ))
    styles.add(ParagraphStyle(
        name="Right", parent=styles["Normal"], alignment=TA_RIGHT,
        fontSize=9, leading=12
    ))
    styles.add(ParagraphStyle(
        name="Tiny", parent=styles["Normal"], fontSize=8.5, leading=11
    ))
    styles.add(ParagraphStyle(
        name="CenterSmall", parent=styles["Normal"], alignment=TA_CENTER,
        fontSize=8, leading=11, textColor=gray
    ))

    story = []

    header_left = [
        Paragraph("PageNest", styles["Brand"]),
        Paragraph("BOOKS &amp; LEARNING", styles["SmallMuted"]),
        Paragraph("Digital order invoice", styles["SmallMuted"])
    ]
    header_right = [
        Paragraph(f"<b>INVOICE</b><br/>{order['invoice_id']}", styles["Right"]),
        Paragraph(f"<b>Date:</b> {order['order_date']}", styles["Right"]),
        Paragraph("<b>Status:</b> Demo order", styles["Right"])
    ]

    head = Table([[header_left, header_right]], colWidths=[105 * mm, 65 * mm])
    head.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), pale),
        ("BOX", (0, 0), (-1, -1), 0.6, border),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10)
    ]))
    story += [head, Spacer(1, 7 * mm)]

    customer = [
        Paragraph("<b>BILLED TO</b>", styles["SectionHead"]),
        Paragraph(order["name"].replace("&", "&amp;"), styles["Tiny"]),
        Paragraph(order["email"].replace("&", "&amp;"), styles["Tiny"]),
        Paragraph(order["phone"], styles["Tiny"]),
        Paragraph(order["address"].replace("&", "&amp;").replace("\n", "<br/>"), styles["Tiny"]),
        Paragraph(
            f"{order['city']}, {order['state']} {order['pincode']}",
            styles["Tiny"]
        ),
        Paragraph(
            f"Customer GSTIN: {order['gstin'] or 'Not provided'}",
            styles["SmallMuted"]
        )
    ]

    seller = [
        Paragraph("<b>SELLER DETAILS</b>", styles["SectionHead"]),
        Paragraph("PageNest Books &amp; Learning", styles["Tiny"]),
        Paragraph("Online demo bookstore", styles["Tiny"]),
        Paragraph("Seller GSTIN: Not configured", styles["SmallMuted"]),
        Paragraph("This is a demonstration invoice.", styles["SmallMuted"]),
        Paragraph("No payment has been collected.", styles["SmallMuted"])
    ]

    parties = Table([[customer, seller]], colWidths=[88 * mm, 82 * mm])
    parties.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("BOX", (0, 0), (-1, -1), 0.5, border),
        ("INNERGRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#E0E6EF")),
        ("LEFTPADDING", (0, 0), (-1, -1), 9),
        ("RIGHTPADDING", (0, 0), (-1, -1), 9),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8)
    ]))
    story += [
        parties, Spacer(1, 6 * mm),
        Paragraph("ORDER ITEMS", styles["SectionHead"])
    ]

    data = [["S.No.", "Book / Description", "Qty", "Unit Price", "Amount"]]
    for idx, item in enumerate(cart_snapshot, 1):
        title = item["title"].replace("&", "&amp;")
        data.append([
            str(idx),
            Paragraph(title, styles["Tiny"]),
            str(item["quantity"]),
            f"INR {item['price']:,.2f}",
            f"INR {item['price'] * item['quantity']:,.2f}"
        ])

    items = Table(
        data,
        colWidths=[13 * mm, 79 * mm, 13 * mm, 31 * mm, 34 * mm],
        repeatRows=1,
        hAlign="LEFT"
    )
    items.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), navy),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 8),
        ("FONTSIZE", (0, 1), (-1, -1), 8),
        ("ALIGN", (0, 0), (0, -1), "CENTER"),
        ("ALIGN", (2, 1), (-1, -1), "RIGHT"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0.4, border),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, pale]),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7)
    ]))
    story += [items, Spacer(1, 5 * mm)]

    delivery_payment = [
        Paragraph(
            f"<b>Delivery option:</b> {order['delivery_option']}",
            styles["Tiny"]
        ),
        Paragraph(
            f"<b>Estimated arrival:</b> {order['delivery_eta']}",
            styles["Tiny"]
        ),
        Paragraph(
            f"<b>Payment method:</b> {order['payment_method']} (demo selection only)",
            styles["Tiny"]
        )
    ]
    story += [KeepTogether(delivery_payment), Spacer(1, 4 * mm)]

    totals = [
        ["Subtotal", f"INR {order['subtotal']:,.2f}"],
        ["Bundle discount", f"- INR {order['bundle_discount']:,.2f}"],
        ["Discount code", f"- INR {order['code_discount']:,.2f}"],
        ["Delivery fee", f"INR {order['delivery_fee']:,.2f}"],
        ["Total discount", f"- INR {order['discount']:,.2f}"],
        ["AMOUNT DUE", f"INR {order['total']:,.2f}"]
    ]

    total_table = Table(totals, colWidths=[47 * mm, 38 * mm], hAlign="RIGHT")
    total_table.setStyle(TableStyle([
        ("ALIGN", (1, 0), (1, -1), "RIGHT"),
        ("FONTNAME", (0, 0), (-1, -2), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 8.5),
        ("LINEABOVE", (0, -1), (-1, -1), 1, blue),
        ("BACKGROUND", (0, -1), (-1, -1), navy),
        ("TEXTCOLOR", (0, -1), (-1, -1), colors.white),
        ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
        ("FONTSIZE", (0, -1), (-1, -1), 10),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6)
    ]))

    story += [total_table, Spacer(1, 7 * mm)]
    story.append(Paragraph(
        "Demo invoice only. No payment processed. Tax is not charged or "
        "represented in this sample bill. Configure verified seller and tax "
        "details before commercial use.",
        styles["CenterSmall"]
    ))
    story.append(Spacer(1, 3 * mm))
    story.append(Paragraph(
        "Thank you for shopping with PageNest.",
        ParagraphStyle(
            name="Thanks", parent=styles["Normal"], fontSize=12,
            leading=16, textColor=navy, alignment=TA_CENTER
        )
    ))

    def draw_footer(canvas, doc):
        canvas.saveState()
        canvas.setStrokeColor(border)
        canvas.line(17 * mm, 12 * mm, A4[0] - 17 * mm, 12 * mm)
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(gray)
        canvas.drawString(17 * mm, 7 * mm, "PageNest | Books & Learning")
        canvas.drawRightString(A4[0] - 17 * mm, 7 * mm, f"Page {doc.page}")
        canvas.restoreState()

    doc.build(story, onFirstPage=draw_footer, onLaterPages=draw_footer)
    return buffer.getvalue()

# ----------------------- SIDEBAR -----------------------
with st.sidebar:
    st.markdown("## 📚 PageNest")
    st.caption("Your personal bookstore")

    nav_key = f"navigation_radio_{st.session_state.page}"
    selected_nav = st.radio(
        "Navigate",
        PAGES,
        index=PAGES.index(st.session_state.page),
        key=nav_key
    )
    if selected_nav != st.session_state.page:
        st.session_state.page = selected_nav
        st.rerun()

    st.divider()
    st.markdown("### 🔎 Find your next book")

    search_query = st.text_input(
        "Search title or author",
        placeholder="e.g. Microeconomics",
        key="sidebar_search"
    )

    categories = ["All Subjects"] + sorted(set(b["category"] for b in BOOKS))
    selected_category = st.selectbox(
        "Subject", categories, key="sidebar_subject"
    )
    price_limit = st.slider(
        "Maximum price (₹)", 100, 1500, 1500, 100,
        key="sidebar_price"
    )
    availability = st.selectbox(
        "Availability",
        ["All Books", "In Stock", "Out of Stock"],
        key="sidebar_availability"
    )

    st.divider()
    st.markdown("### 🛒 Your Cart")
    st.metric("Items", cart_count())
    st.metric("Subtotal", f"₹{subtotal():,.2f}")

    if st.button("View Cart", use_container_width=True):
        go("Shopping Cart")

    st.divider()
    st.markdown("### 💬 PageNest Help")
    st.caption("Ask about books, bundles, discounts or checkout.")

    for message in st.session_state.support_messages[-4:]:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    prompt = st.chat_input("Ask PageNest Help...", key="help_chat_input")
    if prompt:
        st.session_state.support_messages.append({
            "role": "user", "content": prompt
        })
        q = prompt.lower()

        if any(w in q for w in ["discount", "coupon", "code", "offer"]):
            reply = (
                "Use PAGENEST10 at checkout for 10% off after bundle savings. "
                "Bundles show their own 10% savings."
            )
        elif any(w in q for w in ["cart", "checkout", "pay", "payment", "gst", "gstin"]):
            reply = (
                "Add books to your cart, open Shopping Cart and click Proceed "
                "to Checkout. Fill in the required delivery fields; GSTIN is "
                "optional. This demo does not process real payments."
            )
        elif any(w in q for w in ["unavailable", "out of stock", "restock", "store", "nearby"]):
            reply = (
                "Open Find a Book, enter the title and your area, then click "
                "Find Book & Stores. The seven-day estimate is illustrative, "
                "not live supplier data."
            )
        elif any(w in q for w in ["bundle", "class", "course", "semester"]):
            reply = (
                "Open Book Bundles for Commerce & BBA, BBA/MBA, CAT, UPSC, "
                "Python & Research, JEE and NEET."
            )
        else:
            reply = (
                "I can help with catalogue search, bundles, PAGENEST10, "
                "checkout, GSTIN and unavailable books."
            )

        st.session_state.support_messages.append({
            "role": "assistant", "content": reply
        })
        st.rerun()

# ----------------------- GLOBAL HERO -----------------------
st.markdown("""
<div class="hero">
    <h1>📚 PageNest</h1>
    <p>Books, ideas and possibilities — all in one place.</p>
    <p>Discover textbooks, business classics, competitive exam guides and research resources.</p>
</div>
""", unsafe_allow_html=True)

m1, m2, m3 = st.columns(3)
m1.metric("Books in Catalogue", len(BOOKS))
m2.metric("Subject Categories", len(set(b["category"] for b in BOOKS)))
m3.metric("Items in Your Cart", cart_count())

# ----------------------- FILTERED CATALOGUE -----------------------
filtered = BOOKS.copy()

if search_query.strip():
    q = norm(search_query)
    filtered = [
        b for b in filtered
        if q in norm(b["title"])
        or q in norm(b["author"])
        or q in norm(b["category"])
    ]

if selected_category != "All Subjects":
    filtered = [b for b in filtered if b["category"] == selected_category]

filtered = [b for b in filtered if b["price"] <= price_limit]

if availability == "In Stock":
    filtered = [b for b in filtered if b["stock"] > 0]
elif availability == "Out of Stock":
    filtered = [b for b in filtered if b["stock"] == 0]

# ----------------------- CATALOGUE PAGE -----------------------
if st.session_state.page == "Catalogue":
    st.markdown("## Explore the Catalogue")
    st.markdown("### ⭐ Featured Bestsellers")

    featured_titles = [
        ("Rich Dad Poor Dad", "Build your financial mindset", "Money & Personal Finance"),
        ("Ikigai", "Discover your reason for being", "Mindfulness & Wellbeing"),
        ("Atomic Habits", "Small habits. Remarkable results.", "Habits & Productivity"),
        ("The Psychology of Money", "Understand how people think about money", "Money & Behaviour")
    ]

    featured_cols = st.columns(4)

    for featured_col, (featured_title, tagline, banner_label) in zip(
        featured_cols, featured_titles
    ):
        featured_book = next(
            (b for b in BOOKS if b["title"] == featured_title), None
        )

        with featured_col:
            with st.container(border=True):
                if featured_book:
                    featured_cover = book_cover(
                        featured_book["title"], featured_book["author"]
                    )
                    if featured_cover:
                        st.image(featured_cover, use_container_width=True)
                    else:
                        st.markdown(
                            '<div style="height:150px;display:flex;'
                            'align-items:center;justify-content:center;'
                            'background:linear-gradient(135deg,#17345E,#3268A8);'
                            'border-radius:10px;color:white;font-size:36px">📚</div>',
                            unsafe_allow_html=True
                        )

                    st.markdown(f"**{featured_title}**")
                    st.caption(tagline)
                    st.markdown(
                        f"**₹{featured_book['price']:,}** · {banner_label}"
                    )

                    if st.button(
                        "Shop this bestseller",
                        key=f"feature_{featured_book['id']}",
                        use_container_width=True
                    ):
                        current = st.session_state.cart.get(featured_book["id"], 0)
                        if current + 1 <= featured_book["stock"]:
                            st.session_state.cart[featured_book["id"]] = current + 1
                            st.toast(f"{featured_title} added to your cart")
                            st.rerun()
                        else:
                            st.warning("Maximum demo stock reached.")

    st.markdown("### Browse All Books")
    st.caption(f"Showing {len(filtered)} books.")

    sort_by = st.selectbox(
        "Sort by",
        ["Recommended", "Price: Low to High", "Price: High to Low", "Title A–Z"],
        key="sort_catalogue"
    )

    if sort_by == "Price: Low to High":
        filtered.sort(key=lambda b: b["price"])
    elif sort_by == "Price: High to Low":
        filtered.sort(key=lambda b: b["price"], reverse=True)
    elif sort_by == "Title A–Z":
        filtered.sort(key=lambda b: b["title"].lower())

    if not filtered:
        st.info("No books match these filters. Try a different subject or price.")

    for start in range(0, len(filtered), 3):
        cols = st.columns(3)
        for col, book in zip(cols, filtered[start:start + 3]):
            with col:
                render_book_card(book, "catalogue")

# ----------------------- BOOK BUNDLES -----------------------
elif st.session_state.page == "Book Bundles":
    st.markdown("## 🎓 Curated Book Bundles")
    st.write(
        "Useful starter packs for different courses and exams. "
        "Each bundle gets 10% off its listed individual prices."
    )

    bundles = [
        (
            "Commerce & BBA Starter Bundle",
            "For introductory commerce and BBA courses",
            ["Principles of Economics", "Principles of Management",
             "Financial Accounting", "Business Mathematics"]
        ),
        (
            "BBA/MBA Core Bundle",
            "Management, marketing and MBA foundations",
            ["Management", "Marketing Management",
             "Organizational Behavior", "Business Statistics"]
        ),
        (
            "CAT Starter Bundle",
            "Quantitative, verbal and vocabulary preparation",
            ["How to Prepare for Quantitative Aptitude for CAT",
             "How to Prepare for Verbal Ability and Reading Comprehension for CAT",
             "Word Power Made Easy"]
        ),
        (
            "UPSC Foundation Bundle",
            "Polity, geography and modern history",
            ["Indian Polity", "Certificate Physical and Human Geography",
             "A Brief History of Modern India"]
        ),
        (
            "Python & Research Bundle",
            "Coding basics and research methods",
            ["Python Crash Course", "Think Python", "Research Methodology"]
        ),
        (
            "JEE Physics & Chemistry Bundle",
            "Foundational physics and chemistry",
            ["Concepts of Physics Volume 1", "Physical Chemistry", "IIT Mathematics"]
        ),
        (
            "NEET Biology & Chemistry Bundle",
            "Biology and chemistry preparation",
            ["Objective Biology", "Trueman's Elementary Biology",
             "Objective Chemistry for NEET"]
        )
    ]

    for start in range(0, len(bundles), 2):
        cols = st.columns(2)
        for col, bundle in zip(cols, bundles[start:start + 2]):
            title, desc, titles = bundle
            books = [
                next((b for b in BOOKS if b["title"] == t), None)
                for t in titles
            ]
            books = [b for b in books if b]
            total = sum(b["price"] for b in books)
            discounted = round(total * 0.9, 2)

            with col:
                with st.container(border=True):
                    st.markdown(f"### {title}")
                    st.write(desc)

                    for b in books:
                        st.write(f"• {b['title']} — ₹{b['price']:,}")

                    st.write(f"Individual total: ₹{total:,.2f}")
                    st.markdown(
                        f'<div class="book-price">Bundle price: ₹{discounted:,.2f}</div>',
                        unsafe_allow_html=True
                    )

                    if st.button(
                        "Add bundle to cart",
                        key="bundle_" + norm(title).replace(" ", "_"),
                        use_container_width=True
                    ):
                        if all(
                            st.session_state.cart.get(b["id"], 0) + 1 <= b["stock"]
                            for b in books
                        ):
                            for b in books:
                                st.session_state.cart[b["id"]] = (
                                    st.session_state.cart.get(b["id"], 0) + 1
                                )
                            st.session_state.bundle_discount += round(
                                total - discounted, 2
                            )
                            st.toast("Bundle added with 10% bundle savings.")
                            st.rerun()
                        else:
                            st.error(
                                "A title in this bundle does not have enough demo stock."
                            )

# ----------------------- SHOPPING CART -----------------------
elif st.session_state.page == "Shopping Cart":
    st.markdown("## 🛒 Your Shopping Cart")

    if not st.session_state.cart:
        st.info("Your cart is empty.")
        if st.button("Continue Shopping", use_container_width=True):
            go("Catalogue")
    else:
        for book_id in list(st.session_state.cart):
            book = get_book(book_id)
            qty = st.session_state.cart[book_id]

            with st.container(border=True):
                c1, c2, c3, c4 = st.columns([4, 1, 2, 1])
                c1.markdown(f"**{book['title']}**")
                c1.caption(f"{book['author']} · {book['category']}")
                c2.write(f"Qty: {qty}")
                c3.write(f"₹{book['price'] * qty:,.2f}")

                if c4.button("Remove", key=f"remove_{book_id}"):
                    del st.session_state.cart[book_id]
                    st.rerun()

                q1, q2, _ = st.columns([1, 1, 4])

                if q1.button("−", key=f"minus_{book_id}"):
                    if qty <= 1:
                        del st.session_state.cart[book_id]
                    else:
                        st.session_state.cart[book_id] = qty - 1
                    st.rerun()

                if q2.button("+", key=f"plus_{book_id}"):
                    if qty < book["stock"]:
                        st.session_state.cart[book_id] = qty + 1
                        st.rerun()
                    else:
                        st.warning("Maximum demo stock reached.")

        st.divider()
        amount = subtotal()
        bundle_discount = min(st.session_state.bundle_discount, amount)

        st.markdown(f"### Subtotal: ₹{amount:,.2f}")
        if bundle_discount:
            st.write(f"Bundle discount: −₹{bundle_discount:,.2f}")

        c1, c2 = st.columns(2)
        if c1.button("Continue Shopping", use_container_width=True):
            go("Catalogue")
        if c2.button("Proceed to Checkout", use_container_width=True):
            go("Checkout")

# ----------------------- CHECKOUT -----------------------
elif st.session_state.page == "Checkout":
    st.markdown("## Checkout & Digital Invoice")

    if not st.session_state.cart:
        completed = st.session_state.get("completed_order")

        if completed:
            st.success("Your demo order has been confirmed!")
            st.markdown(f"### Order number: {completed['invoice_id']}")
            st.write(
                f"**Customer:** {completed['name']} · {completed['email']}"
            )
            st.write(
                f"**Delivery:** {completed['delivery_option']} · "
                f"{completed['delivery_eta']}"
            )
            st.write(
                f"**Payment preference:** {completed['payment_method']} "
                "(demo only; no payment processed)"
            )
            st.metric("Order total", f"INR {completed['total']:,.2f}")

            try:
                completed_pdf = create_invoice_pdf(
                    completed, completed["cart_snapshot"]
                )
                st.download_button(
                    "⬇ Download Order Invoice PDF",
                    data=completed_pdf,
                    file_name=f"{completed['invoice_id']}.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
            except Exception:
                st.error(
                    "Could not create the PDF. Check that reportlab is listed "
                    "in requirements.txt."
                )

            if st.button("Start a New Order", use_container_width=True):
                st.session_state.completed_order = None
                go("Catalogue")
        else:
            st.info("Your cart is empty.")
            if st.button("Browse Books", use_container_width=True):
                go("Catalogue")

    else:
        amount = subtotal()
        bundle_discount = min(st.session_state.bundle_discount, amount)

        with st.form("checkout_form"):
            st.markdown("### Delivery Details")
            full_name = st.text_input("Full Name *")
            email = st.text_input("Email Address *")
            phone = st.text_input("Phone Number *")
            address = st.text_area("Delivery Address *")
            city = st.text_input("City *")
            state = st.text_input("State *")
            pincode = st.text_input("PIN Code *")

            st.markdown("### 🚚 Delivery Options")
            delivery_option = st.radio(
                "Choose how you want to receive your books",
                [
                    "Standard Delivery — Free (5–7 business days)",
                    "Express Delivery — ₹99 (2–3 business days)",
                    "Store Pickup — Free (ready in 1–2 business days)"
                ],
                index=0,
                help=(
                    "Delivery times are estimates for this demo and are not "
                    "live courier commitments."
                )
            )

            delivery_fee = (
                99.0 if delivery_option.startswith("Express Delivery") else 0.0
            )
            delivery_eta = (
                "2–3 business days"
                if delivery_option.startswith("Express Delivery")
                else "ready in 1–2 business days"
                if delivery_option.startswith("Store Pickup")
                else "5–7 business days"
            )

            st.markdown("### 💳 Payment Options")
            payment_method = st.radio(
                "Choose a payment method",
                ["UPI", "Credit / Debit Card", "Net Banking", "Cash on Delivery (COD)"],
                horizontal=True,
                help=(
                    "These are demo selections only. No payment will be "
                    "collected or processed."
                )
            )

            st.markdown("### Invoice Details")
            gstin = st.text_input(
                "Customer GSTIN (optional)",
                placeholder="Enter GSTIN if applicable"
            )
            discount_code = st.text_input(
                "Discount Code", placeholder="Try PAGENEST10"
            )
            st.caption(
                "PAGENEST10 gives 10% off after bundle savings. "
                "Taxes are not calculated in this demo invoice."
            )

            submitted = st.form_submit_button(
                "Calculate Total", use_container_width=True
            )

        if submitted:
            required = [
                full_name, email, phone, address, city, state, pincode
            ]

            if not all(x.strip() for x in required):
                st.error("Please complete all required delivery fields.")
            elif not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email.strip()):
                st.error("Please enter a valid email address.")
            elif not re.fullmatch(r"[0-9+\-\s()]{7,20}", phone.strip()):
                st.error("Please enter a valid phone number.")
            elif not re.fullmatch(r"[0-9A-Za-z -]{4,10}", pincode.strip()):
                st.error("Please enter a valid PIN code.")
            elif gstin.strip() and not re.fullmatch(
                r"[0-9A-Z]{15}", gstin.strip().upper()
            ):
                st.error("GSTIN should contain 15 alphanumeric characters.")
            else:
                after_bundle = max(0, amount - bundle_discount)
                code_discount = (
                    round(after_bundle * 0.10, 2)
                    if discount_code.strip().upper() == "PAGENEST10"
                    else 0
                )

                if discount_code.strip() and discount_code.strip().upper() != "PAGENEST10":
                    st.warning(
                        "Discount code not recognised. Bundle savings remain applied."
                    )

                total_discount = bundle_discount + code_discount
                cart_snapshot = [
                    {
                        "title": get_book(i)["title"],
                        "quantity": q,
                        "price": get_book(i)["price"]
                    }
                    for i, q in st.session_state.cart.items()
                ]

                st.session_state.last_order = {
                    "name": full_name.strip(),
                    "email": email.strip(),
                    "phone": phone.strip(),
                    "address": address.strip(),
                    "city": city.strip(),
                    "state": state.strip(),
                    "pincode": pincode.strip(),
                    "gstin": gstin.strip().upper(),
                    "subtotal": amount,
                    "bundle_discount": bundle_discount,
                    "code_discount": code_discount,
                    "discount": total_discount,
                    "delivery_option": delivery_option,
                    "delivery_fee": delivery_fee,
                    "delivery_eta": delivery_eta,
                    "payment_method": payment_method,
                    "total": max(0, amount - total_discount + delivery_fee),
                    "order_date": date.today().strftime("%d %B %Y"),
                    "invoice_id": (
                        "PN-" + date.today().strftime("%Y%m%d") + "-"
                        + uuid.uuid4().hex[:6].upper()
                    ),
                    "cart_snapshot": cart_snapshot
                }

                st.success(
                    "Order summary calculated. Review the delivery, payment "
                    "and final total below."
                )

        order = st.session_state.last_order

        if order:
            st.markdown("### Digital Bill Preview")
            st.write(
                f"**Invoice:** {order['invoice_id']} · "
                f"**Date:** {order['order_date']}"
            )
            st.write(
                f"**Billed to:** {order['name']} · {order['email']}"
            )
            st.write(
                f"**Delivery:** {order['delivery_option']} · "
                f"Estimated: {order['delivery_eta']}"
            )
            st.write(
                f"**Payment method:** {order['payment_method']} · "
                "Demo selection only; no payment processed"
            )

            lines = [
                {
                    "Book": item["title"],
                    "Qty": item["quantity"],
                    "Rate": f"₹{item['price']:,.2f}",
                    "Amount": f"₹{item['price'] * item['quantity']:,.2f}"
                }
                for item in order["cart_snapshot"]
            ]
            st.dataframe(lines, use_container_width=True, hide_index=True)

            a, b, c, d = st.columns(4)
            a.metric("Subtotal", f"₹{order['subtotal']:,.2f}")
            b.metric("Discount", f"−₹{order['discount']:,.2f}")
            c.metric("Delivery", f"₹{order['delivery_fee']:,.2f}")
            d.metric("Final Amount", f"₹{order['total']:,.2f}")

            try:
                pdf = create_invoice_pdf(order, order["cart_snapshot"])
                st.download_button(
                    "⬇ Download Professional PDF Invoice",
                    data=pdf,
                    file_name=f"{order['invoice_id']}.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
            except Exception:
                st.error(
                    "Could not create PDF invoice. Check that reportlab is "
                    "installed in requirements.txt."
                )

            if st.button("Confirm Demo Order", use_container_width=True):
                st.session_state.completed_order = order
                st.session_state.cart = {}
                st.session_state.bundle_discount = 0.0
                st.session_state.last_order = None
                st.success(
                    f"Demo order confirmed. Delivery: {order['delivery_option']}. "
                    f"Payment preference: {order['payment_method']}. "
                    "No payment was processed."
                )
                st.rerun()

# ----------------------- FIND A BOOK -----------------------
elif st.session_state.page == "Find a Book":
    st.markdown("## 🔎 Find a Book")
    st.write("Search online sellers or locate nearby bookstores.")

    find_title = st.text_input(
        "Book title",
        value=st.session_state.find_book_title,
        key="find_title_input"
    )
    find_author = st.text_input("Author (optional)", key="find_author_input")
    search_city = st.text_input(
        "City or area",
        placeholder="e.g. Sonipat, Haryana",
        key="find_city_input"
    )

    if st.button("Find Book & Stores", use_container_width=True):
        if not find_title.strip():
            st.error("Enter the book title first.")
        else:
            term = " ".join(
                x for x in [find_title.strip(), find_author.strip()] if x
            )
            online = urllib.parse.quote(term + " buy book India")
            cover = urllib.parse.quote(term + " book cover")
            place = urllib.parse.quote(
                "bookstores near " + search_city.strip()
                if search_city.strip()
                else "bookstores near me"
            )

            st.markdown("### Where to look")
            st.markdown(
                f"[Search online sellers](https://www.google.com/search?q={online})"
            )
            st.markdown(
                f"[Search book cover images](https://www.google.com/search?tbm=isch&q={cover})"
            )
            st.markdown(
                f"[Find bookstores on Google Maps](https://www.google.com/maps/search/?api=1&query={place})"
            )

            eta = date.today() + timedelta(days=7)
            st.markdown("### Estimated restock")
            st.write(
                f"Illustrative 7-day estimate: **{eta.strftime('%d %B %Y')}**."
            )
            st.caption(
                "This is not live supplier inventory or a confirmed delivery date. "
                "Contact the seller to verify."
            )

# ----------------------- FOOTER -----------------------
st.markdown("""
<div class="footer">
    <strong>PageNest | Books &amp; Learning</strong><br>
    Find your next idea. Discover your next chapter.<br>
    <span style="font-size:12px;">
        Demo bookstore · Sample prices and inventory · No real payments processed
    </span>
</div>
""", unsafe_allow_html=True)
