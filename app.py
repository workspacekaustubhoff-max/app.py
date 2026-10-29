
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

# =====================================================
# 1. CLEAN, HIGH-CONTRAST DESIGN
# =====================================================

st.markdown("""
<style>
:root {
    --bg: #F4F6FA;
    --surface: #FFFFFF;
    --sidebar: #EAF0F8;
    --text: #202938;
    --muted: #566477;
    --blue: #2457C5;
    --blue-hover: #19449E;
    --green: #18794E;
    --border: #DCE3ED;
}

.stApp {
    background: var(--bg);
    color: var(--text);
}

.block-container {
    max-width: 1500px;
    padding-top: 1.5rem;
    padding-bottom: 3rem;
}

[data-testid="stSidebar"] {
    background: var(--sidebar);
    border-right: 1px solid var(--border);
}

[data-testid="stSidebar"] * {
    color: var(--text);
}

h1, h2, h3, h4, p, label,
[data-testid="stMarkdownContainer"] {
    color: var(--text);
}

[data-testid="stCaptionContainer"] p {
    color: var(--muted) !important;
}

/* Clear, readable input labels */
[data-testid="stWidgetLabel"] p,
[data-testid="stWidgetLabel"] label,
.stTextInput label,
.stSelectbox label,
.stSlider label,
.stNumberInput label,
.stRadio label,
.stCheckbox label {
    color: #202938 !important;
    font-weight: 600 !important;
}

/* White input boxes with dark text */
div[data-baseweb="input"] input,
div[data-baseweb="textarea"] textarea {
    background: #FFFFFF !important;
    color: #202938 !important;
    -webkit-text-fill-color: #202938 !important;
    border: 1px solid #BCC8D8 !important;
    border-radius: 8px !important;
}

div[data-baseweb="select"] > div {
    background: #FFFFFF !important;
    color: #202938 !important;
    border: 1px solid #BCC8D8 !important;
    border-radius: 8px !important;
}

div[data-baseweb="select"] * {
    color: #202938 !important;
}

/* Buttons */
div.stButton > button,
div.stDownloadButton > button,
div.stLinkButton > a {
    background: var(--blue) !important;
    color: #FFFFFF !important;
    border: 1px solid var(--blue) !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    min-height: 40px;
}

div.stButton > button:hover,
div.stDownloadButton > button:hover,
div.stLinkButton > a:hover {
    background: var(--blue-hover) !important;
    border-color: var(--blue-hover) !important;
    color: #FFFFFF !important;
}

/* Cards */
[data-testid="stVerticalBlockBorderWrapper"] {
    background: #FFFFFF;
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 5px;
}

[data-testid="stImage"] img {
    border-radius: 8px;
}

/* Metrics */
[data-testid="stMetric"] {
    background: #FFFFFF;
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 14px;
}

[data-testid="stMetricLabel"] {
    color: #566477 !important;
}

[data-testid="stMetricValue"] {
    color: #202938 !important;
}

/* Tabs */
button[data-baseweb="tab"] {
    color: #374151 !important;
}

button[data-baseweb="tab"][aria-selected="true"] {
    color: var(--blue) !important;
    border-bottom-color: var(--blue) !important;
}

/* Price and stock */
.book-price {
    color: #202938;
    font-size: 1.15rem;
    font-weight: 750;
}

.book-stock {
    color: #18794E;
    font-size: 0.88rem;
    font-weight: 600;
}

.book-unavailable {
    color: #9A4D13;
    font-size: 0.88rem;
    font-weight: 600;
}

/* Order total */
.order-total {
    background: #FFFFFF;
    border: 2px solid #2457C5;
    border-radius: 12px;
    padding: 20px;
    color: #202938;
}

.order-total .amount {
    color: #19449E;
    font-size: 2rem;
    font-weight: 800;
}

hr {
    border-color: #DCE3ED;
}

a {
    color: #2457C5 !important;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# 2. CATALOGUE
# =====================================================

RAW_BOOKS = [
# Mathematics
("Mathematics","NCERT Mathematics Class 11","NCERT",180,"school maths",1,2),
("Mathematics","NCERT Mathematics Class 12","NCERT",210,"school maths",1,2),
("Mathematics","Higher Engineering Mathematics","B. S. Grewal",850,"engineering maths",1,4),
("Mathematics","Business Mathematics","J. K. Sharma",550,"commerce maths",1,3),
("Mathematics","Calculus","James Stewart",1100,"calculus",0,5),
("Mathematics","Discrete Mathematics","Kenneth Rosen",950,"logic",1,3),
("Mathematics","RD Sharma Mathematics Class 11","R. D. Sharma",650,"school maths",1,2),
("Mathematics","RD Sharma Mathematics Class 12","R. D. Sharma",750,"school maths",1,2),
("Mathematics","Statistics for Business and Economics","Anderson et al.",900,"statistics",1,4),
("Mathematics","Advanced Engineering Mathematics","Erwin Kreyszig",950,"engineering maths",0,6),

# Science
("Science","Concepts of Physics Volume 1","H. C. Verma",450,"physics jee",1,2),
("Science","Concepts of Physics Volume 2","H. C. Verma",480,"physics jee",1,2),
("Science","NCERT Physics Class 11","NCERT",190,"school physics",1,2),
("Science","NCERT Physics Class 12","NCERT",220,"school physics",1,2),
("Science","NCERT Chemistry Class 11","NCERT",190,"chemistry",1,2),
("Science","NCERT Chemistry Class 12","NCERT",220,"chemistry",1,2),
("Science","Organic Chemistry","Morrison and Boyd",850,"chemistry",0,5),
("Science","Physical Chemistry","P. Bahadur",700,"chemistry",1,3),
("Science","Fundamentals of Biology","NCERT",250,"biology",1,2),
("Science","A Brief History of Time","Stephen Hawking",399,"space astronomy",1,3),

# Commerce
("Commerce","Accountancy Class 11","T. S. Grewal",650,"accounts",1,2),
("Commerce","Accountancy Class 12","T. S. Grewal",750,"accounts",1,2),
("Commerce","Business Studies Class 11","NCERT",180,"bst",1,2),
("Commerce","Business Studies Class 12","NCERT",220,"bst",1,2),
("Commerce","Introduction to Financial Accounting","Charles T. Horngren",950,"accounting",1,4),
("Commerce","Cost Accounting","M. N. Arora",850,"accounts",1,4),
("Commerce","Corporate Accounting","S. N. Maheshwari",900,"accounts",1,4),
("Commerce","Auditing and Assurance","Vikas Oswal",650,"audit",0,5),
("Commerce","Taxation","V. K. Singhania",950,"income tax",1,3),
("Commerce","Fundamentals of Accounting","S. N. Maheshwari",600,"accounts",1,3),

# Economics
("Economics","Principles of Microeconomics","N. Gregory Mankiw",750,"micro economics",1,2),
("Economics","Principles of Macroeconomics","N. Gregory Mankiw",750,"macro economics",1,2),
("Economics","Intermediate Microeconomics","Hal R. Varian",1100,"micro theory",0,6),
("Economics","Macroeconomics","Olivier Blanchard",1050,"macro theory",1,4),
("Economics","Indian Economy","Ramesh Singh",850,"india economy upsc",1,2),
("Economics","Development Economics","Debraj Ray",950,"development",1,4),
("Economics","International Economics","Dominick Salvatore",900,"international trade",0,5),
("Economics","Public Finance","H. L. Bhatia",750,"government budget",1,3),
("Economics","Econometrics","Damodar Gujarati",1000,"statistics",1,4),
("Economics","Economics","Paul A. Samuelson",950,"economics principles",1,4),

# Business and Management
("Business & Management","Principles of Management","Harold Koontz",650,"management",1,2),
("Business & Management","Management","Stephen P. Robbins",950,"organizational management",1,3),
("Business & Management","Marketing Management","Philip Kotler",1200,"marketing",1,4),
("Business & Management","Financial Management","I. M. Pandey",850,"finance",1,3),
("Business & Management","Human Resource Management","Gary Dessler",1000,"hr hrm",0,5),
("Business & Management","Operations Management","Heizer and Render",950,"operations",1,4),
("Business & Management","Organizational Behaviour","Stephen P. Robbins",900,"behavior",1,3),
("Business & Management","Business Research Methods","Donald R. Cooper",1000,"research",1,4),
("Business & Management","Entrepreneurship","Hisrich and Peters",850,"startup",1,3),
("Business & Management","Business Communication","Meenakshi Raman",550,"communication",1,2),

# CAT / MBA
("CAT / MBA","Quantitative Aptitude for CAT","Arun Sharma",750,"cat maths",1,2),
("CAT / MBA","Data Interpretation for CAT","Arun Sharma",700,"cat di",1,2),
("CAT / MBA","Verbal Ability and Reading Comprehension","Arun Sharma",750,"cat varc english",1,3),
("CAT / MBA","Quantitative Aptitude for Competitive Examinations","R. S. Aggarwal",650,"aptitude",1,2),
("CAT / MBA","Verbal and Non-Verbal Reasoning","R. S. Aggarwal",600,"reasoning",1,2),
("CAT / MBA","Logical Reasoning and Data Interpretation","Nishit K. Sinha",700,"cat lrdi",0,5),
("CAT / MBA","CAT Previous Years Papers","Various Authors",450,"cat past papers",1,2),
("CAT / MBA","MBA Entrance Exam Practice Guide","Various Authors",500,"mba mock tests",1,3),

# JEE
("JEE","Understanding Physics","D. C. Pandey",650,"jee physics",1,2),
("JEE","Problems in General Physics","I. E. Irodov",550,"advanced physics",0,5),
("JEE","Objective Mathematics","R. D. Sharma",850,"jee maths",1,3),
("JEE","IIT Mathematics","M. L. Khanna",750,"jee maths",1,3),
("JEE","Organic Chemistry","O. P. Tandon",700,"jee chemistry",1,2),
("JEE","Physical Chemistry","O. P. Tandon",700,"jee chemistry",1,2),
("JEE","Concise Inorganic Chemistry","J. D. Lee",850,"chemistry",0,6),
("JEE","JEE Main Previous Years Questions","Various Authors",500,"jee pyq",1,2),

# NEET
("NEET","Objective Biology","Dinesh",750,"neet biology",1,2),
("NEET","Truemans Biology Volume 1","M. P. Tyagi et al.",850,"biology",1,3),
("NEET","Truemans Biology Volume 2","M. P. Tyagi et al.",850,"biology",1,3),
("NEET","Objective Physics for NEET","D. C. Pandey",700,"neet physics",1,2),
("NEET","Objective Chemistry for NEET","R. K. Gupta",700,"neet chemistry",1,2),
("NEET","NCERT Biology Class 11","NCERT",180,"biology",1,2),
("NEET","NCERT Biology Class 12","NCERT",220,"biology",1,2),
("NEET","NEET Previous Years Questions","Various Authors",500,"neet pyq",1,2),

# UPSC
("UPSC","Indian Polity","M. Laxmikanth",850,"constitution",1,2),
("UPSC","A Brief History of Modern India","Spectrum",650,"history",1,2),
("UPSC","Certificate Physical and Human Geography","Goh Cheng Leong",550,"geography",1,3),
("UPSC","India's Struggle for Independence","Bipan Chandra",600,"history",1,3),
("UPSC","Indian Economy","Ramesh Singh",850,"economy",1,2),
("UPSC","Environment","Shankar IAS Academy",650,"ecology",1,2),
("UPSC","Oxford Student Atlas for India","Oxford University Press",350,"maps",1,2),
("UPSC","General Studies Manual","Various Authors",900,"gs prelims mains",0,5),

# Other competitive exams
("Other Competitive Exams","Objective General English","S. P. Bakshi",550,"english grammar",1,2),
("Other Competitive Exams","Lucents General Knowledge","Lucent",350,"gk",1,2),
("Other Competitive Exams","Fast Track Objective Arithmetic","Rajesh Verma",550,"arithmetic",1,3),
("Other Competitive Exams","A Modern Approach to Verbal Reasoning","R. S. Aggarwal",450,"reasoning",1,2),
("Other Competitive Exams","General Knowledge 2026","Various Authors",400,"current affairs",1,2),
("Other Competitive Exams","Banking Awareness","Arihant Experts",350,"bank po",1,2),
("Other Competitive Exams","SSC CGL Practice Guide","Arihant Experts",500,"ssc",1,3),
("Other Competitive Exams","Railway Recruitment Exam Guide","Arihant Experts",450,"railway",1,3),
]

BOOKS = [
    {
        "id": i + 1,
        "category": row[0],
        "title": row[1],
        "author": row[2],
        "price": row[3],
        "keywords": row[4],
        "available": bool(row[5]),
        "days": row[6],
    }
    for i, row in enumerate(RAW_BOOKS)
]

CATEGORIES = ["All categories"] + sorted(set(b["category"] for b in BOOKS))

# =====================================================
# 3. SESSION STATE
# =====================================================

if "cart" not in st.session_state:
    st.session_state.cart = {}

if "requests" not in st.session_state:
    st.session_state.requests = set()

if "page" not in st.session_state:
    st.session_state.page = "Browse books"

if "selected_unavailable" not in st.session_state:
    st.session_state.selected_unavailable = None

# =====================================================
# 4. HELPER FUNCTIONS
# =====================================================

def rupees(amount):
    return "₹{:,.2f}".format(amount)

def normalise(text):
    return " ".join(
        "".join(
            char.lower() if char.isalnum() else " "
            for char in str(text)
        ).split()
    )

def find_books(query, books):
    if not query.strip():
        return books

    query = normalise(query)
    found = []

    for book in books:
        searchable = normalise(
            book["title"] + " " + book["author"] + " "
            + book["category"] + " " + book["keywords"]
        )

        if query in searchable:
            found.append((1.0, book))
            continue

        searchable_words = searchable.split()
        query_words = query.split()
        word_scores = []

        for query_word in query_words:
            if query_word in searchable_words:
                word_scores.append(1.0)
            else:
                matches = difflib.get_close_matches(
                    query_word, searchable_words, n=1, cutoff=0.55
                )
                if matches:
                    word_scores.append(
                        difflib.SequenceMatcher(
                            None, query_word, matches[0]
                        ).ratio()
                    )
                else:
                    word_scores.append(0.0)

        score = sum(word_scores) / max(1, len(word_scores))

        if score >= 0.55:
            found.append((score, book))

    found.sort(key=lambda item: (-item[0], item[1]["title"]))
    return [item[1] for item in found]

@st.cache_data(ttl=86400, show_spinner=False)
def book_cover(title, author):
    params = urllib.parse.urlencode({
        "title": title,
        "author": author,
        "limit": 1
    })

    url = "https://openlibrary.org/search.json?" + params
    request = urllib.request.Request(
        url, headers={"User-Agent": "PageNestBookstore/1.0"}
    )

    try:
        with urllib.request.urlopen(request, timeout=2.5) as response:
            data = json.loads(response.read().decode("utf-8"))

        docs = data.get("docs", [])
        if docs and docs[0].get("cover_i"):
            return (
                "https://covers.openlibrary.org/b/id/"
                + str(docs[0]["cover_i"]) + "-M.jpg"
            )
    except Exception:
        pass

    return None

def nearby_store_url(book, location):
    query = f"bookstore selling {book['title']} near {location}"
    return (
        "https://www.google.com/maps/search/?api=1&query="
        + urllib.parse.quote(query)
    )

def add_to_cart(book):
    if book["available"]:
        book_id = book["id"]
        st.session_state.cart[book_id] = (
            st.session_state.cart.get(book_id, 0) + 1
        )

# =====================================================
# 5. SIDEBAR
# =====================================================

with st.sidebar:
    st.markdown("# 📚 PageNest")
    st.caption("BOOKS & LEARNING")
    st.divider()

    st.markdown("### Catalogue filters")

    query = st.text_input(
        "Search title, author or subject",
        placeholder="Try microeconomics or Mankiw"
    )

    category = st.selectbox("Category", CATEGORIES)

    max_price = st.slider(
        "Maximum price (₹)", 100, 2000, 2000, step=50
    )

    author_filter = st.text_input(
        "Publisher / author",
        placeholder="Optional filter"
    )

    st.divider()
    st.markdown("### Navigate")

    if st.button("📚 Browse books", use_container_width=True):
        st.session_state.page = "Browse books"

    if st.button("🛒 Cart & checkout", use_container_width=True):
        st.session_state.page = "Cart & checkout"

    if st.button("🔎 Find a book", use_container_width=True):
        st.session_state.page = "Find a book"

    if st.button("ℹ️ About PageNest", use_container_width=True):
        st.session_state.page = "About PageNest"

    st.divider()
    st.caption(f"{len(BOOKS)} catalogue entries")
    st.caption("Demo catalogue. Check editions and stock before ordering.")

# =====================================================
# 6. TOP HEADER
# =====================================================

header_col, cart_col = st.columns([5, 1])

with header_col:
    st.markdown(
        "<h1 style='margin-bottom:0;color:#202938'>📚 PageNest</h1>"
        "<p style='color:#566477;margin-top:3px'>"
        "Discover. Learn. Grow.</p>",
        unsafe_allow_html=True
    )

with cart_col:
    st.markdown("### 🛒 Cart")
    st.metric("Items", sum(st.session_state.cart.values()))

st.divider()

# =====================================================
# 7. BROWSE BOOKS
# =====================================================

if st.session_state.page == "Browse books":

    st.markdown("## Find your next book")
    st.caption(
        "Textbooks, university reading and competitive exam preparation."
    )

    filtered = [
        b for b in BOOKS
        if (category == "All categories" or b["category"] == category)
        and b["price"] <= max_price
        and (
            not author_filter.strip()
            or author_filter.lower() in b["author"].lower()
        )
    ]

    filtered = find_books(query, filtered)

    sort_option = st.selectbox(
        "Sort books",
        [
            "Recommended",
            "Price: low to high",
            "Price: high to low",
            "Title A–Z"
        ]
    )

    if sort_option == "Price: low to high":
        filtered.sort(key=lambda b: b["price"])
    elif sort_option == "Price: high to low":
        filtered.sort(key=lambda b: b["price"], reverse=True)
    elif sort_option == "Title A–Z":
        filtered.sort(key=lambda b: b["title"].lower())

    st.caption(f"{len(filtered)} books found")

    if not filtered:
        st.info("No books match these filters. Try another search.")
    else:
        for start in range(0, len(filtered), 4):
            columns = st.columns(4)

            for col, book in zip(columns, filtered[start:start + 4]):
                with col:
                    with st.container(border=True):
                        cover = book_cover(book["title"], book["author"])

                        if cover:
                            st.image(cover, use_container_width=True)
                        else:
                            st.markdown(
                                "<div style='height:190px;background:#EAF0F8;"
                                "border-radius:8px;display:flex;"
                                "align-items:center;justify-content:center;"
                                "text-align:center;padding:14px;color:#202938'>"
                                "<div><div style='font-size:32px'>📖</div>"
                                f"<b>{book['title']}</b><br>"
                                f"<small>{book['category']}</small></div></div>",
                                unsafe_allow_html=True
                            )

                        st.markdown(f"**{book['title']}**")
                        st.caption(book["author"])
                        st.markdown(
                            "<div class='book-price'>"
                            + rupees(book["price"])
                            + "</div>",
                            unsafe_allow_html=True
                        )

                        if book["available"]:
                            st.markdown(
                                "<div class='book-stock'>● In stock (demo)</div>",
                                unsafe_allow_html=True
                            )

                            if st.button(
                                "Add to cart",
                                key=f"add_{book['id']}",
                                use_container_width=True
                            ):
                                add_to_cart(book)
                                st.toast("Book added to cart")
                                st.rerun()
                        else:
                            st.markdown(
                                "<div class='book-unavailable'>"
                                "Currently unavailable</div>",
                                unsafe_allow_html=True
                            )

                            st.caption(
                                f"Estimated restock: {book['days']} days*"
                            )

                            if st.button(
                                "Find nearby store",
                                key=f"store_{book['id']}",
                                use_container_width=True
                            ):
                                st.session_state.selected_unavailable = book["id"]
                                st.session_state.page = "Find a book"
                                st.rerun()

                            if st.button(
                                "Request this book",
                                key=f"request_{book['id']}",
                                use_container_width=True
                            ):
                                st.session_state.requests.add(book["id"])
                                st.toast("Request saved for this session")

    st.caption(
        "*Availability and restock estimates are sample data, "
        "not confirmed supplier information."
    )

# =====================================================
# 8. CART AND CHECKOUT
# =====================================================

elif st.session_state.page == "Cart & checkout":

    st.markdown("## 🛒 Your cart")
    st.caption("Review your selected books and calculate your order.")

    cart_items = []

    for book_id, quantity in list(st.session_state.cart.items()):
        book = next((b for b in BOOKS if b["id"] == book_id), None)
        if book:
            cart_items.append((book, quantity))

    if not cart_items:
        st.info("Your cart is empty. Browse the catalogue to add books.")
    else:
        subtotal = 0

        for book, quantity in cart_items:
            c1, c2, c3, c4 = st.columns([4, 1.3, 1.5, 1])

            with c1:
                st.markdown(f"**{book['title']}**")
                st.caption(book["author"])

            with c2:
                updated_quantity = st.number_input(
                    "Quantity",
                    min_value=1,
                    max_value=99,
                    value=quantity,
                    key=f"quantity_{book['id']}"
                )
                st.session_state.cart[book["id"]] = updated_quantity

            line_total = book["price"] * updated_quantity
            subtotal += line_total

            with c3:
                st.markdown("**Line total**")
                st.write(rupees(line_total))

            with c4:
                if st.button("Remove", key=f"remove_{book['id']}"):
                    del st.session_state.cart[book["id"]]
                    st.rerun()

        st.divider()
        st.markdown("## Discount")

        discount_code = st.text_input(
            "Discount code",
            placeholder="Try PAGE5 for 5% off"
        )

        if discount_code.strip().upper() == "PAGE5":
            discount_rate = 0.05
            st.success("PAGE5 discount applied: 5%")
        else:
            discount_rate = 0.0
            if discount_code.strip():
                st.warning("Code not recognised. No discount applied.")

        discount = subtotal * discount_rate
        discounted_subtotal = subtotal - discount

        st.markdown("## Billing details")

        customer_name = st.text_input(
            "Customer name",
            placeholder="Enter your name"
        )

        customer_email = st.text_input(
            "Email address (optional)",
            placeholder="you@example.com"
        )

        gstin = st.text_input(
            "GSTIN (optional)",
            placeholder="Enter 15-character GSTIN",
            max_chars=15
        ).strip().upper()

        if gstin and (len(gstin) != 15 or not gstin.isalnum()):
            st.warning(
                "Check the GSTIN format. This is only a format check, "
                "not verification of registration."
            )

        gst_rate = st.selectbox(
            "Estimated GST rate",
            [0, 5, 12, 18],
            help="Select an assumed rate for this demo."
        )

        gst_amount = discounted_subtotal * gst_rate / 100
        total = discounted_subtotal + gst_amount

        st.divider()

        summary_col, total_col = st.columns([2, 1])

        with summary_col:
            st.markdown("### Order summary")
            st.write(f"Subtotal: {rupees(subtotal)}")
            st.write(f"Discount: −{rupees(discount)}")
            st.write(f"Estimated GST: {rupees(gst_amount)}")

        with total_col:
            st.markdown(
                "<div class='order-total'>"
                "<div style='font-weight:700;color:#566477'>ORDER TOTAL</div>"
                f"<div class='amount'>{rupees(total)}</div>"
                "<div style='color:#566477;font-size:13px'>"
                "Including estimated GST</div></div>",
                unsafe_allow_html=True
            )

        st.caption(
            "Demo checkout only. No payment is collected. GST rates are "
            "assumptions, and entering a GSTIN does not create a compliant "
            "tax invoice or verify registration."
        )

        if st.button(
            "Prepare receipt",
            type="primary",
            use_container_width=True
        ):
            receipt = io.StringIO()
            writer = csv.writer(receipt)

            writer.writerow(["PageNest Books & Learning — Demo Receipt"])
            writer.writerow([
                "Date", datetime.now().strftime("%Y-%m-%d %H:%M")
            ])
            writer.writerow(["Customer", customer_name])
            writer.writerow(["Email", customer_email])
            writer.writerow(["GSTIN entered", gstin])
            writer.writerow([])
            writer.writerow([
                "Book", "Author", "Quantity", "Unit price", "Line total"
            ])

            for book, _ in cart_items:
                qty = st.session_state.cart[book["id"]]
                writer.writerow([
                    book["title"],
                    book["author"],
                    qty,
                    book["price"],
                    book["price"] * qty
                ])

            writer.writerow([])
            writer.writerow(["Subtotal", subtotal])
            writer.writerow(["Discount", discount])
            writer.writerow(["Estimated GST", gst_amount])
            writer.writerow(["Total", total])

            st.download_button(
                "⬇ Download receipt (CSV)",
                data=receipt.getvalue(),
                file_name="pagenest_receipt.csv",
                mime="text/csv",
                use_container_width=True
            )

        if st.button("Empty cart"):
            st.session_state.cart = {}
            st.rerun()

# =====================================================
# 9. FIND BOOK / NEARBY STORE
# =====================================================

elif st.session_state.page == "Find a book":

    st.markdown("## 🔎 Find a book")
    st.write(
        "Look for unavailable books at nearby shops, or save a request."
    )

    unavailable = [b for b in BOOKS if not b["available"]]

    options = {
        f"{b['title']} — {b['author']}": b
        for b in unavailable
    }

    labels = list(options.keys())
    default_index = 0

    if st.session_state.selected_unavailable:
        for index, book in enumerate(unavailable):
            if book["id"] == st.session_state.selected_unavailable:
                default_index = index
                break

    selected_label = st.selectbox(
        "Select an unavailable book",
        labels,
        index=default_index
    )

    selected_book = options[selected_label]

    st.info(
        f"Sample restock estimate: {selected_book['days']} days. "
        "This is not a confirmed delivery date."
    )

    location = st.text_input(
        "Your city, area or PIN code",
        placeholder="For example, Sonipat"
    )

    if location.strip():
        st.link_button(
            "Search nearby bookstores on Google Maps",
            nearby_store_url(selected_book, location),
            use_container_width=True
        )

        st.caption(
            "Contact the shop to confirm the exact title, edition and stock."
        )

    if st.button("Request this book", type="primary"):
        st.session_state.requests.add(selected_book["id"])
        st.success("Your request is saved for this session.")

    st.divider()
    st.markdown("### Requested books")

    requested = [
        b for b in BOOKS if b["id"] in st.session_state.requests
    ]

    if requested:
        for book in requested:
            st.write(
                f"📖 {book['title']} — sample estimate: {book['days']} days"
            )
    else:
        st.caption("No book requests yet.")

    st.caption(
        "Requests are stored only for the current session. "
        "Email notifications and persistent requests need a database."
    )

# =====================================================
# 10. ABOUT
# =====================================================

elif st.session_state.page == "About PageNest":

    st.markdown("## About PageNest")

    st.write(
        "PageNest is a bookstore concept for students, readers and "
        "competitive exam aspirants. Its goal is to make finding the "
        "right book simple and comfortable."
    )

    st.markdown("### What you can do")
    st.write("- Search by title, author or subject.")
    st.write("- Filter by category and maximum price.")
    st.write("- View book cover images when available.")
    st.write("- Add books to your cart and change quantities.")
    st.write("- Apply a demo discount code.")
    st.write("- Estimate GST and download a receipt.")
    st.write("- Find nearby bookstores for unavailable titles.")

    st.caption(
        "Catalogue, prices, stock and restock times are illustrative. "
        "Verify book editions and availability before purchasing."
    )

# =====================================================
# 11. FOOTER
# =====================================================

st.divider()

footer_left, footer_right = st.columns(2)

with footer_left:
    st.markdown("**📚 PageNest | Books & Learning**")
    st.caption("Discover. Learn. Grow.")

with footer_right:
    st.caption(
        "A clean, accessible bookstore interface built with Streamlit."
    )
