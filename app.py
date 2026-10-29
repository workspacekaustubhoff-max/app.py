
import streamlit as st
import urllib.request
import urllib.parse
import json
import difflib

st.set_page_config(
    page_title="PageNest | Books & Learning",
    page_icon="📚",
    layout="wide"
)

# -------------------- THEME --------------------

st.markdown("""
<style>
.stApp { background: #faf9f6; color: #17202a; }
.block-container { padding-top: 1.3rem; max-width: 1500px; }
[data-testid="stSidebar"] { background: #f0eee8; }
h1, h2, h3 { color: #18283b; }
.book-card {
    background: white;
    border: 1px solid #e6e5e0;
    border-radius: 12px;
    padding: 12px;
    min-height: 100px;
}
.price { font-size: 1.15rem; font-weight: 750; color: #17202a; }
.small-note { color: #687385; font-size: 0.85rem; }
div.stButton > button {
    border-radius: 8px;
    border: 1px solid #e8ad2e;
    background: #ffc94d;
    color: #17202a;
    font-weight: 650;
}
div.stButton > button:hover {
    background: #f3b82f;
    border-color: #e0a21c;
}
</style>
""", unsafe_allow_html=True)

# -------------------- BOOK CATALOGUE --------------------
# Illustrative catalogue and prices. Verify editions before purchase.

RAW_BOOKS = [
    ("Mathematics", "NCERT Mathematics Class 11", "NCERT", 180, "school maths"),
    ("Mathematics", "NCERT Mathematics Class 12", "NCERT", 210, "school maths"),
    ("Mathematics", "Higher Engineering Mathematics", "B. S. Grewal", 850, "engineering calculus"),
    ("Mathematics", "Business Mathematics", "J. K. Sharma", 550, "commerce maths"),
    ("Mathematics", "Calculus", "James Stewart", 1100, "differentiation integration"),
    ("Mathematics", "Discrete Mathematics", "Kenneth Rosen", 950, "logic"),
    ("Mathematics", "RD Sharma Mathematics Class 11", "R. D. Sharma", 650, "school maths"),
    ("Mathematics", "RD Sharma Mathematics Class 12", "R. D. Sharma", 750, "school maths"),
    ("Mathematics", "Statistics for Business and Economics", "Anderson et al.", 900, "statistics"),
    ("Mathematics", "Advanced Engineering Mathematics", "Erwin Kreyszig", 950, "engineering maths"),

    ("Science", "Concepts of Physics Volume 1", "H. C. Verma", 450, "physics"),
    ("Science", "Concepts of Physics Volume 2", "H. C. Verma", 480, "physics"),
    ("Science", "NCERT Physics Class 11", "NCERT", 190, "school physics"),
    ("Science", "NCERT Physics Class 12", "NCERT", 220, "school physics"),
    ("Science", "NCERT Chemistry Class 11", "NCERT", 190, "chemistry"),
    ("Science", "NCERT Chemistry Class 12", "NCERT", 220, "chemistry"),
    ("Science", "Organic Chemistry", "Morrison and Boyd", 850, "chemistry"),
    ("Science", "Physical Chemistry", "P. Bahadur", 700, "chemistry"),
    ("Science", "Fundamentals of Biology", "NCERT", 250, "biology"),
    ("Science", "A Brief History of Time", "Stephen Hawking", 399, "space astronomy"),

    ("Commerce", "Accountancy Class 11", "T. S. Grewal", 650, "accounts"),
    ("Commerce", "Accountancy Class 12", "T. S. Grewal", 750, "accounts"),
    ("Commerce", "Business Studies Class 11", "NCERT", 180, "bst"),
    ("Commerce", "Business Studies Class 12", "NCERT", 220, "bst"),
    ("Commerce", "Introduction to Financial Accounting", "Charles T. Horngren", 950, "accounting"),
    ("Commerce", "Cost Accounting", "M. N. Arora", 850, "accounts"),
    ("Commerce", "Corporate Accounting", "S. N. Maheshwari", 900, "accounts"),
    ("Commerce", "Auditing and Assurance", "Vikas Oswal", 650, "audit"),
    ("Commerce", "Taxation", "V. K. Singhania", 950, "income tax"),
    ("Commerce", "Fundamentals of Accounting", "S. N. Maheshwari", 600, "accounts"),

    ("Economics", "Principles of Microeconomics", "N. Gregory Mankiw", 750, "micro economics"),
    ("Economics", "Principles of Macroeconomics", "N. Gregory Mankiw", 750, "macro economics"),
    ("Economics", "Intermediate Microeconomics", "Hal R. Varian", 1100, "micro theory"),
    ("Economics", "Macroeconomics", "Olivier Blanchard", 1050, "macro theory"),
    ("Economics", "Indian Economy", "Ramesh Singh", 850, "india economy"),
    ("Economics", "Development Economics", "Debraj Ray", 950, "development"),
    ("Economics", "International Economics", "Dominick Salvatore", 900, "international trade"),
    ("Economics", "Public Finance", "H. L. Bhatia", 750, "government budget"),
    ("Economics", "Econometrics", "Damodar Gujarati", 1000, "statistics"),
    ("Economics", "Economics", "Paul A. Samuelson", 950, "economics principles"),

    ("Business & Management", "Principles of Management", "Harold Koontz", 650, "management"),
    ("Business & Management", "Management", "Stephen P. Robbins", 950, "organizational management"),
    ("Business & Management", "Marketing Management", "Philip Kotler", 1200, "marketing"),
    ("Business & Management", "Financial Management", "I. M. Pandey", 850, "finance"),
    ("Business & Management", "Human Resource Management", "Gary Dessler", 1000, "hr hrm"),
    ("Business & Management", "Operations Management", "Heizer and Render", 950, "operations"),
    ("Business & Management", "Organizational Behaviour", "Stephen P. Robbins", 900, "behavior"),
    ("Business & Management", "Business Research Methods", "Donald R. Cooper", 1000, "research"),
    ("Business & Management", "Entrepreneurship", "Hisrich and Peters", 850, "startup"),
    ("Business & Management", "Business Communication", "Meenakshi Raman", 550, "communication"),

    ("CAT / MBA", "Quantitative Aptitude for CAT", "Arun Sharma", 750, "cat maths"),
    ("CAT / MBA", "Data Interpretation for CAT", "Arun Sharma", 700, "cat di"),
    ("CAT / MBA", "Verbal Ability and Reading Comprehension", "Arun Sharma", 750, "cat varc english"),
    ("CAT / MBA", "Quantitative Aptitude for Competitive Examinations", "R. S. Aggarwal", 650, "aptitude"),
    ("CAT / MBA", "Verbal and Non-Verbal Reasoning", "R. S. Aggarwal", 600, "reasoning"),
    ("CAT / MBA", "Logical Reasoning and Data Interpretation", "Nishit K. Sinha", 700, "cat lrdi"),
    ("CAT / MBA", "CAT Previous Years' Papers", "Various Authors", 450, "cat past papers"),
    ("CAT / MBA", "MBA Entrance Exam Practice Guide", "Various Authors", 500, "mba mock tests"),

    ("JEE", "Understanding Physics", "D. C. Pandey", 650, "jee physics"),
    ("JEE", "Problems in General Physics", "I. E. Irodov", 550, "advanced physics"),
    ("JEE", "Objective Mathematics", "R. D. Sharma", 850, "jee maths"),
    ("JEE", "IIT Mathematics", "M. L. Khanna", 750, "jee maths"),
    ("JEE", "Organic Chemistry", "O. P. Tandon", 700, "jee chemistry"),
    ("JEE", "Physical Chemistry", "O. P. Tandon", 700, "jee chemistry"),
    ("JEE", "Concise Inorganic Chemistry", "J. D. Lee", 850, "chemistry"),
    ("JEE", "JEE Main Previous Years' Questions", "Various Authors", 500, "jee pyq"),

    ("NEET", "Objective Biology", "Dinesh", 750, "neet biology"),
    ("NEET", "Trueman's Biology Volume 1", "M. P. Tyagi et al.", 850, "biology"),
    ("NEET", "Trueman's Biology Volume 2", "M. P. Tyagi et al.", 850, "biology"),
    ("NEET", "Objective Physics for NEET", "D. C. Pandey", 700, "neet physics"),
    ("NEET", "Objective Chemistry for NEET", "R. K. Gupta", 700, "neet chemistry"),
    ("NEET", "NCERT Biology Class 11", "NCERT", 180, "biology"),
    ("NEET", "NCERT Biology Class 12", "NCERT", 220, "biology"),
    ("NEET", "NEET Previous Years' Questions", "Various Authors", 500, "neet pyq"),

    ("UPSC", "Indian Polity", "M. Laxmikanth", 850, "constitution"),
    ("UPSC", "A Brief History of Modern India", "Spectrum", 650, "history"),
    ("UPSC", "Certificate Physical and Human Geography", "Goh Cheng Leong", 550, "geography"),
    ("UPSC", "India's Struggle for Independence", "Bipan Chandra", 600, "history"),
    ("UPSC", "Indian Economy", "Ramesh Singh", 850, "economy"),
    ("UPSC", "Environment", "Shankar IAS Academy", 650, "ecology"),
    ("UPSC", "Oxford Student Atlas for India", "Oxford University Press", 350, "maps"),
    ("UPSC", "General Studies Manual", "Various Authors", 900, "gs prelims mains"),

    ("Other Competitive Exams", "Objective General English", "S. P. Bakshi", 550, "english grammar"),
    ("Other Competitive Exams", "Lucent's General Knowledge", "Lucent", 350, "gk"),
    ("Other Competitive Exams", "Fast Track Objective Arithmetic", "Rajesh Verma", 550, "arithmetic"),
    ("Other Competitive Exams", "A Modern Approach to Verbal Reasoning", "R. S. Aggarwal", 450, "reasoning"),
    ("Other Competitive Exams", "General Knowledge 2026", "Various Authors", 400, "current affairs"),
    ("Other Competitive Exams", "Banking Awareness", "Arihant Experts", 350, "bank po"),
    ("Other Competitive Exams", "SSC CGL Practice Guide", "Arihant Experts", 500, "ssc"),
    ("Other Competitive Exams", "Railway Recruitment Exam Guide", "Arihant Experts", 450, "railway"),
]

BOOKS = [
    {
        "id": i + 1,
        "category": row[0],
        "title": row[1],
        "author": row[2],
        "price": row[3],
        "keywords": row[4],
    }
    for i, row in enumerate(RAW_BOOKS)
]

CATEGORIES = list(dict.fromkeys(b["category"] for b in BOOKS))

CATEGORY_EMOJI = {
    "Mathematics": "📐",
    "Science": "🔬",
    "Commerce": "📊",
    "Economics": "📈",
    "Business & Management": "💼",
    "CAT / MBA": "🎯",
    "JEE": "⚛️",
    "NEET": "🧬",
    "UPSC": "🇮🇳",
    "Other Competitive Exams": "🏆",
}

CATEGORY_IMAGES = {
    "Mathematics": "https://images.unsplash.com/photo-1509228468518-180dd4864904?w=500",
    "Science": "https://images.unsplash.com/photo-1532094349884-543bc11b234d?w=500",
    "Commerce": "https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=500",
    "Economics": "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=500",
    "Business & Management": "https://images.unsplash.com/photo-1521737711867-e3b97375f902?w=500",
    "CAT / MBA": "https://images.unsplash.com/photo-1434030216411-0b793f4b4173?w=500",
    "JEE": "https://images.unsplash.com/photo-1635070041078-e363dbe005cb?w=500",
    "NEET": "https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?w=500",
    "UPSC": "https://images.unsplash.com/photo-1524492412937-b28074a5d7da?w=500",
    "Other Competitive Exams": "https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?w=500",
}

# -------------------- COVER LOOKUP --------------------

@st.cache_data(ttl=86400, show_spinner=False)
def get_cover_url(title, author):
    """Look up a book cover from Open Library. Returns None if unavailable."""
    query = urllib.parse.urlencode({
        "title": title,
        "author": author,
        "limit": 1
    })
    url = "https://openlibrary.org/search.json?" + query
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "PageNestBookstore/1.0"}
    )
    try:
        with urllib.request.urlopen(request, timeout=3) as response:
            data = json.loads(response.read().decode("utf-8"))
        docs = data.get("docs", [])
        if docs and docs[0].get("cover_i"):
            cover_id = docs[0]["cover_i"]
            return f"https://covers.openlibrary.org/b/id/{cover_id}-M.jpg"
    except Exception:
        pass
    return None

def normalise(value):
    return " ".join(
        "".join(c.lower() if c.isalnum() else " " for c in str(value)).split()
    )

def search_books(query, books):
    if not query.strip():
        return books

    query = normalise(query)
    ranked = []

    for book in books:
        text = normalise(
            book["title"] + " " + book["author"] + " "
            + book["category"] + " " + book["keywords"]
        )
        if query in text:
            ranked.append((1.0, book))
            continue

        words = text.split()
        query_words = query.split()
        scores = []

        for qword in query_words:
            if qword in words:
                scores.append(1.0)
            else:
                match = difflib.get_close_matches(qword, words, n=1, cutoff=0.55)
                scores.append(
                    difflib.SequenceMatcher(None, qword, match[0]).ratio()
                    if match else 0
                )

        score = sum(scores) / len(scores) if scores else 0
        if score >= 0.55:
            ranked.append((score, book))

    ranked.sort(key=lambda x: (-x[0], x[1]["title"]))
    return [book for _, book in ranked]

# -------------------- CART STATE --------------------

if "cart" not in st.session_state:
    st.session_state.cart = {}

def add_to_cart(book_id):
    st.session_state.cart[book_id] = st.session_state.cart.get(book_id, 0) + 1

def money(value):
    return f"₹{value:,.0f}"

# -------------------- HEADER --------------------

top1, top2 = st.columns([3, 1])
with top1:
    st.markdown("# 📖 PageNest")
    st.caption("BOOKS & LEARNING  ·  Discover. Learn. Grow.")
with top2:
    st.markdown("### 🛒 Cart")
    st.metric("Items", sum(st.session_state.cart.values()))

st.divider()

# -------------------- HERO BANNER --------------------

st.markdown("""
<div style="
background: linear-gradient(90deg, rgba(17,30,43,.96), rgba(17,30,43,.62)),
url('https://images.unsplash.com/photo-1507842217343-583bb7270b66?w=1800');
background-size: cover; background-position: center;
padding: 42px 34px; border-radius: 16px; color: white;
">
<p style="color:#ffce58; letter-spacing:2px; font-weight:700;">
YOUR NEXT CHAPTER STARTS HERE
</p>
<h1 style="color:white; font-size:clamp(28px,4vw,46px);">
Find the book that moves you forward.
</h1>
<p style="font-size:18px; color:#f3f4f6;">
Explore textbooks, competitive exam guides and books for curious minds.
</p>
</div>
""", unsafe_allow_html=True)

st.write("")

# -------------------- SEARCH AND FILTERS --------------------

search_col, category_col = st.columns([3, 2])

with search_col:
    query = st.text_input(
        "Search the library",
        placeholder="Search by title, author, publisher or subject..."
    )

with category_col:
    selected_category = st.selectbox(
        "Browse a category",
        ["All Categories"] + CATEGORIES
    )

with st.expander("⚙️ More filters"):
    filter1, filter2, filter3 = st.columns(3)

    with filter1:
        max_price = st.slider("Maximum price (₹)", 100, 2000, 2000, 50)

    with filter2:
        sort_by = st.selectbox(
            "Sort books by",
            ["Recommended", "Price: Low to High", "Price: High to Low", "Title A–Z"]
        )

    with filter3:
        publisher_query = st.text_input("Filter author/publisher")

filtered = [
    b for b in BOOKS
    if (selected_category == "All Categories" or b["category"] == selected_category)
    and b["price"] <= max_price
    and (not publisher_query.strip() or publisher_query.lower() in b["author"].lower())
]

filtered = search_books(query, filtered)

if sort_by == "Price: Low to High":
    filtered.sort(key=lambda b: b["price"])
elif sort_by == "Price: High to Low":
    filtered.sort(key=lambda b: b["price"], reverse=True)
elif sort_by == "Title A–Z":
    filtered.sort(key=lambda b: b["title"].lower())

# -------------------- CATEGORY TILES --------------------

st.subheader("Shop by Category")

category_cols = st.columns(5)

for index, category in enumerate(CATEGORIES):
    with category_cols[index % 5]:
        st.image(CATEGORY_IMAGES[category], use_container_width=True)
        if st.button(
            f"{CATEGORY_EMOJI[category]} {category}",
            key=f"category_{category}",
            use_container_width=True
        ):
            st.session_state.chosen_category = category
            st.rerun()

if "chosen_category" in st.session_state:
    chosen = st.session_state.chosen_category
    st.info(f"Selected category: {chosen}")
    if st.button("Clear category selection"):
        del st.session_state.chosen_category
        st.rerun()

# -------------------- BOOK CARDS --------------------

st.divider()
st.subheader("📚 Explore Books")
st.caption(f"{len(filtered)} books match your search and filters.")

def show_book_card(book):
    with st.container(border=True):
        cover_url = get_cover_url(book["title"], book["author"])

        if cover_url:
            try:
                st.image(cover_url, use_container_width=True)
            except Exception:
                st.image(CATEGORY_IMAGES[book["category"]], use_container_width=True)
        else:
            st.image(CATEGORY_IMAGES[book["category"]], use_container_width=True)

        st.markdown(f"**{book['title']}**")
        st.caption(book["author"])
        st.caption(book["category"])
        st.markdown(f"<div class='price'>{money(book['price'])}</div>",
                    unsafe_allow_html=True)

        if st.button("＋ Add to Cart", key=f"add_{book['id']}", use_container_width=True):
            add_to_cart(book["id"])
            st.toast("Added to your cart!")
            st.rerun()

if filtered:
    for start in range(0, len(filtered), 5):
        cols = st.columns(5)
        for col, book in zip(cols, filtered[start:start + 5]):
            with col:
                show_book_card(book)
else:
    st.info("No books found. Try a different search or adjust the filters.")

# -------------------- SHOPPING CART --------------------

st.divider()
st.subheader("🛒 Your Cart")

cart_books = [
    (next((b for b in BOOKS if b["id"] == book_id), None), qty)
    for book_id, qty in st.session_state.cart.items()
]
cart_books = [(b, qty) for b, qty in cart_books if b is not None]

if not cart_books:
    st.write("Your cart is empty. Add a few books to get started.")
else:
    subtotal = 0

    for book, qty in cart_books:
        c1, c2, c3, c4 = st.columns([4, 1, 2, 1])
        with c1:
            st.write(book["title"])
            st.caption(book["author"])
        with c2:
            st.write(f"× {qty}")
        with c3:
            st.write(money(book["price"] * qty))
        with c4:
            if st.button("Remove", key=f"remove_{book['id']}"):
                del st.session_state.cart[book["id"]]
                st.rerun()
        subtotal += book["price"] * qty

    discount = subtotal * (0.10 if subtotal >= 2000 else 0.05 if subtotal >= 1000 else 0)
    st.write(f"Subtotal: {money(subtotal)}")
    st.write(f"Estimated discount: −{money(discount)}")
    st.markdown(f"### Total: {money(subtotal - discount)}")

    st.caption("Demo cart only. This website does not process payments.")
    if st.button("Clear Cart"):
        st.session_state.cart = {}
        st.rerun()

# -------------------- FOOTER --------------------

st.divider()
footer1, footer2, footer3 = st.columns(3)

with footer1:
    st.markdown("**📖 PageNest**")
    st.caption("A home for every curious mind.")

with footer2:
    st.markdown("**Explore**")
    st.caption("Textbooks · Economics · Business · Exam Prep")

with footer3:
    st.markdown("**About**")
    st.caption("A student bookstore demo built with Streamlit.")

st.caption(
    "Book-cover availability depends on Open Library. Some titles may show a category image instead. "
    "Prices are illustrative; confirm editions, ISBNs and availability before purchase."
)
