
import streamlit as st
import urllib.parse
import urllib.request
import json
import difflib
import csv
import io
from datetime import datetime

st.set_page_config(
    page_title="PageNest Books & Learning",
    page_icon="📚",
    layout="wide"
)

# ---------------- CONFIGURATION ----------------

CURRENCY = "₹"
GST_RATE_DEFAULT = 0
DEFAULT_RESTOCK_DAYS = 5

BOOKS = [
    ("Mathematics", "NCERT Mathematics Class 11", "NCERT", 180, "school maths", True, 2),
    ("Mathematics", "NCERT Mathematics Class 12", "NCERT", 210, "school maths", True, 2),
    ("Mathematics", "Higher Engineering Mathematics", "B. S. Grewal", 850, "engineering maths", True, 4),
    ("Mathematics", "Business Mathematics", "J. K. Sharma", 550, "commerce maths", True, 3),
    ("Mathematics", "Calculus", "James Stewart", 1100, "calculus", False, 5),
    ("Mathematics", "Discrete Mathematics", "Kenneth Rosen", 950, "logic", True, 3),
    ("Mathematics", "RD Sharma Mathematics Class 11", "R. D. Sharma", 650, "school maths", True, 2),
    ("Mathematics", "RD Sharma Mathematics Class 12", "R. D. Sharma", 750, "school maths", True, 2),
    ("Mathematics", "Statistics for Business and Economics", "Anderson et al.", 900, "statistics", True, 4),
    ("Mathematics", "Advanced Engineering Mathematics", "Erwin Kreyszig", 950, "engineering maths", False, 6),

    ("Science", "Concepts of Physics Volume 1", "H. C. Verma", 450, "physics jee", True, 2),
    ("Science", "Concepts of Physics Volume 2", "H. C. Verma", 480, "physics jee", True, 2),
    ("Science", "NCERT Physics Class 11", "NCERT", 190, "school physics", True, 2),
    ("Science", "NCERT Physics Class 12", "NCERT", 220, "school physics", True, 2),
    ("Science", "NCERT Chemistry Class 11", "NCERT", 190, "chemistry", True, 2),
    ("Science", "NCERT Chemistry Class 12", "NCERT", 220, "chemistry", True, 2),
    ("Science", "Organic Chemistry", "Morrison and Boyd", 850, "chemistry", False, 5),
    ("Science", "Physical Chemistry", "P. Bahadur", 700, "chemistry", True, 3),
    ("Science", "Fundamentals of Biology", "NCERT", 250, "biology", True, 2),
    ("Science", "A Brief History of Time", "Stephen Hawking", 399, "space astronomy", True, 3),

    ("Commerce", "Accountancy Class 11", "T. S. Grewal", 650, "accounts", True, 2),
    ("Commerce", "Accountancy Class 12", "T. S. Grewal", 750, "accounts", True, 2),
    ("Commerce", "Business Studies Class 11", "NCERT", 180, "bst", True, 2),
    ("Commerce", "Business Studies Class 12", "NCERT", 220, "bst", True, 2),
    ("Commerce", "Introduction to Financial Accounting", "Charles T. Horngren", 950, "accounting", True, 4),
    ("Commerce", "Cost Accounting", "M. N. Arora", 850, "accounts", True, 4),
    ("Commerce", "Corporate Accounting", "S. N. Maheshwari", 900, "accounts", True, 4),
    ("Commerce", "Auditing and Assurance", "Vikas Oswal", 650, "audit", False, 5),
    ("Commerce", "Taxation", "V. K. Singhania", 950, "income tax", True, 3),
    ("Commerce", "Fundamentals of Accounting", "S. N. Maheshwari", 600, "accounts", True, 3),

    ("Economics", "Principles of Microeconomics", "N. Gregory Mankiw", 750, "micro economics", True, 2),
    ("Economics", "Principles of Macroeconomics", "N. Gregory Mankiw", 750, "macro economics", True, 2),
    ("Economics", "Intermediate Microeconomics", "Hal R. Varian", 1100, "micro theory", False, 6),
    ("Economics", "Macroeconomics", "Olivier Blanchard", 1050, "macro theory", True, 4),
    ("Economics", "Indian Economy", "Ramesh Singh", 850, "india economy upsc", True, 2),
    ("Economics", "Development Economics", "Debraj Ray", 950, "development", True, 4),
    ("Economics", "International Economics", "Dominick Salvatore", 900, "international trade", False, 5),
    ("Economics", "Public Finance", "H. L. Bhatia", 750, "government budget", True, 3),
    ("Economics", "Econometrics", "Damodar Gujarati", 1000, "statistics", True, 4),
    ("Economics", "Economics", "Paul A. Samuelson", 950, "economics principles", True, 4),

    ("Business & Management", "Principles of Management", "Harold Koontz", 650, "management", True, 2),
    ("Business & Management", "Management", "Stephen P. Robbins", 950, "organizational management", True, 3),
    ("Business & Management", "Marketing Management", "Philip Kotler", 1200, "marketing", True, 4),
    ("Business & Management", "Financial Management", "I. M. Pandey", 850, "finance", True, 3),
    ("Business & Management", "Human Resource Management", "Gary Dessler", 1000, "hr hrm", False, 5),
    ("Business & Management", "Operations Management", "Heizer and Render", 950, "operations", True, 4),
    ("Business & Management", "Organizational Behaviour", "Stephen P. Robbins", 900, "behavior", True, 3),
    ("Business & Management", "Business Research Methods", "Donald R. Cooper", 1000, "research", True, 4),
    ("Business & Management", "Entrepreneurship", "Hisrich and Peters", 850, "startup", True, 3),
    ("Business & Management", "Business Communication", "Meenakshi Raman", 550, "communication", True, 2),

    ("CAT / MBA", "Quantitative Aptitude for CAT", "Arun Sharma", 750, "cat maths", True, 2),
    ("CAT / MBA", "Data Interpretation for CAT", "Arun Sharma", 700, "cat di", True, 2),
    ("CAT / MBA", "Verbal Ability and Reading Comprehension", "Arun Sharma", 750, "cat varc english", True, 3),
    ("CAT / MBA", "Quantitative Aptitude for Competitive Examinations", "R. S. Aggarwal", 650, "aptitude", True, 2),
    ("CAT / MBA", "Verbal and Non-Verbal Reasoning", "R. S. Aggarwal", 600, "reasoning", True, 2),
    ("CAT / MBA", "Logical Reasoning and Data Interpretation", "Nishit K. Sinha", 700, "cat lrdi", False, 5),
    ("CAT / MBA", "CAT Previous Years Papers", "Various Authors", 450, "cat past papers", True, 2),
    ("CAT / MBA", "MBA Entrance Exam Practice Guide", "Various Authors", 500, "mba mock tests", True, 3),

    ("JEE", "Understanding Physics", "D. C. Pandey", 650, "jee physics", True, 2),
    ("JEE", "Problems in General Physics", "I. E. Irodov", 550, "advanced physics", False, 5),
    ("JEE", "Objective Mathematics", "R. D. Sharma", 850, "jee maths", True, 3),
    ("JEE", "IIT Mathematics", "M. L. Khanna", 750, "jee maths", True, 3),
    ("JEE", "Organic Chemistry", "O. P. Tandon", 700, "jee chemistry", True, 2),
    ("JEE", "Physical Chemistry", "O. P. Tandon", 700, "jee chemistry", True, 2),
    ("JEE", "Concise Inorganic Chemistry", "J. D. Lee", 850, "chemistry", False, 6),
    ("JEE", "JEE Main Previous Years Questions", "Various Authors", 500, "jee pyq", True, 2),

    ("NEET", "Objective Biology", "Dinesh", 750, "neet biology", True, 2),
    ("NEET", "Truemans Biology Volume 1", "M. P. Tyagi et al.", 850, "biology", True, 3),
    ("NEET", "Truemans Biology Volume 2", "M. P. Tyagi et al.", 850, "biology", True, 3),
    ("NEET", "Objective Physics for NEET", "D. C. Pandey", 700, "neet physics", True, 2),
    ("NEET", "Objective Chemistry for NEET", "R. K. Gupta", 700, "neet chemistry", True, 2),
    ("NEET", "NCERT Biology Class 11", "NCERT", 180, "biology", True, 2),
    ("NEET", "NCERT Biology Class 12", "NCERT", 220, "biology", True, 2),
    ("NEET", "NEET Previous Years Questions", "Various Authors", 500, "neet pyq", True, 2),

    ("UPSC", "Indian Polity", "M. Laxmikanth", 850, "constitution", True, 2),
    ("UPSC", "A Brief History of Modern India", "Spectrum", 650, "history", True, 2),
    ("UPSC", "Certificate Physical and Human Geography", "Goh Cheng Leong", 550, "geography", True, 3),
    ("UPSC", "Indias Struggle for Independence", "Bipan Chandra", 600, "history", True, 3),
    ("UPSC", "Indian Economy", "Ramesh Singh", 850, "economy", True, 2),
    ("UPSC", "Environment", "Shankar IAS Academy", 650, "ecology", True, 2),
    ("UPSC", "Oxford Student Atlas for India", "Oxford University Press", 350, "maps", True, 2),
    ("UPSC", "General Studies Manual", "Various Authors", 900, "gs prelims mains", False, 5),

    ("Other Competitive Exams", "Objective General English", "S. P. Bakshi", 550, "english grammar", True, 2),
    ("Other Competitive Exams", "Lucents General Knowledge", "Lucent", 350, "gk", True, 2),
    ("Other Competitive Exams", "Fast Track Objective Arithmetic", "Rajesh Verma", 550, "arithmetic", True, 3),
    ("Other Competitive Exams", "A Modern Approach to Verbal Reasoning", "R. S. Aggarwal", 450, "reasoning", True, 2),
    ("Other Competitive Exams", "General Knowledge 2026", "Various Authors", 400, "current affairs", True, 2),
    ("Other Competitive Exams", "Banking Awareness", "Arihant Experts", 350, "bank po", True, 2),
    ("Other Competitive Exams", "SSC CGL Practice Guide", "Arihant Experts", 500, "ssc", True, 3),
    ("Other Competitive Exams", "Railway Recruitment Exam Guide", "Arihant Experts", 450, "railway", True, 3),
]

CATALOGUE = [
    {
        "id": i + 1, "category": r[0], "title": r[1],
        "author": r[2], "price": r[3], "keywords": r[4],
        "available": r[5], "restock_days": r[6]
    }
    for i, r in enumerate(BOOKS)
]

CATEGORIES = ["All categories"] + sorted({b["category"] for b in CATALOGUE})

# ---------------- SESSION STATE ----------------

if "cart" not in st.session_state:
    st.session_state.cart = {}
if "requested_books" not in st.session_state:
    st.session_state.requested_books = set()

def money(amount):
    return f"{CURRENCY}{amount:,.2f}"

def normalise(text):
    return " ".join(
        "".join(c.lower() if c.isalnum() else " " for c in str(text)).split()
    )

def find_books(query, books):
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
                matches = difflib.get_close_matches(part, words, n=1, cutoff=0.55)
                scores.append(
                    difflib.SequenceMatcher(None, part, matches[0]).ratio()
                    if matches else 0.0
                )

        score = sum(scores) / max(1, len(scores))
        if score >= 0.55:
            results.append((score, book))

    results.sort(key=lambda x: (-x[0], x[1]["title"]))
    return [b for _, b in results]

@st.cache_data(ttl=86400, show_spinner=False)
def get_cover(title, author):
    query = urllib.parse.urlencode({"title": title, "author": author, "limit": 1})
    url = "https://openlibrary.org/search.json?" + query
    request = urllib.request.Request(
        url, headers={"User-Agent": "PageNestBookstore/1.0"}
    )
    try:
        with urllib.request.urlopen(request, timeout=2.5) as response:
            data = json.loads(response.read().decode("utf-8"))
        docs = data.get("docs", [])
        if docs and docs[0].get("cover_i"):
            return "https://covers.openlibrary.org/b/id/" + str(docs[0]["cover_i"]) + "-M.jpg"
    except Exception:
        pass
    return None

def maps_url(book, place):
    query = f"bookstore selling {book['title']} near {place}".strip()
    return "https://www.google.com/maps/search/?api=1&query=" + urllib.parse.quote(query)

def add_to_cart(book_id):
    book = next(b for b in CATALOGUE if b["id"] == book_id)
    if not book["available"]:
        st.session_state.requested_books.add(book_id)
        return
    st.session_state.cart[book_id] = st.session_state.cart.get(book_id, 0) + 1

# ---------------- STYLING ----------------

st.markdown("""
<style>
.stApp { background: #faf9f6; }
.block-container { padding-top: 1.1rem; max-width: 1450px; }
[data-testid="stSidebar"] { background: #f0eee8; }
h1, h2, h3 { color: #17283a; }
.book-name { font-weight: 650; font-size: .98rem; min-height: 2.6rem; }
.muted { color: #6b7280; font-size: .82rem; }
.price { font-size: 1.08rem; font-weight: 750; }
div.stButton > button {
  border-radius: 8px; border: 1px solid #e3b13f;
  background: #ffcf58; color: #18283b; font-weight: 600;
}
div.stButton > button:hover { background: #f3bb37; }
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------

header, cart_count = st.columns([5, 1])
with header:
    st.markdown("# 📚 PageNest")
    st.caption("BOOKS & LEARNING  ·  A quieter place to find your next book")
with cart_count:
    st.markdown("### 🛒 Cart")
    st.metric("Items", sum(st.session_state.cart.values()))

st.divider()

# ---------------- LEFT CATALOGUE SIDEBAR ----------------

with st.sidebar:
    st.markdown("## Browse catalogue")
    search = st.text_input("Search books", placeholder="Title, author or subject")
    category = st.selectbox("Category", CATEGORIES)
    price_limit = st.slider("Maximum price", 100, 2000, 2000, 50)
    publisher = st.text_input("Author / publisher", placeholder="Optional")
    st.divider()
    st.markdown("### Quick links")
    page = st.radio(
        "Go to",
        ["Browse books", "Cart & checkout", "Book requests", "About PageNest"],
        label_visibility="collapsed"
    )
    st.caption(f"{len(CATALOGUE)} catalogue entries")

# ---------------- MAIN BROWSE ----------------

if page == "Browse books":
    st.markdown("## Find your next book")
    st.caption("A simple catalogue, without the clutter.")

    books = [
        b for b in CATALOGUE
        if (category == "All categories" or b["category"] == category)
        and b["price"] <= price_limit
        and (not publisher.strip() or publisher.lower() in b["author"].lower())
    ]
    books = find_books(search, books)

    sort = st.selectbox("Sort by", ["Recommended", "Price: low to high", "Price: high to low", "Title"])
    if sort == "Price: low to high":
        books.sort(key=lambda b: b["price"])
    elif sort == "Price: high to low":
        books.sort(key=lambda b: b["price"], reverse=True)
    elif sort == "Title":
        books.sort(key=lambda b: b["title"].lower())

    st.caption(f"{len(books)} books found")

    if not books:
        st.info("No books found. Try another search or category.")
    else:
        for start in range(0, len(books), 4):
            cols = st.columns(4)
            for col, book in zip(cols, books[start:start + 4]):
                with col:
                    with st.container(border=True):
                        cover = get_cover(book["title"], book["author"])
                        if cover:
                            st.image(cover, use_container_width=True)
                        else:
                            st.markdown(
                                f"<div style='height:180px;background:#e9e5da;"
                                f"display:flex;align-items:center;justify-content:center;"
                                f"text-align:center;border-radius:6px;padding:12px;'>"
                                f"<span><b>{book['title']}</b><br><small>{book['category']}</small></span></div>",
                                unsafe_allow_html=True
                            )

                        st.markdown(f"**{book['title']}**")
                        st.caption(book["author"])
                        st.markdown(f"<div class='price'>{money(book['price'])}</div>", unsafe_allow_html=True)

                        if book["available"]:
                            st.caption("● In stock (demo status)")
                            if st.button("Add to cart", key=f"add_{book['id']}", use_container_width=True):
                                add_to_cart(book["id"])
                                st.toast("Added to cart")
                                st.rerun()
                        else:
                            st.caption("○ Currently unavailable")
                            st.caption(f"Estimated restock: {book['restock_days']} days (demo estimate)")
                            if st.button("Find nearby store", key=f"near_{book['id']}", use_container_width=True):
                                st.session_state.nearby_book_id = book["id"]
                                st.session_state.active_page = "Book requests"
                                st.rerun()
                            if st.button("Request this book", key=f"req_{book['id']}", use_container_width=True):
                                st.session_state.requested_books.add(book["id"])
                                st.toast("Book added to your request list")

    # Nearby-store section for selected unavailable book
    if "nearby_book_id" in st.session_state:
        target = next((b for b in CATALOGUE if b["id"] == st.session_state.nearby_book_id), None)
        if target:
            st.divider()
            st.subheader("Find this book nearby")
            st.write(target["title"])
            location = st.text_input(
                "Enter your city, area or PIN code",
                key="store_location",
                placeholder="For example, Sonipat or 131001"
            )
            if location.strip():
                st.link_button(
                    "Search nearby bookstores on Google Maps",
                    maps_url(target, location),
                    use_container_width=True
                )
                st.caption("Google Maps results depend on your location and local store listings. Availability must be confirmed with the shop.")

# ---------------- CART & CHECKOUT ----------------

elif page == "Cart & checkout":
    st.markdown("## 🛒 Cart & checkout")
    st.caption("Review quantities, discount, tax estimate and billing details.")

    items = []
    for book_id, quantity in list(st.session_state.cart.items()):
        book = next((b for b in CATALOGUE if b["id"] == book_id), None)
        if book:
            items.append((book, quantity))

    if not items:
        st.info("Your cart is empty. Browse the catalogue and add books first.")
    else:
        subtotal = 0
        for book, quantity in items:
            c1, c2, c3, c4 = st.columns([4, 1, 2, 1])
            with c1:
                st.write(f"**{book['title']}**")
                st.caption(book["author"])
            with c2:
                new_qty = st.number_input(
                    "Qty", 1, 99, quantity, key=f"qty_{book['id']}"
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
        st.subheader("Discount")
        discount_code = st.text_input("Discount code", placeholder="Try PAGE5")
        discount_rate = 0.05 if discount_code.strip().upper() == "PAGE5" else 0.0

        if discount_rate:
            st.success("PAGE5 discount applied: 5%")
        elif discount_code:
            st.warning("Code not recognised. No discount applied.")

        discount = subtotal * discount_rate
        taxable_total = subtotal - discount

        st.subheader("Billing details")
        customer_name = st.text_input("Customer name")
        customer_email = st.text_input("Email (optional)")
        gstin = st.text_input(
            "GSTIN (optional)",
            max_chars=15,
            placeholder="Enter GSTIN only if applicable"
        ).strip().upper()

        if gstin and (len(gstin) != 15 or not gstin.isalnum()):
            st.warning("GSTIN should contain 15 alphanumeric characters. Please verify it before using it on a tax invoice.")

        gst_rate = st.selectbox(
            "GST estimate (%)",
            [0, 5, 12, 18],
            index=0,
            help="This is a calculation aid, not a determination of the legally applicable rate."
        )
        gst_amount = taxable_total * gst_rate / 100
        total = taxable_total + gst_amount

        a, b = st.columns(2)
        with a:
            st.write("Subtotal", money(subtotal))
            st.write("Discount", f"-{money(discount)}")
            st.write("Estimated GST", money(gst_amount))
        with b:
            st.markdown(f"### Total: {money(total)}")

        st.caption("GSTIN entry does not verify registration or create a compliant tax invoice. Confirm applicable GST treatment before issuing a real invoice.")

        if st.button("Prepare bill / receipt", type="primary", use_container_width=True):
            output = io.StringIO()
            writer = csv.writer(output)
            writer.writerow(["PageNest Books & Learning - Demo Receipt"])
            writer.writerow(["Date", datetime.now().strftime("%Y-%m-%d %H:%M")])
            writer.writerow(["Customer", customer_name])
            writer.writerow(["Email", customer_email])
            writer.writerow(["GSTIN supplied", gstin])
            writer.writerow([])
            writer.writerow(["Book", "Author", "Quantity", "Unit Price", "Line Total"])
            for book, _ in items:
                qty = st.session_state.cart[book["id"]]
                writer.writerow([book["title"], book["author"], qty, book["price"], book["price"] * qty])
            writer.writerow([])
            writer.writerow(["Subtotal", subtotal])
            writer.writerow(["Discount", discount])
            writer.writerow(["Estimated GST", gst_amount])
            writer.writerow(["Total", total])

            st.download_button(
                "Download receipt (CSV)",
                output.getvalue(),
                file_name="pagenest_receipt.csv",
                mime="text/csv",
                use_container_width=True
            )
            st.info("This is a demo receipt, not proof of payment or a tax invoice.")

        if st.button("Empty cart"):
            st.session_state.cart = {}
            st.rerun()

# ---------------- BOOK REQUESTS / STORE FINDER ----------------

elif page == "Book requests":
    st.markdown("## Book requests & availability")
    st.write("For books not currently available, you can search nearby bookstores or keep a request in this session.")

    unavailable = [b for b in CATALOGUE if not b["available"]]
    book_options = {f"{b['title']} — {b['author']}": b for b in unavailable}
    selected_label = st.selectbox("Choose an unavailable book", list(book_options))
    selected_book = book_options[selected_label]

    st.info(f"Estimated restock time: {selected_book['restock_days']} days. This is a demo estimate, not a live supplier confirmation.")

    place = st.text_input("Your city, area or PIN code", placeholder="Enter a location to search nearby shops")
    if st.button("Find nearby bookstores", type="primary"):
        if place.strip():
            st.link_button(
                "Open nearby bookstore results",
                maps_url(selected_book, place),
                use_container_width=True
            )
            st.caption("Call the store to confirm the exact title, edition and stock.")
        else:
            st.warning("Enter your city, area or PIN code first.")

    if st.button("Request restock for this book"):
        st.session_state.requested_books.add(selected_book["id"])
        st.success("Request saved for this session.")

    st.subheader("Your requested books")
    requested = [b for b in CATALOGUE if b["id"] in st.session_state.requested_books]
    if requested:
        for book in requested:
            st.write(f"• {book['title']} — estimated {book['restock_days']} days")
    else:
        st.caption("No book requests yet.")

    st.caption("Requests are stored only while this app session is active. Email notifications and persistent requests require a database or notification service.")

# ---------------- ABOUT ----------------

elif page == "About PageNest":
    st.markdown("## About PageNest")
    st.write(
        "PageNest Books & Learning is a bookstore interface for textbooks, "
        "higher education and competitive exam preparation."
    )
    st.write("Browse books, filter by category and price, manage a cart and prepare a demo receipt.")
    st.caption("Catalogue prices, stock statuses and restock estimates are illustrative. Confirm actual availability and editions before purchasing.")

st.divider()
st.caption("PageNest Books & Learning · Built with Streamlit")
