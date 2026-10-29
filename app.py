
import streamlit as st
import urllib.parse
import urllib.request
import json
import re
from difflib import SequenceMatcher
from datetime import date, timedelta

# ============================================================
# PAGENEST | BOOKS & LEARNING
# Complete Streamlit bookstore application
# ============================================================

st.set_page_config(
    page_title="PageNest | Books & Learning",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ------------------------- DESIGN ----------------------------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}
.stApp {
    background: #F5F7FB;
    color: #172033;
}
header[data-testid="stHeader"] {
    background: transparent;
}
.block-container {
    padding-top: 1.5rem;
    padding-bottom: 3rem;
    max-width: 1500px;
}
h1, h2, h3 {
    color: #172033;
}
.hero {
    background: linear-gradient(120deg, #12264A 0%, #234C83 100%);
    padding: 36px;
    border-radius: 20px;
    color: white;
    margin-bottom: 24px;
}
.hero h1 {
    font-family: 'Playfair Display', serif;
    color: white;
    font-size: 42px;
    margin-bottom: 8px;
}
.hero p {
    color: #E4ECFA;
    font-size: 16px;
    margin-bottom: 0;
}
.section-title {
    font-family: 'Playfair Display', serif;
    font-size: 27px;
    font-weight: 700;
    margin-top: 14px;
    margin-bottom: 12px;
}
.book-card {
    background: white;
    border: 1px solid #E3E8F1;
    border-radius: 16px;
    padding: 14px;
    min-height: 145px;
    margin-bottom: 6px;
}
.book-title {
    font-size: 15px;
    font-weight: 700;
    color: #172033;
    line-height: 1.4;
    min-height: 40px;
}
.book-author {
    color: #65718A;
    font-size: 12px;
    min-height: 32px;
}
.book-category {
    color: #2857A4;
    background: #EAF1FF;
    display: inline-block;
    padding: 4px 8px;
    border-radius: 20px;
    font-size: 10px;
    font-weight: 700;
    margin: 5px 0;
}
.book-price {
    font-size: 19px;
    font-weight: 700;
    color: #163C78;
    margin-top: 6px;
}
.metric-card {
    background: white;
    border: 1px solid #E3E8F1;
    border-radius: 14px;
    padding: 16px;
}
.metric-label {
    color: #65718A;
    font-size: 13px;
}
.metric-value {
    font-size: 25px;
    font-weight: 700;
    color: #172033;
}
div.stButton > button {
    background: #2458A6;
    color: white;
    border: 0;
    border-radius: 9px;
    font-weight: 600;
    min-height: 40px;
}
div.stButton > button:hover {
    background: #173D79;
    color: white;
    border: 0;
}
div[data-testid="stSidebar"] {
    background: #EAF0F8;
}
div[data-testid="stSidebar"] h2,
div[data-testid="stSidebar"] h3 {
    color: #172033;
}
div[data-testid="stImage"] img {
    border-radius: 8px;
}
a {
    color: #2458A6;
}
.footer {
    background: #12264A;
    color: #E4ECFA;
    padding: 22px;
    border-radius: 14px;
    text-align: center;
    margin-top: 36px;
}
</style>
""", unsafe_allow_html=True)

# ----------------------- BOOK CATALOGUE ----------------------
# Prices are illustrative INR listing prices.
# Stock values are demo values; connect a database for live inventory.

RAW_BOOKS = [
    # Economics
    ("Principles of Economics", "N. Gregory Mankiw", "Economics", 899, 8),
    ("Principles of Microeconomics", "N. Gregory Mankiw", "Economics", 799, 7),
    ("Principles of Macroeconomics", "N. Gregory Mankiw", "Economics", 799, 6),
    ("Microeconomics", "Robert Pindyck and Daniel Rubinfeld", "Economics", 1199, 5),
    ("Intermediate Microeconomics", "Hal R. Varian", "Economics", 999, 4),
    ("Macroeconomics", "N. Gregory Mankiw", "Economics", 1099, 6),
    ("Economics", "Paul A. Samuelson and William D. Nordhaus", "Economics", 1299, 3),
    ("Development Economics", "Debraj Ray", "Economics", 999, 4),
    ("International Economics", "Dominick Salvatore", "Economics", 899, 5),
    ("The Wealth of Nations", "Adam Smith", "Economics", 499, 9),

    # Business and management
    ("Principles of Management", "Harold Koontz and Heinz Weihrich", "Business & Management", 799, 7),
    ("Management", "Stephen P. Robbins and Mary Coulter", "Business & Management", 999, 5),
    ("Organizational Behavior", "Stephen P. Robbins and Timothy Judge", "Business & Management", 1099, 5),
    ("Marketing Management", "Philip Kotler and Kevin Lane Keller", "Business & Management", 1299, 4),
    ("Fundamentals of Marketing", "William J. Stanton", "Business & Management", 799, 3),
    ("Human Resource Management", "Gary Dessler", "Business & Management", 999, 4),
    ("Operations Management", "Jay Heizer, Barry Render and Chuck Munson", "Business & Management", 1099, 5),
    ("Competitive Strategy", "Michael E. Porter", "Business & Management", 899, 4),
    ("The Lean Startup", "Eric Ries", "Business & Management", 499, 8),
    ("Good to Great", "Jim Collins", "Business & Management", 499, 6),
    ("The Personal MBA", "Josh Kaufman", "Business & Management", 599, 5),
    ("Business Model Generation", "Alexander Osterwalder and Yves Pigneur", "Business & Management", 899, 3),

    # Accounting and finance
    ("Financial Accounting", "Jerry J. Weygandt, Paul D. Kimmel and Donald E. Kieso", "Accounting & Finance", 999, 5),
    ("Accounting Principles", "Jerry J. Weygandt, Paul D. Kimmel and Donald E. Kieso", "Accounting & Finance", 899, 4),
    ("Fundamentals of Corporate Finance", "Stephen A. Ross, Randolph W. Westerfield and Bradford D. Jordan", "Accounting & Finance", 1199, 4),
    ("Corporate Finance", "Jonathan Berk and Peter DeMarzo", "Accounting & Finance", 1299, 3),
    ("Financial Management", "I. M. Pandey", "Accounting & Finance", 899, 6),
    ("Investment Analysis and Portfolio Management", "Frank K. Reilly and Keith C. Brown", "Accounting & Finance", 1199, 3),
    ("The Intelligent Investor", "Benjamin Graham", "Accounting & Finance", 599, 7),
    ("A Random Walk Down Wall Street", "Burton G. Malkiel", "Accounting & Finance", 599, 5),

    # Mathematics and statistics
    ("Business Mathematics", "J. K. Sharma", "Mathematics & Statistics", 599, 7),
    ("Business Statistics", "J. K. Sharma", "Mathematics & Statistics", 699, 6),
    ("Statistics for Business and Economics", "Paul Newbold, William Carlson and Betty Thorne", "Mathematics & Statistics", 999, 4),
    ("Fundamentals of Mathematical Statistics", "S. C. Gupta and V. K. Kapoor", "Mathematics & Statistics", 899, 5),
    ("Introduction to Probability", "Joseph K. Blitzstein and Jessica Hwang", "Mathematics & Statistics", 999, 4),
    ("Calculus", "James Stewart", "Mathematics & Statistics", 1099, 5),
    ("Linear Algebra and Its Applications", "David C. Lay", "Mathematics & Statistics", 999, 4),
    ("How to Solve It", "George Pólya", "Mathematics & Statistics", 399, 6),

    # Science and technology
    ("A Brief History of Time", "Stephen Hawking", "Science & Technology", 399, 7),
    ("Cosmos", "Carl Sagan", "Science & Technology", 499, 5),
    ("The Selfish Gene", "Richard Dawkins", "Science & Technology", 599, 4),
    ("The Origin of Species", "Charles Darwin", "Science & Technology", 499, 6),
    ("Concepts of Physics Volume 1", "H. C. Verma", "Science & Technology", 499, 8),
    ("Concepts of Physics Volume 2", "H. C. Verma", "Science & Technology", 499, 7),
    ("Fundamentals of Physics", "David Halliday, Robert Resnick and Jearl Walker", "Science & Technology", 1199, 4),
    ("Campbell Biology", "Lisa A. Urry and others", "Science & Technology", 1499, 3),
    ("The Feynman Lectures on Physics", "Richard P. Feynman, Robert B. Leighton and Matthew Sands", "Science & Technology", 1499, 2),

    # CAT and MBA entrance
    ("How to Prepare for Quantitative Aptitude for CAT", "Arun Sharma", "CAT & MBA Entrance", 699, 8),
    ("How to Prepare for Data Interpretation for CAT", "Arun Sharma", "CAT & MBA Entrance", 599, 7),
    ("How to Prepare for Verbal Ability and Reading Comprehension for CAT", "Arun Sharma", "CAT & MBA Entrance", 699, 8),
    ("Quantitative Aptitude for CAT", "Nishit K. Sinha", "CAT & MBA Entrance", 699, 6),
    ("Verbal Ability and Reading Comprehension for CAT", "Nishit K. Sinha", "CAT & MBA Entrance", 599, 5),
    ("Word Power Made Easy", "Norman Lewis", "CAT & MBA Entrance", 199, 10),
    ("A Modern Approach to Verbal and Non-Verbal Reasoning", "R. S. Aggarwal", "CAT & MBA Entrance", 499, 8),
    ("Logical Reasoning and Data Interpretation for CAT", "Nishit K. Sinha", "CAT & MBA Entrance", 699, 5),

    # JEE
    ("Concepts of Physics", "H. C. Verma", "JEE Preparation", 499, 8),
    ("Problems in General Physics", "I. E. Irodov", "JEE Preparation", 499, 5),
    ("Physical Chemistry", "O. P. Tandon", "JEE Preparation", 699, 6),
    ("Organic Chemistry", "Morrison and Boyd", "JEE Preparation", 999, 3),
    ("Concise Inorganic Chemistry", "J. D. Lee", "JEE Preparation", 799, 4),
    ("IIT Mathematics", "M. L. Khanna", "JEE Preparation", 799, 5),

    # NEET
    ("Objective Biology", "Dinesh", "NEET Preparation", 699, 6),
    ("Trueman's Elementary Biology", "M. P. Tyagi", "NEET Preparation", 799, 5),
    ("Objective Physics for NEET", "D. C. Pandey", "NEET Preparation", 699, 6),
    ("Objective Chemistry for NEET", "D. C. Pandey", "NEET Preparation", 699, 6),

    # UPSC and public examinations
    ("Indian Polity", "M. Laxmikanth", "UPSC & Civil Services", 799, 8),
    ("Certificate Physical and Human Geography", "Goh Cheng Leong", "UPSC & Civil Services", 499, 7),
    ("A Brief History of Modern India", "Rajiv Ahir", "UPSC & Civil Services", 499, 8),
    ("India's Struggle for Independence", "Bipan Chandra", "UPSC & Civil Services", 599, 6),
    ("Indian Economy", "Ramesh Singh", "UPSC & Civil Services", 899, 5),
    ("Environment", "Shankar IAS Academy", "UPSC & Civil Services", 699, 6),
    ("Introduction to the Constitution of India", "D. D. Basu", "UPSC & Civil Services", 699, 4),
    ("Our Parliament", "Subhash Kashyap", "UPSC & Civil Services", 399, 5),

    # Law and communication
    ("Business Law", "Robert W. Emerson", "Law & Communication", 899, 4),
    ("Business Law Including Company Law", "P. C. Tulsian", "Law & Communication", 799, 5),
    ("Business Communication Today", "Courtland L. Bovee and John V. Thill", "Law & Communication", 999, 3),
    ("The Elements of Style", "William Strunk Jr. and E. B. White", "Law & Communication", 299, 7),
    ("On Writing Well", "William Zinsser", "Law & Communication", 399, 5),

    # Programming and research
    ("Python Crash Course", "Eric Matthes", "Programming & Research", 799, 6),
    ("Automate the Boring Stuff with Python", "Al Sweigart", "Programming & Research", 699, 5),
    ("Learning Python", "Mark Lutz", "Programming & Research", 1199, 3),
    ("Think Python", "Allen B. Downey", "Programming & Research", 599, 5),
    ("Research Design", "John W. Creswell and J. David Creswell", "Programming & Research", 999, 4),
    ("The Craft of Research", "Wayne C. Booth and others", "Programming & Research", 699, 5),
    ("Research Methodology", "C. R. Kothari", "Programming & Research", 599, 7),
]

BOOKS = []
for index, item in enumerate(RAW_BOOKS):
    title, author, category, price, stock = item
    BOOKS.append({
        "id": index + 1,
        "title": title,
        "author": author,
        "category": category,
        "price": price,
        "stock": stock,
    })

# ---------------------- SESSION STATE ------------------------

if "cart" not in st.session_state:
    st.session_state.cart = {}

if "last_order" not in st.session_state:
    st.session_state.last_order = None

if "page" not in st.session_state:
    st.session_state.page = "Catalogue"

# ---------------------- COVER LOOKUP -------------------------

def clean_text(value):
    value = re.sub(r"[^a-zA-Z0-9 ]", " ", str(value).lower())
    return " ".join(value.split())


def title_similarity(first, second):
    return SequenceMatcher(
        None, clean_text(first), clean_text(second)
    ).ratio()


@st.cache_data(ttl=86400, show_spinner=False)
def book_cover(title, author):
    """Find a cover using Google Books, then Open Library."""

    def get_json(url):
        request = urllib.request.Request(
            url,
            headers={"User-Agent": "PageNestBookstore/1.0"}
        )
        with urllib.request.urlopen(request, timeout=4) as response:
            return json.loads(response.read().decode("utf-8"))

    # Google Books API
    try:
        query = f'intitle:"{title}" inauthor:"{author}"'
        url = (
            "https://www.googleapis.com/books/v1/volumes?"
            + urllib.parse.urlencode({
                "q": query,
                "maxResults": 8,
                "printType": "books",
            })
        )

        data = get_json(url)

        for item in data.get("items", []):
            info = item.get("volumeInfo", {})
            result_title = info.get("title", "")

            if title_similarity(title, result_title) < 0.58:
                continue

            result_authors = info.get("authors", [])
            author_match = (
                not result_authors
                or any(
                    title_similarity(author, result_author) > 0.45
                    or title_similarity(result_author, author) > 0.45
                    for result_author in result_authors
                )
            )

            if not author_match:
                continue

            links = info.get("imageLinks", {})
            image_url = (
                links.get("extraLarge")
                or links.get("large")
                or links.get("medium")
                or links.get("thumbnail")
                or links.get("smallThumbnail")
            )

            if image_url:
                return image_url.replace("http://", "https://")

    except Exception:
        pass

    # Open Library API
    try:
        url = (
            "https://openlibrary.org/search.json?"
            + urllib.parse.urlencode({
                "title": title,
                "author": author,
                "limit": 10,
                "fields": "title,author_name,cover_i",
            })
        )

        data = get_json(url)

        for item in data.get("docs", []):
            result_title = item.get("title", "")
            result_authors = item.get("author_name", [])

            if title_similarity(title, result_title) < 0.58:
                continue

            author_match = (
                not result_authors
                or any(
                    title_similarity(author, result_author) > 0.45
                    or title_similarity(result_author, author) > 0.45
                    for result_author in result_authors
                )
            )

            cover_id = item.get("cover_i")
            if author_match and cover_id:
                return (
                    f"https://covers.openlibrary.org/b/id/"
                    f"{cover_id}-L.jpg?default=false"
                )

    except Exception:
        pass

    return None


# ----------------------- CART HELPERS ------------------------

def cart_quantity():
    return sum(st.session_state.cart.values())


def cart_subtotal():
    return sum(
        next(book["price"] for book in BOOKS if book["id"] == book_id) * quantity
        for book_id, quantity in st.session_state.cart.items()
    )


def add_to_cart(book_id):
    book = next(book for book in BOOKS if book["id"] == book_id)
    current_quantity = st.session_state.cart.get(book_id, 0)

    if current_quantity >= book["stock"]:
        st.warning("Sorry, no more copies are available in the demo inventory.")
        return

    st.session_state.cart[book_id] = current_quantity + 1
    st.toast(f"Added {book['title']} to your cart!")


# -------------------------- HEADER ---------------------------

st.markdown("""
<div class="hero">
    <h1>PageNest</h1>
    <p>Books, ideas and possibilities — all in one place.</p>
    <p>Explore academic textbooks, competitive exam preparation,
    business classics and research resources.</p>
</div>
""", unsafe_allow_html=True)

metric1, metric2, metric3 = st.columns(3)

with metric1:
    st.markdown(
        f'<div class="metric-card"><div class="metric-label">Books in catalogue</div>'
        f'<div class="metric-value">{len(BOOKS)}</div></div>',
        unsafe_allow_html=True,
    )

with metric2:
    st.markdown(
        f'<div class="metric-card"><div class="metric-label">Subjects</div>'
        f'<div class="metric-value">{len(set(b["category"] for b in BOOKS))}</div></div>',
        unsafe_allow_html=True,
    )

with metric3:
    st.markdown(
        f'<div class="metric-card"><div class="metric-label">Items in your cart</div>'
        f'<div class="metric-value">{cart_quantity()}</div></div>',
        unsafe_allow_html=True,
    )

st.write("")

# -------------------------- SIDEBAR --------------------------

with st.sidebar:
    st.markdown("## 📚 PageNest")
    st.caption("Your personal bookstore")

    page_choice = st.radio(
        "Navigate",
        ["Catalogue", "Shopping Cart", "Checkout", "Find a Book"],
        index=["Catalogue", "Shopping Cart", "Checkout", "Find a Book"].index(
            st.session_state.page
        ),
    )
    st.session_state.page = page_choice

    st.divider()

    st.markdown("### 🔎 Find your next book")

    search_query = st.text_input(
        "Search title or author",
        placeholder="e.g. Microeconomics",
        key="catalogue_search",
    )

    categories = ["All Subjects"] + sorted(set(
        book["category"] for book in BOOKS
    ))

    selected_category = st.selectbox(
        "Subject",
        categories,
        key="catalogue_category",
    )

    max_price = max(book["price"] for book in BOOKS)
    price_limit = st.slider(
        "Maximum price (₹)",
        min_value=100,
        max_value=max_price,
        value=max_price,
        step=100,
    )

    availability_filter = st.selectbox(
        "Availability",
        ["All Books", "In Stock", "Out of Stock"],
    )

    st.divider()

    st.markdown("### 🛒 Your cart")
    st.metric("Items", cart_quantity())
    st.metric("Subtotal", f"₹{cart_subtotal():,.2f}")

    if st.button("View Cart", use_container_width=True):
        st.session_state.page = "Shopping Cart"
        st.rerun()

    st.caption("Prices shown are sample catalogue prices.")

# --------------------- CATALOGUE FILTERS ---------------------

filtered_books = BOOKS.copy()

if search_query.strip():
    query = clean_text(search_query)
    filtered_books = [
        book for book in filtered_books
        if query in clean_text(book["title"])
        or query in clean_text(book["author"])
        or query in clean_text(book["category"])
    ]

if selected_category != "All Subjects":
    filtered_books = [
        book for book in filtered_books
        if book["category"] == selected_category
    ]

filtered_books = [
    book for book in filtered_books
    if book["price"] <= price_limit
]

if availability_filter == "In Stock":
    filtered_books = [book for book in filtered_books if book["stock"] > 0]
elif availability_filter == "Out of Stock":
    filtered_books = [book for book in filtered_books if book["stock"] == 0]

# ------------------------ CATALOGUE PAGE ---------------------

if st.session_state.page == "Catalogue":
    st.markdown('<div class="section-title">Explore the Catalogue</div>',
                unsafe_allow_html=True)

    st.caption(
        f"Showing {len(filtered_books)} of {len(BOOKS)} books. "
        "Use the sidebar to filter by subject, price or availability."
    )

    sort_option = st.selectbox(
        "Sort books by",
        ["Recommended", "Price: Low to High", "Price: High to Low", "Title A–Z"],
    )

    if sort_option == "Price: Low to High":
        filtered_books.sort(key=lambda book: book["price"])
    elif sort_option == "Price: High to Low":
        filtered_books.sort(key=lambda book: book["price"], reverse=True)
    elif sort_option == "Title A–Z":
        filtered_books.sort(key=lambda book: book["title"].lower())

    if not filtered_books:
        st.warning("No books match those filters.")
        st.info("Try another search term or increase your maximum price.")

    else:
        # Three cards per row
        for start in range(0, len(filtered_books), 3):
            row_books = filtered_books[start:start + 3]
            columns = st.columns(3)

            for column, book in zip(columns, row_books):
                with column:
                    with st.container(border=True):
                        cover = book_cover(book["title"], book["author"])

                        if cover:
                            try:
                                st.image(cover, use_container_width=True)
                            except Exception:
                                st.info("Cover image could not be displayed.")
                        else:
                            st.markdown(
                                "<div style='height:190px;display:flex;"
                                "align-items:center;justify-content:center;"
                                "background:#EAF0F8;border-radius:10px;"
                                "font-size:48px;'>📚</div>",
                                unsafe_allow_html=True,
                            )
                            image_query = urllib.parse.quote(
                                f'{book["title"]} {book["author"]} book cover'
                            )
                            st.markdown(
                                f"[Search for this book's cover](https://www.google.com/search?tbm=isch&q={image_query})"
                            )

                        st.markdown(
                            f'<div class="book-title">{book["title"]}</div>',
                            unsafe_allow_html=True,
                        )
                        st.markdown(
                            f'<div class="book-author">{book["author"]}</div>',
                            unsafe_allow_html=True,
                        )
                        st.markdown(
                            f'<span class="book-category">{book["category"]}</span>',
                            unsafe_allow_html=True,
                        )
                        st.markdown(
                            f'<div class="book-price">₹{book["price"]:,}</div>',
                            unsafe_allow_html=True,
                        )

                        if book["stock"] > 0:
                            st.caption(f"{book['stock']} copies in demo stock")
                            if st.button(
                                "＋ Add to Cart",
                                key=f"add_{book['id']}",
                                use_container_width=True,
                            ):
                                add_to_cart(book["id"])
                                st.rerun()
                        else:
                            st.warning("Currently unavailable")
                            if st.button(
                                "Find Nearby Store",
                                key=f"nearby_{book['id']}",
                                use_container_width=True,
                            ):
                                st.session_state["find_book_title"] = book["title"]
                                st.session_state.page = "Find a Book"
                                st.rerun()

# ------------------------ SHOPPING CART ----------------------

elif st.session_state.page == "Shopping Cart":
    st.markdown('<div class="section-title">Your Shopping Cart</div>',
                unsafe_allow_html=True)

    if not st.session_state.cart:
        st.info("Your cart is empty. Explore the catalogue to add books.")
        if st.button("Continue Shopping"):
            st.session_state.page = "Catalogue"
            st.rerun()

    else:
        for book_id in list(st.session_state.cart.keys()):
            book = next(book for book in BOOKS if book["id"] == book_id)
            quantity = st.session_state.cart[book_id]

            with st.container(border=True):
                col1, col2, col3, col4 = st.columns([4, 1, 2, 1])

                with col1:
                    st.markdown(f"**{book['title']}**")
                    st.caption(f"{book['author']} · {book['category']}")

                with col2:
                    st.write(f"Qty: {quantity}")

                with col3:
                    st.write(f"₹{book['price'] * quantity:,.2f}")

                with col4:
                    if st.button("Remove", key=f"remove_{book_id}"):
                        del st.session_state.cart[book_id]
                        st.rerun()

                qty_col1, qty_col2, qty_col3 = st.columns([1, 1, 4])

                with qty_col1:
                    if st.button("−", key=f"minus_{book_id}"):
                        if quantity <= 1:
                            del st.session_state.cart[book_id]
                        else:
                            st.session_state.cart[book_id] = quantity - 1
                        st.rerun()

                with qty_col2:
                    if st.button("+", key=f"plus_{book_id}"):
                        if quantity < book["stock"]:
                            st.session_state.cart[book_id] = quantity + 1
                        else:
                            st.warning("Maximum available demo stock reached.")
                        st.rerun()

        st.divider()

        subtotal = cart_subtotal()
        st.markdown(f"### Subtotal: ₹{subtotal:,.2f}")
        st.caption("Shipping and applicable taxes, if any, are calculated at checkout.")

        cart_actions1, cart_actions2 = st.columns(2)

        with cart_actions1:
            if st.button("Continue Shopping", use_container_width=True):
                st.session_state.page = "Catalogue"
                st.rerun()

        with cart_actions2:
            if st.button("Proceed to Checkout", use_container_width=True):
                st.session_state.page = "Checkout"
                st.rerun()

# ---------------------------- CHECKOUT -----------------------

elif st.session_state.page == "Checkout":
    st.markdown('<div class="section-title">Checkout</div>',
                unsafe_allow_html=True)

    if not st.session_state.cart:
        st.info("Your cart is empty. Add books before checking out.")
        if st.button("Browse Books"):
            st.session_state.page = "Catalogue"
            st.rerun()

    else:
        subtotal = cart_subtotal()

        st.markdown("### Order Summary")

        for book_id, quantity in st.session_state.cart.items():
            book = next(book for book in BOOKS if book["id"] == book_id)
            st.write(
                f"**{book['title']}** × {quantity} — "
                f"₹{book['price'] * quantity:,.2f}"
            )

        st.divider()

        with st.form("checkout_form"):
            st.markdown("### Delivery Details")

            full_name = st.text_input("Full Name *")
            email = st.text_input("Email Address *")
            phone = st.text_input("Phone Number *")
            address = st.text_area("Delivery Address *")
            city = st.text_input("City *")
            state = st.text_input("State *")
            pincode = st.text_input("PIN Code *")

            st.markdown("### Invoice Details")
            gstin = st.text_input(
                "GSTIN (optional)",
                placeholder="Enter GSTIN if applicable",
            )

            discount_code = st.text_input(
                "Discount Code",
                placeholder="Try PAGENEST10",
            )

            st.caption(
                "This is a demonstration checkout. It does not process "
                "payments or place a real order."
            )

            submitted = st.form_submit_button(
                "Calculate Total",
                use_container_width=True,
            )

        if submitted:
            required_fields = [
                full_name, email, phone, address,
                city, state, pincode
            ]

            if not all(field.strip() for field in required_fields):
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
                discount = 0

                if discount_code.strip().upper() == "PAGENEST10":
                    discount = round(subtotal * 0.10, 2)
                    st.success("PAGENEST10 applied: 10% discount.")
                elif discount_code.strip():
                    st.warning("Code not recognised. No discount applied.")

                total = max(0, subtotal - discount)

                st.session_state.last_order = {
                    "name": full_name.strip(),
                    "email": email.strip(),
                    "phone": phone.strip(),
                    "address": address.strip(),
                    "city": city.strip(),
                    "state": state.strip(),
                    "pincode": pincode.strip(),
                    "gstin": gstin.strip().upper(),
                    "subtotal": subtotal,
                    "discount": discount,
                    "total": total,
                    "items": len(st.session_state.cart),
                    "order_date": date.today().isoformat(),
                }

                st.markdown("### Your Estimated Total")

                total_col1, total_col2, total_col3 = st.columns(3)

                total_col1.metric("Subtotal", f"₹{subtotal:,.2f}")
                total_col2.metric("Discount", f"−₹{discount:,.2f}")
                total_col3.metric("Total", f"₹{total:,.2f}")

                st.info(
                    "Your order summary has been calculated. "
                    "No payment has been taken and no real order has been placed."
                )

        if st.session_state.last_order:
            order = st.session_state.last_order

            st.divider()
            st.markdown("### Latest Calculated Order")
            st.write(f"**Customer:** {order['name']}")
            st.write(f"**Order date:** {order['order_date']}")
            st.write(f"**Delivery city:** {order['city']}, {order['state']}")
            st.write(f"**Items:** {order['items']}")
            st.write(f"**Total:** ₹{order['total']:,.2f}")

            summary_text = (
                "PAGENEST ORDER SUMMARY\n"
                f"Customer: {order['name']}\n"
                f"Email: {order['email']}\n"
                f"Phone: {order['phone']}\n"
                f"Delivery address: {order['address']}, {order['city']}, "
                f"{order['state']} {order['pincode']}\n"
                f"GSTIN: {order['gstin'] or 'Not provided'}\n"
                f"Subtotal: INR {order['subtotal']:.2f}\n"
                f"Discount: INR {order['discount']:.2f}\n"
                f"Total: INR {order['total']:.2f}\n"
                f"Date: {order['order_date']}\n"
                "Demo only; payment not processed."
            )

            st.download_button(
                "Download Order Summary",
                data=summary_text,
                file_name="pagenest_order_summary.txt",
                mime="text/plain",
                use_container_width=True,
            )

# ------------------------ FIND A BOOK ------------------------

elif st.session_state.page == "Find a Book":
    st.markdown('<div class="section-title">Find a Book</div>',
                unsafe_allow_html=True)

    st.write(
        "Can't find a title or it's out of stock? Search online bookstores "
        "or look for nearby bookshops."
    )

    default_title = st.session_state.get("find_book_title", "")

    find_title = st.text_input(
        "Book title",
        value=default_title,
        placeholder="Enter the title you need",
        key="find_title_input",
    )

    find_author = st.text_input(
        "Author (optional)",
        placeholder="Enter author name",
    )

    city_for_search = st.text_input(
        "City or area",
        placeholder="e.g. Sonipat, Haryana",
    )

    if st.button("Search for Book", use_container_width=True):
        if not find_title.strip():
            st.error("Please enter a book title.")
        else:
            search_text = " ".join(
                part for part in [find_title.strip(), find_author.strip()]
                if part
            )

            online_query = urllib.parse.quote(search_text + " buy book India")
            maps_query = urllib.parse.quote(
                "bookstores near " + city_for_search.strip()
                if city_for_search.strip()
                else "bookstores near me"
            )
            cover_query = urllib.parse.quote(search_text + " book cover")

            st.markdown("### Search Results")
            st.markdown(
                f"[Search Google for this book](https://www.google.com/search?q={online_query})"
            )
            st.markdown(
                f"[Search Google Images for the cover](https://www.google.com/search?tbm=isch&q={cover_query})"
            )
            st.markdown(
                f"[Find nearby bookstores on Google Maps](https://www.google.com/maps/search/?api=1&query={maps_query})"
            )

            estimated_date = date.today() + timedelta(days=7)

            st.markdown("### Estimated Restocking")
            st.write(
                f"If the supplier can fulfil the order, a sample restocking "
                f"estimate is **{estimated_date.strftime('%d %B %Y')}**."
            )
            st.caption(
                "This is only a planning estimate, not a confirmed supplier date. "
                "Actual availability and delivery time must be verified with the seller."
            )

# --------------------------- FOOTER --------------------------

st.markdown("""
<div class="footer">
    <strong>PageNest | Books & Learning</strong><br>
    Find your next idea. Discover your next chapter.<br>
    <span style="font-size:12px;">
        Student project demonstration · Sample prices and inventory
    </span>
</div>
""", unsafe_allow_html=True)
