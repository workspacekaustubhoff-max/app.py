
import streamlit as st
import urllib.request
import urllib.parse
import json
import difflib
import csv
import io
from datetime import datetime

st.set_page_config(
    page_title="PageNest | Books & Learning",
    page_icon="📚",
    layout="wide"
)

# ==================================================
# PAGENEST THEME
# ==================================================

st.markdown("""
<style>
:root {
    --navy: #172A3A;
    --ivory: #F7F5EF;
    --teal: #47766C;
    --gold: #E8B85C;
    --white: #FFFFFF;
    --border: #E5E2D9;
    --muted: #697580;
}

.stApp {
    background-color: var(--ivory);
    color: var(--navy);
}

.block-container {
    max-width: 1500px;
    padding-top: 1.4rem;
    padding-bottom: 3rem;
}

[data-testid="stSidebar"] {
    background: #EEECE4;
    border-right: 1px solid var(--border);
}

h1, h2, h3 {
    color: var(--navy) !important;
    letter-spacing: -0.4px;
}

[data-testid="stCaptionContainer"] {
    color: var(--muted);
}

[data-testid="stVerticalBlockBorderWrapper"] {
    background: var(--white);
    border: 1px solid var(--border);
    border-radius: 12px;
}

[data-testid="stImage"] img {
    border-radius: 7px;
}

div.stButton > button,
div.stDownloadButton > button,
div.stLinkButton > a {
    background: var(--navy);
    color: white;
    border: 1px solid var(--navy);
    border-radius: 8px;
    min-height: 38px;
    font-weight: 600;
}

div.stButton > button:hover,
div.stDownloadButton > button:hover,
div.stLinkButton > a:hover {
    background: var(--teal);
    color: white;
    border-color: var(--teal);
}

div[data-baseweb="input"] input,
div[data-baseweb="select"] > div,
div[data-baseweb="textarea"] textarea {
    background: white;
    border-radius: 8px;
}

[data-testid="stMetric"] {
    background: white;
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 12px;
}

hr {
    border-color: var(--border);
}

a {
    color: var(--teal);
}

.price {
    color: var(--navy);
    font-weight: 750;
    font-size: 1.1rem;
}

.stock {
    color: var(--teal);
    font-size: .85rem;
}

.unavailable {
    color: #9A5B34;
    font-size: .85rem;
}
</style>
""", unsafe_allow_html=True)

# ==================================================
# BOOK CATALOGUE
# Fields: category, title, author, price, keywords,
# demo availability, illustrative restock days
# ==================================================

RAW_BOOKS = [
("Mathematics","NCERT Mathematics Class 11","NCERT",180,"school maths",True,2),
("Mathematics","NCERT Mathematics Class 12","NCERT",210,"school maths",True,2),
("Mathematics","Higher Engineering Mathematics","B. S. Grewal",850,"engineering maths",True,4),
("Mathematics","Business Mathematics","J. K. Sharma",550,"commerce maths",True,3),
("Mathematics","Calculus","James Stewart",1100,"calculus",False,5),
("Mathematics","Discrete Mathematics","Kenneth Rosen",950,"logic",True,3),
("Mathematics","RD Sharma Mathematics Class 11","R. D. Sharma",650,"school maths",True,2),
("Mathematics","RD Sharma Mathematics Class 12","R. D. Sharma",750,"school maths",True,2),
("Mathematics","Statistics for Business and Economics","Anderson et al.",900,"statistics",True,4),
("Mathematics","Advanced Engineering Mathematics","Erwin Kreyszig",950,"engineering maths",False,6),

("Science","Concepts of Physics Volume 1","H. C. Verma",450,"physics jee",True,2),
("Science","Concepts of Physics Volume 2","H. C. Verma",480,"physics jee",True,2),
("Science","NCERT Physics Class 11","NCERT",190,"school physics",True,2),
("Science","NCERT Physics Class 12","NCERT",220,"school physics",True,2),
("Science","NCERT Chemistry Class 11","NCERT",190,"chemistry",True,2),
("Science","NCERT Chemistry Class 12","NCERT",220,"chemistry",True,2),
("Science","Organic Chemistry","Morrison and Boyd",850,"chemistry",False,5),
("Science","Physical Chemistry","P. Bahadur",700,"chemistry",True,3),
("Science","Fundamentals of Biology","NCERT",250,"biology",True,2),
("Science","A Brief History of Time","Stephen Hawking",399,"space astronomy",True,3),

("Commerce","Accountancy Class 11","T. S. Grewal",650,"accounts",True,2),
("Commerce","Accountancy Class 12","T. S. Grewal",750,"accounts",True,2),
("Commerce","Business Studies Class 11","NCERT",180,"bst",True,2),
("Commerce","Business Studies Class 12","NCERT",220,"bst",True,2),
("Commerce","Introduction to Financial Accounting","Charles T. Horngren",950,"accounting",True,4),
("Commerce","Cost Accounting","M. N. Arora",850,"accounts",True,4),
("Commerce","Corporate Accounting","S. N. Maheshwari",900,"accounts",True,4),
("Commerce","Auditing and Assurance","Vikas Oswal",650,"audit",False,5),
("Commerce","Taxation","V. K. Singhania",950,"income tax",True,3),
("Commerce","Fundamentals of Accounting","S. N. Maheshwari",600,"accounts",True,3),

("Economics","Principles of Microeconomics","N. Gregory Mankiw",750,"micro economics",True,2),
("Economics","Principles of Macroeconomics","N. Gregory Mankiw",750,"macro economics",True,2),
("Economics","Intermediate Microeconomics","Hal R. Varian",1100,"micro theory",False,6),
("Economics","Macroeconomics","Olivier Blanchard",1050,"macro theory",True,4),
("Economics","Indian Economy","Ramesh Singh",850,"india economy upsc",True,2),
("Economics","Development Economics","Debraj Ray",950,"development",True,4),
("Economics","International Economics","Dominick Salvatore",900,"international trade",False,5),
("Economics","Public Finance","H. L. Bhatia",750,"government budget",True,3),
("Economics","Econometrics","Damodar Gujarati",1000,"statistics",True,4),
("Economics","Economics","Paul A. Samuelson",950,"economics principles",True,4),

("Business & Management","Principles of Management","Harold Koontz",650,"management",True,2),
("Business & Management","Management","Stephen P. Robbins",950,"organizational management",True,3),
("Business & Management","Marketing Management","Philip Kotler",1200,"marketing",True,4),
("Business & Management","Financial Management","I. M. Pandey",850,"finance",True,3),
("Business & Management","Human Resource Management","Gary Dessler",1000,"hr hrm",False,5),
("Business & Management","Operations Management","Heizer and Render",950,"operations",True,4),
("Business & Management","Organizational Behaviour","Stephen P. Robbins",900,"behavior",True,3),
("Business & Management","Business Research Methods","Donald R. Cooper",1000,"research",True,4),
("Business & Management","Entrepreneurship","Hisrich and Peters",850,"startup",True,3),
("Business & Management","Business Communication","Meenakshi Raman",550,"communication",True,2),

("CAT / MBA","Quantitative Aptitude for CAT","Arun Sharma",750,"cat maths",True,2),
("CAT / MBA","Data Interpretation for CAT","Arun Sharma",700,"cat di",True,2),
("CAT / MBA","Verbal Ability and Reading Comprehension","Arun Sharma",750,"cat varc english",True,3),
("CAT / MBA","Quantitative Aptitude for Competitive Examinations","R. S. Aggarwal",650,"aptitude",True,2),
("CAT / MBA","Verbal and Non-Verbal Reasoning","R. S. Aggarwal",600,"reasoning",True,2),
("CAT / MBA","Logical Reasoning and Data Interpretation","Nishit K. Sinha",700,"cat lrdi",False,5),
("CAT / MBA","CAT Previous Years Papers","Various Authors",450,"cat past papers",True,2),
("CAT / MBA","MBA Entrance Exam Practice Guide","Various Authors",500,"mba mock tests",True,3),

("JEE","Understanding Physics","D. C. Pandey",650,"jee physics",True,2),
("JEE","Problems in General Physics","I. E. Irodov",550,"advanced physics",False,5),
("JEE","Objective Mathematics","R. D. Sharma",850,"jee maths",True,3),
("JEE","IIT Mathematics","M. L. Khanna",750,"jee maths",True,3),
("JEE","Organic Chemistry","O. P. Tandon",700,"jee chemistry",True,2),
("JEE","Physical Chemistry","O. P. Tandon",700,"jee chemistry",True,2),
("JEE","Concise Inorganic Chemistry","J. D. Lee",850,"chemistry",False,6),
("JEE","JEE Main Previous Years Questions","Various Authors",500,"jee pyq",True,2),

("NEET","Objective Biology","Dinesh",750,"neet biology",True,2),
("NEET","Truemans Biology Volume 1","M. P. Tyagi et al.",850,"biology",True,3),
("NEET","Truemans Biology Volume 2","M. P. Tyagi et al.",850,"biology",True,3),
("NEET","Objective Physics for NEET","D. C. Pandey",700,"neet physics",True,2),
("NEET","Objective Chemistry for NEET","R. K. Gupta",700,"neet chemistry",True,2),
("NEET","NCERT Biology Class 11","NCERT",180,"biology",True,2),
("NEET","NCERT Biology Class 12","NCERT",220,"biology",True,2),
("NEET","NEET Previous Years Questions","Various Authors",500,"neet pyq",True,2),

("UPSC","Indian Polity","M. Laxmikanth",850,"constitution",True,2),
("UPSC","A Brief History of Modern India","Spectrum",650,"history",True,2),
("UPSC","Certificate Physical and Human Geography","Goh Cheng Leong",550,"geography",True,3),
("UPSC","Indias Struggle for Independence","Bipan Chandra",600,"history",True,3),
("UPSC","Indian Economy","Ramesh Singh",850,"economy",True,2),
("UPSC","Environment","Shankar IAS Academy",650,"ecology",True,2),
("UPSC","Oxford Student Atlas for India","Oxford University Press",350,"maps",True,2),
("UPSC","General Studies Manual","Various Authors",900,"gs prelims mains",False,5),

("Other Competitive Exams","Objective General English","S. P. Bakshi",550,"english grammar",True,2),
("Other Competitive Exams","Lucents General Knowledge","Lucent",350,"gk",True,2),
("Other Competitive Exams","Fast Track Objective Arithmetic","Rajesh Verma",550,"arithmetic",True,3),
("Other Competitive Exams","A Modern Approach to Verbal Reasoning","R. S. Aggarwal",450,"reasoning",True,2),
("Other Competitive Exams","General Knowledge 2026","Various Authors",400,"current affairs",True,2),
("Other Competitive Exams","Banking Awareness","Arihant Experts",350,"bank po",True,2),
("Other Competitive Exams","SSC CGL Practice Guide","Arihant Experts",500,"ssc",True,3),
("Other Competitive Exams","Railway Recruitment Exam Guide","Arihant Experts",450,"railway",True,3),
]

CATALOGUE = [
    {
        "id": i + 1, "category": r[0], "title": r[1],
        "author": r[2], "price": r[3], "keywords": r[4],
        "available": r[5], "restock_days": r[6]
    }
    for i, r in enumerate(RAW_BOOKS)
]

CATEGORIES = ["All categories"] + sorted({b["category"] for b in CATALOGUE})

# ==================================================
# SESSION STATE
# ==================================================

if "cart" not in st.session_state:
    st.session_state.cart = {}

if "requested_books" not in st.session_state:
    st.session_state.requested_books = set()

if "page" not in st.session_state:
    st.session_state.page = "Browse books"

if "store_book_id" not in st.session_state:
    st.session_state.store_book_id = None

# ==================================================
# HELPERS
# ==================================================

def money(value):
    return f"₹{value:,.2f}"

def normalise(text):
    return " ".join(
        "".join(c.lower() if c.isalnum() else " " for c in str(text)).split()
    )

def search_books(query, books):
    if not query.strip():
        return books

    q = normalise(query)
    results = []

    for book in books:
        searchable = normalise(
            book["title"] + " " + book["author"] + " "
            + book["category"] + " " + book["keywords"]
        )

        if q in searchable:
            results.append((1.0, book))
            continue

        words = searchable.split()
        scores = []

        for part in q.split():
            if part in words:
                scores.append(1.0)
            else:
                matches = difflib.get_close_matches(
                    part, words, n=1, cutoff=0.55
                )
                scores.append(
                    difflib.SequenceMatcher(
                        None, part, matches[0]
                    ).ratio() if matches else 0.0
                )

        score = sum(scores) / max(1, len(scores))
        if score >= 0.55:
            results.append((score, book))

    results.sort(key=lambda x: (-x[0], x[1]["title"]))
    return [book for _, book in results]

@st.cache_data(ttl=86400, show_spinner=False)
def get_cover(title, author):
    query = urllib.parse.urlencode({
        "title": title, "author": author, "limit": 1
    })
    url = "https://openlibrary.org/search.json?" + query

    request = urllib.request.Request(
        url, headers={"User-Agent": "PageNestBookstore/1.0"}
    )

    try:
        with urllib.request.urlopen(request, timeout=2.5) as response:
            data = json.loads(response.read().decode("utf-8"))

        docs = data.get("docs", [])
        if docs and docs[0].get("cover_i"):
            cover_id = docs[0]["cover_i"]
            return (
                "https://covers.openlibrary.org/b/id/"
                + str(cover_id) + "-M.jpg"
            )
    except Exception:
        pass

    return None

def maps_url(book, location):
    query = f"bookstore selling {book['title']} near {location}"
    return (
        "https://www.google.com/maps/search/?api=1&query="
        + urllib.parse.quote(query)
    )

def add_to_cart(book_id):
    book = next(b for b in CATALOGUE if b["id"] == book_id)
    if book["available"]:
        st.session_state.cart[book_id] = (
            st.session_state.cart.get(book_id, 0) + 1
        )
    else:
        st.session_state.requested_books.add(book_id)

# ==================================================
# LEFT SIDEBAR
# ==================================================

with st.sidebar:
    st.markdown("# 📚 PageNest")
    st.caption("BOOKS & LEARNING")
    st.divider()

    st.markdown("### Catalogue")
    search_query = st.text_input(
        "Search books",
        placeholder="Title, author or subject"
    )

    category = st.selectbox("Category", CATEGORIES)

    max_price = st.slider(
        "Maximum price", 100, 2000, 2000, 50
    )

    author_filter = st.text_input(
        "Author / publisher",
        placeholder="Optional"
    )

    st.divider()
    st.markdown("### Navigate")

    if st.button("📚 Browse books", use_container_width=True):
        st.session_state.page = "Browse books"

    if st.button("🛒 Cart & checkout", use_container_width=True):
        st.session_state.page = "Cart & checkout"

    if st.button("🔎 Find a book", use_container_width=True):
        st.session_state.page = "Book requests"

    if st.button("ℹ️ About PageNest", use_container_width=True):
        st.session_state.page = "About PageNest"

    st.divider()
    st.caption(f"{len(CATALOGUE)} catalogue entries")
    st.caption("Demo catalogue — check editions and stock before purchase.")

# ==================================================
# HEADER
# ==================================================

header, cart_header = st.columns([5, 1])

with header:
    st.markdown(
        "<h1 style='margin-bottom:0;color:#172A3A'>PageNest</h1>"
        "<p style='color:#47766C;margin-top:0'>"
        "Discover. Learn. Grow.</p>",
        unsafe_allow_html=True
    )

with cart_header:
    st.markdown("### 🛒 Cart")
    st.metric("Items", sum(st.session_state.cart.values()))

st.divider()

# ==================================================
# BROWSE PAGE
# ==================================================

if st.session_state.page == "Browse books":

    st.markdown("## Find your next book")
    st.caption(
        "A calm, focused bookstore for textbooks, higher education "
        "and competitive exam preparation."
    )

    books = [
        b for b in CATALOGUE
        if (category == "All categories" or b["category"] == category)
        and b["price"] <= max_price
        and (
            not author_filter.strip()
            or author_filter.lower() in b["author"].lower()
        )
    ]

    books = search_books(search_query, books)

    sort_by = st.selectbox(
        "Sort catalogue",
        [
            "Recommended",
            "Price: low to high",
            "Price: high to low",
            "Title A–Z"
        ]
    )

    if sort_by == "Price: low to high":
        books.sort(key=lambda b: b["price"])
    elif sort_by == "Price: high to low":
        books.sort(key=lambda b: b["price"], reverse=True)
    elif sort_by == "Title A–Z":
        books.sort(key=lambda b: b["title"].lower())

    st.caption(f"{len(books)} books found")

    if not books:
        st.info("No books found. Try changing your search or filters.")
    else:
        for start in range(0, len(books), 4):
            columns = st.columns(4)

            for col, book in zip(columns, books[start:start + 4]):
                with col:
                    with st.container(border=True):
                        cover = get_cover(book["title"], book["author"])

                        if cover:
                            st.image(cover, use_container_width=True)
                        else:
                            st.markdown(
                                "<div style='height:190px;background:#EDE9DF;"
                                "border-radius:8px;display:flex;"
                                "align-items:center;justify-content:center;"
                                "padding:14px;text-align:center;color:#172A3A'>"
                                "<div><div style='font-size:28px'>📖</div>"
                                f"<b>{book['title']}</b><br>"
                                f"<small>{book['category']}</small></div></div>",
                                unsafe_allow_html=True
                            )

                        st.markdown(f"**{book['title']}**")
                        st.caption(book["author"])
                        st.markdown(
                            f"<div class='price'>{money(book['price'])}</div>",
                            unsafe_allow_html=True
                        )

                        if book["available"]:
                            st.markdown(
                                "<span class='stock'>● In stock (demo)</span>",
                                unsafe_allow_html=True
                            )

                            if st.button(
                                "Add to cart",
                                key=f"add_{book['id']}",
                                use_container_width=True
                            ):
                                add_to_cart(book["id"])
                                st.toast("Added to cart")
                                st.rerun()
                        else:
                            st.markdown(
                                "<span class='unavailable'>Currently unavailable</span>",
                                unsafe_allow_html=True
                            )
                            st.caption(
                                f"Estimated restock: {book['restock_days']} days*"
                            )

                            if st.button(
                                "Find nearby store",
                                key=f"near_{book['id']}",
                                use_container_width=True
                            ):
                                st.session_state.store_book_id = book["id"]
                                st.session_state.page = "Book requests"
                                st.rerun()

                            if st.button(
                                "Request this book",
                                key=f"request_{book['id']}",
                                use_container_width=True
                            ):
                                st.session_state.requested_books.add(book["id"])
                                st.toast("Book request saved for this session")

    st.caption(
        "*Availability and restock times are illustrative demo values, "
        "not live supplier data."
    )

# ==================================================
# CART AND CHECKOUT
# ==================================================

elif st.session_state.page == "Cart & checkout":

    st.markdown("## 🛒 Your cart")
    st.caption("Review your books and prepare a demo receipt.")

    cart_items = []

    for book_id, qty in list(st.session_state.cart.items()):
        book = next(
            (b for b in CATALOGUE if b["id"] == book_id), None
        )
        if book:
            cart_items.append((book, qty))

    if not cart_items:
        st.info("Your cart is empty. Browse the catalogue to add books.")
    else:
        subtotal = 0

        for book, qty in cart_items:
            c1, c2, c3, c4 = st.columns([4, 1, 2, 1])

            with c1:
                st.write(f"**{book['title']}**")
                st.caption(book["author"])

            with c2:
                new_qty = st.number_input(
                    "Quantity",
                    min_value=1,
                    max_value=99,
                    value=qty,
                    key=f"qty_{book['id']}"
                )
                st.session_state.cart[book["id"]] = new_qty

            with c3:
                line_total = book["price"] * st.session_state.cart[book["id"]]
                st.write(money(line_total))
                subtotal += line_total

            with c4:
                if st.button("Remove", key=f"remove_{book['id']}"):
                    del st.session_state.cart[book["id"]]
                    st.rerun()

        st.divider()
        st.markdown("### Discount")

        discount_code = st.text_input(
            "Discount code",
            placeholder="Enter PAGE5 for 5% off"
        )

        discount_rate = (
            0.05 if discount_code.strip().upper() == "PAGE5" else 0.0
        )

        if discount_rate:
            st.success("PAGE5 discount applied: 5%")
        elif discount_code:
            st.warning("Invalid code. No discount applied.")

        discount = subtotal * discount_rate
        after_discount = subtotal - discount

        st.markdown("### Billing details")

        customer_name = st.text_input("Customer name")
        customer_email = st.text_input("Email (optional)")
        gstin = st.text_input(
            "GSTIN (optional)",
            max_chars=15,
            placeholder="15-character GSTIN"
        ).strip().upper()

        if gstin and (
            len(gstin) != 15 or not gstin.isalnum()
        ):
            st.warning(
                "Please check the GSTIN format. This check does not "
                "verify registration."
            )

        gst_rate = st.selectbox(
            "GST estimate (%)",
            [0, 5, 12, 18],
            help="Choose an assumed rate for this demo calculation."
        )

        gst_amount = after_discount * gst_rate / 100
        total = after_discount + gst_amount

        st.divider()

        left, right = st.columns([2, 1])

        with left:
            st.write(f"Subtotal: {money(subtotal)}")
            st.write(f"Discount: −{money(discount)}")
            st.write(f"Estimated GST: {money(gst_amount)}")

        with right:
            st.markdown(
                f"<div style='background:#172A3A;color:white;padding:18px;"
                f"border-radius:12px'><small>ORDER TOTAL</small>"
                f"<h2 style='color:white!important;margin:5px 0'>"
                f"{money(total)}</h2></div>",
                unsafe_allow_html=True
            )

        st.caption(
            "This is a demo checkout. GSTIN entry does not verify GST "
            "registration or make this a compliant tax invoice. "
            "No payment is collected."
        )

        if st.button("Prepare receipt", type="primary", use_container_width=True):
            output = io.StringIO()
            writer = csv.writer(output)

            writer.writerow(["PageNest Books & Learning — Demo Receipt"])
            writer.writerow(["Date", datetime.now().strftime("%Y-%m-%d %H:%M")])
            writer.writerow(["Customer", customer_name])
            writer.writerow(["Email", customer_email])
            writer.writerow(["GSTIN entered", gstin])
            writer.writerow([])
            writer.writerow(["Book", "Author", "Quantity", "Unit price", "Line total"])

            for book, _ in cart_items:
                quantity = st.session_state.cart[book["id"]]
                writer.writerow([
                    book["title"], book["author"], quantity,
                    book["price"], book["price"] * quantity
                ])

            writer.writerow([])
            writer.writerow(["Subtotal", subtotal])
            writer.writerow(["Discount", discount])
            writer.writerow(["Estimated GST", gst_amount])
            writer.writerow(["Total", total])

            st.download_button(
                "⬇ Download receipt (CSV)",
                output.getvalue(),
                file_name="pagenest_receipt.csv",
                mime="text/csv",
                use_container_width=True
            )

        if st.button("Empty cart"):
            st.session_state.cart = {}
            st.rerun()

# ==================================================
# FIND A BOOK / NEARBY STORE
# ==================================================

elif st.session_state.page == "Book requests":

    st.markdown("## Find a book")
    st.write(
        "Search for a nearby bookstore if a title is unavailable "
        "in the PageNest demo catalogue."
    )

    unavailable = [b for b in CATALOGUE if not b["available"]]

    options = {
        f"{b['title']} — {b['author']}": b
        for b in unavailable
    }

    default_index = 0
    if st.session_state.store_book_id:
        for i, book in enumerate(unavailable):
            if book["id"] == st.session_state.store_book_id:
                default_index = i
                break

    selected_label = st.selectbox(
        "Select an unavailable book",
        list(options.keys()),
        index=default_index
    )

    selected_book = options[selected_label]

    st.info(
        f"Demo restock estimate: {selected_book['restock_days']} days. "
        "This is not a confirmed delivery date."
    )

    location = st.text_input(
        "Your city, area or PIN code",
        placeholder="Enter a location to find nearby shops"
    )

    if location.strip():
        st.link_button(
            "Search nearby bookstores on Google Maps",
            maps_url(selected_book, location),
            use_container_width=True
        )
        st.caption(
            "Call the shop to confirm that the exact title and edition "
            "are in stock. Map results do not confirm availability."
        )

    if st.button("Request this book", type="primary"):
        st.session_state.requested_books.add(selected_book["id"])
        st.success("Request saved for this session.")

    st.divider()
    st.markdown("### Your requested books")

    requested = [
        b for b in CATALOGUE
        if b["id"] in st.session_state.requested_books
    ]

    if requested:
        for book in requested:
            st.write(
                f"📖 {book['title']} — estimated "
                f"{book['restock_days']} days"
            )
    else:
        st.caption("You have not requested any books yet.")

    st.caption(
        "Requests are kept only in the current session. "
        "Persistent requests and notifications require a database."
    )

# ==================================================
# ABOUT
# ==================================================

elif st.session_state.page == "About PageNest":

    st.markdown("## About PageNest")
    st.write(
        "PageNest Books & Learning is a clean, reading-focused bookstore "
        "for school and university textbooks, commerce, economics, "
        "business management and competitive examinations."
    )

    st.markdown("### Our features")
    st.write("- Search and browse the catalogue")
    st.write("- Filter by subject, author and price")
    st.write("- Add books to your cart")
    st.write("- Apply demo discount codes")
    st.write("- Estimate tax and download a receipt")
    st.write("- Search for nearby bookstores")

    st.caption(
        "Book prices, availability and restock estimates are illustrative. "
        "Verify editions and stock before purchasing."
    )

# ==================================================
# FOOTER
# ==================================================

st.divider()

footer1, footer2 = st.columns(2)

with footer1:
    st.markdown("**📚 PageNest**")
    st.caption("Discover. Learn. Grow.")

with footer2:
    st.caption(
        "Kindle-inspired reading aesthetic · Streamlit bookstore demo"
    )
