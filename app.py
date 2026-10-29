
import streamlit as st
import urllib.request
import urllib.parse
import json
from datetime import datetime

# =====================================================
# THE BUSINESS BOOKSHOP | COMPLETE STREAMLIT WEBSITE
# =====================================================

st.set_page_config(
    page_title="The Business Bookshop",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------- DESIGN ------------------------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@500;600;700&display=swap');

.stApp {
    background: #F7F5EF;
    color: #253B30;
    font-family: 'DM Sans', sans-serif;
}
h1, h2, h3 {
    font-family: 'Playfair Display', serif !important;
    color: #234536 !important;
}
.hero {
    background: linear-gradient(125deg, #183C2D, #507858);
    padding: 45px 35px;
    border-radius: 22px;
    color: white;
    margin-bottom: 28px;
}
.hero h1 {
    color: #FFF8E9 !important;
    font-size: 44px;
}
.hero p {
    color: #E6EDDF;
    font-size: 17px;
}
.eyebrow {
    letter-spacing: 3px;
    font-size: 12px;
    color: #D4E2C5;
    text-transform: uppercase;
}
.book-card {
    background: #FFFFFF;
    border: 1px solid #E8E4D9;
    border-radius: 15px;
    padding: 15px;
    min-height: 165px;
    margin-bottom: 8px;
}
.book-title {
    font-family: 'Playfair Display', serif;
    color: #234536;
    font-size: 19px;
    font-weight: 600;
}
.book-subject {
    color: #65816A;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 1px;
    text-transform: uppercase;
}
.book-author, .muted {
    color: #777D73;
    font-size: 12px;
}
.book-price {
    color: #234536;
    font-size: 22px;
    font-weight: 700;
}
div.stButton > button {
    background: #234536;
    color: white;
    border: none;
    border-radius: 9px;
    min-height: 40px;
}
div.stButton > button:hover {
    background: #4D7555;
    color: white;
    border: none;
}
div[data-testid="stMetric"] {
    background: white;
    border: 1px solid #E8E4D9;
    padding: 15px;
    border-radius: 12px;
}
[data-testid="stSidebar"] {
    background: #F0EEE5;
}
hr {
    border-color: #E4E0D5;
}
.footer {
    text-align: center;
    padding: 20px;
    color: #777D73;
}
</style>
""", unsafe_allow_html=True)


# ---------------------- BOOK DATABASE -----------------

BOOKS = {
    "B101": {
        "title": "Principles of Microeconomics",
        "subject": "Microeconomics",
        "author": "N. Gregory Mankiw",
        "mrp": 799,
        "discount": 10,
        "isbn": "9780357133484",
        "description": "Discover demand, supply, markets and consumer choices."
    },
    "B102": {
        "title": "Principles of Macroeconomics",
        "subject": "Macroeconomics",
        "author": "N. Gregory Mankiw",
        "mrp": 849,
        "discount": 12,
        "isbn": "9780357133491",
        "description": "Explore GDP, inflation, unemployment and economic growth."
    },
    "B103": {
        "title": "Business Statistics",
        "subject": "Business Statistics",
        "author": "Academic Reference",
        "mrp": 599,
        "discount": 10,
        "isbn": "",
        "description": "Learn probability, data analysis and statistical methods."
    },
    "B104": {
        "title": "Business Mathematics",
        "subject": "Business Mathematics",
        "author": "Academic Reference",
        "mrp": 549,
        "discount": 15,
        "isbn": "",
        "description": "Practice percentages, equations and business calculations."
    },
    "B105": {
        "title": "Financial Accounting",
        "subject": "Financial Accounting",
        "author": "Academic Reference",
        "mrp": 699,
        "discount": 10,
        "isbn": "",
        "description": "Understand journal entries, ledgers and financial statements."
    },
    "B106": {
        "title": "Python for Everybody",
        "subject": "Python",
        "author": "Charles R. Severance",
        "mrp": 649,
        "discount": 15,
        "isbn": "9781530051120",
        "description": "Start programming with Python and practical examples."
    },
    "B107": {
        "title": "Business Law",
        "subject": "Legal Aspects of Business",
        "author": "Academic Reference",
        "mrp": 749,
        "discount": 10,
        "isbn": "",
        "description": "Explore contracts, regulations and business law."
    },
    "B108": {
        "title": "Media, Society and Government",
        "subject": "Media, Society and Government",
        "author": "Academic Reference",
        "mrp": 499,
        "discount": 8,
        "isbn": "",
        "description": "Understand media, public opinion and government."
    },
    "B109": {
        "title": "The Personal MBA",
        "subject": "Business Studies",
        "author": "Josh Kaufman",
        "mrp": 699,
        "discount": 12,
        "isbn": "9781591843528",
        "description": "Explore business, marketing and management fundamentals."
    }
}

SUBJECT_ICONS = {
    "Microeconomics": "📉",
    "Macroeconomics": "🌍",
    "Business Statistics": "📊",
    "Business Mathematics": "➗",
    "Financial Accounting": "🧾",
    "Python": "💻",
    "Legal Aspects of Business": "⚖️",
    "Media, Society and Government": "📰",
    "Business Studies": "💼"
}


# ---------------------- SESSION STATE -----------------

if "cart" not in st.session_state:
    st.session_state.cart = {}

if "page" not in st.session_state:
    st.session_state.page = "Home"

if "selected_subject" not in st.session_state:
    st.session_state.selected_subject = "All Subjects"

if "last_order" not in st.session_state:
    st.session_state.last_order = None


# ---------------------- FUNCTIONS ---------------------

def money(amount):
    """Format numbers as Indian rupees."""
    return f"₹{amount:,.2f}"


def get_book(book_id):
    """Return a book using its unique ID."""
    return BOOKS.get(book_id, {})


def calculate_price(mrp, discount_percent):
    """Calculate discount and selling price."""
    discount_amount = mrp * discount_percent / 100
    selling_price = mrp - discount_amount

    return {
        "mrp": round(mrp, 2),
        "discount_percent": discount_percent,
        "discount_amount": round(discount_amount, 2),
        "selling_price": round(selling_price, 2)
    }


@st.cache_data(ttl=3600, show_spinner=False)
def get_book_cover(isbn, title):
    """Retrieve cover images from Google Books with a fallback."""
    fallback = (
        "https://images.unsplash.com/"
        "photo-1507842217343-583bb7270b66"
        "?auto=format&fit=crop&w=500&q=80"
    )

    query = f"isbn:{isbn}" if isbn else f'intitle:"{title}"'
    url = (
        "https://www.googleapis.com/books/v1/volumes?q="
        + urllib.parse.quote(query)
        + "&maxResults=1"
    )

    try:
        request = urllib.request.Request(
            url,
            headers={"User-Agent": "BusinessBookshop/1.0"}
        )

        with urllib.request.urlopen(request, timeout=3) as response:
            data = json.loads(response.read().decode("utf-8"))

        items = data.get("items", [])

        if items:
            info = items[0].get("volumeInfo", {})
            images = info.get("imageLinks", {})
            cover = images.get("thumbnail", images.get("smallThumbnail"))

            if cover:
                return cover.replace("http://", "https://")

    except Exception:
        pass

    return fallback


def calculate_bill(cart, gst_rate=0):
    """Calculate total MRP, discounts, GST and amount payable."""
    total_mrp = 0
    total_discount = 0
    subtotal = 0
    item_count = 0

    # FOR LOOP: process each item in the shopping cart.
    for book_id, quantity in cart.items():
        book = get_book(book_id)

        if book:
            price = calculate_price(
                book.get("mrp", 0),
                book.get("discount", 0)
            )

            total_mrp += price["mrp"] * quantity
            total_discount += price["discount_amount"] * quantity
            subtotal += price["selling_price"] * quantity
            item_count += quantity

    gst_amount = subtotal * gst_rate / 100

    return {
        "item_count": item_count,
        "mrp_total": round(total_mrp, 2),
        "discount_total": round(total_discount, 2),
        "subtotal": round(subtotal, 2),
        "gst_rate": gst_rate,
        "gst_amount": round(gst_amount, 2),
        "grand_total": round(subtotal + gst_amount, 2)
    }


def search_books(keyword, subject):
    """Find books by title, author or subject."""
    results = []
    keyword = keyword.lower().strip()

    # FOR LOOP: check every book in the dictionary.
    for book_id, book in BOOKS.items():
        title = book.get("title", "").lower()
        author = book.get("author", "").lower()
        category = book.get("subject", "")

        if subject != "All Subjects" and category != subject:
            continue

        # IF / ELIF / ELSE conditions.
        if not keyword:
            results.append(book_id)
        elif (
            keyword in title
            or keyword in author
            or keyword in category.lower()
        ):
            results.append(book_id)
        else:
            continue

    return results


def add_to_cart(book_id):
    """Add a book to the shopping cart."""
    st.session_state.cart[book_id] = (
        st.session_state.cart.get(book_id, 0) + 1
    )


def navigate_to(page, subject=None):
    """Change the page from a button callback."""
    st.session_state.page = page

    if subject:
        st.session_state.selected_subject = subject


def display_book(book_id):
    """Display a book with its image, price and cart button."""
    book = get_book(book_id)

    if not book:
        return

    price = calculate_price(
        book.get("mrp", 0),
        book.get("discount", 0)
    )

    cover = get_book_cover(
        book.get("isbn", ""),
        book.get("title", "")
    )

    st.image(cover, use_container_width=True)

    st.markdown(
        f"""
        <div class="book-card">
            <div class="book-subject">
                {SUBJECT_ICONS.get(book.get("subject", ""), "📚")}
                {book.get("subject", "Books")}
            </div>
            <div class="book-title">{book.get("title", "Book")}</div>
            <div class="book-author">{book.get("author", "Unknown author")}</div>
            <p>{book.get("description", "")}</p>
            <div class="book-price">{money(price["selling_price"])}</div>
            <div class="muted">
                MRP: {money(price["mrp"])} |
                Save {price["discount_percent"]}%
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    with st.expander("View price details"):
        st.write("MRP:", money(price["mrp"]))
        st.write("Discount:", money(price["discount_amount"]))
        st.write("Price before GST:", money(price["selling_price"]))

    st.button(
        "🛒 Add to cart",
        key=f"add_{book_id}",
        use_container_width=True,
        on_click=add_to_cart,
        args=(book_id,)
    )


# ---------------------- SIDEBAR -----------------------

with st.sidebar:
    st.markdown("## 📚 The Business Bookshop")
    st.caption("Your campus learning companion")
    st.divider()

    st.radio(
        "EXPLORE",
        ["Home", "Browse Books", "Shopping Cart", "My Bill", "About Us"],
        key="page"
    )

    st.divider()
    st.metric(
        "Books in your cart",
        sum(st.session_state.cart.values())
    )

    st.caption("Read better. Learn smarter. Grow further.")


# ---------------------- HERO --------------------------

st.markdown("""
<div class="hero">
    <div class="eyebrow">READ • LEARN • GROW</div>
    <h1>The Business Bookshop</h1>
    <p>Your next big idea starts with the right book.</p>
    <p>Discover economics, finance, mathematics, programming and more.</p>
</div>
""", unsafe_allow_html=True)


# ====================== HOME PAGE =====================

if st.session_state.page == "Home":

    st.markdown("## Welcome to your learning space")
    st.write(
        "Explore academic books, discover new subjects and find "
        "resources for your learning journey."
    )

    a, b, c = st.columns(3)

    a.metric("Subjects", len(SUBJECT_ICONS))
    b.metric("Books listed", len(BOOKS))
    c.metric("Starting price", "₹499")

    st.divider()
    st.markdown("## Explore by subject")

    subject_names = list(SUBJECT_ICONS.keys())

    # FOR LOOP: show the subjects in rows of three.
    for start in range(0, len(subject_names), 3):
        columns = st.columns(3)

        for index, subject in enumerate(subject_names[start:start + 3]):
            with columns[index]:
                st.markdown(
                    f"""
                    <div class="book-card">
                        <div style="font-size:32px">
                            {SUBJECT_ICONS.get(subject, "📚")}
                        </div>
                        <div class="book-title">{subject}</div>
                        <div class="book-author">Learn at your own pace</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                st.button(
                    "Explore books",
                    key=f"subject_{index}_{start}",
                    use_container_width=True,
                    on_click=navigate_to,
                    args=("Browse Books", subject)
                )

    st.divider()
    st.markdown("## Editor's picks")

    columns = st.columns(3)

    for index, book_id in enumerate(["B101", "B106", "B109"]):
        with columns[index]:
            display_book(book_id)


# ====================== BROWSE PAGE ===================

elif st.session_state.page == "Browse Books":

    st.markdown("## Browse our collection")
    st.write("Search by title, author or subject.")

    subjects = ["All Subjects"] + list(SUBJECT_ICONS.keys())
    current_subject = st.session_state.selected_subject

    if current_subject not in subjects:
        current_subject = "All Subjects"

    selected_subject = st.selectbox(
        "Choose a subject",
        subjects,
        index=subjects.index(current_subject)
    )

    # Keep the selected subject for navigation from Home.
    st.session_state.selected_subject = selected_subject

    keyword = st.text_input(
        "🔍 Search books",
        placeholder="Try Python, economics or accounting"
    )

    matching_ids = search_books(keyword, selected_subject)

    st.caption(f"{len(matching_ids)} book(s) found")
    st.divider()

    if not matching_ids:
        st.info("No books found. Try another search.")

    else:
        # FOR LOOP: render each matching book in a three-column grid.
        for start in range(0, len(matching_ids), 3):
            columns = st.columns(3)

            for index, book_id in enumerate(matching_ids[start:start + 3]):
                with columns[index]:
                    display_book(book_id)


# ====================== CART PAGE =====================

elif st.session_state.page == "Shopping Cart":

    st.markdown("## Your shopping cart")

    if not st.session_state.cart:
        st.info("Your cart is empty. Browse our collection to get started.")

        st.button(
            "Browse books",
            on_click=navigate_to,
            args=("Browse Books",)
        )

    else:
        # WHILE LOOP: process cart items by their position.
        cart_ids = list(st.session_state.cart.keys())
        index = 0

        while index < len(cart_ids):
            book_id = cart_ids[index]
            book = get_book(book_id)

            if book:
                price = calculate_price(
                    book.get("mrp", 0),
                    book.get("discount", 0)
                )

                with st.container(border=True):
                    col1, col2, col3 = st.columns([3, 2, 1])

                    with col1:
                        st.markdown(f"**{book.get('title', 'Book')}**")
                        st.caption(book.get("subject", ""))
                        st.caption(
                            f"Unit price: {money(price['selling_price'])}"
                        )

                    with col2:
                        quantity = st.number_input(
                            "Quantity",
                            min_value=1,
                            max_value=20,
                            value=st.session_state.cart[book_id],
                            key=f"quantity_{book_id}"
                        )
                        st.session_state.cart[book_id] = quantity

                    with col3:
                        st.markdown("**Line total**")
                        st.write(
                            money(price["selling_price"] * quantity)
                        )

                        st.button(
                            "Remove",
                            key=f"remove_{book_id}",
                            on_click=lambda bid=book_id: (
                                st.session_state.cart.pop(bid, None)
                            )
                        )

            index += 1

        st.divider()

        bill = calculate_bill(st.session_state.cart)

        a, b = st.columns(2)
        a.metric("Total MRP", money(bill["mrp_total"]))
        b.metric("Total savings", money(bill["discount_total"]))

        st.subheader(f"Subtotal: {money(bill['subtotal'])}")

        st.button(
            "Proceed to billing",
            use_container_width=True,
            on_click=navigate_to,
            args=("My Bill",)
        )

        st.button(
            "Clear entire cart",
            on_click=lambda: st.session_state.cart.clear()
        )


# ====================== BILL PAGE =====================

elif st.session_state.page == "My Bill":

    st.markdown("## Checkout & billing")

    if not st.session_state.cart:
        st.info("Your cart is empty. Add a book before generating a bill.")

        st.button(
            "Browse books",
            on_click=navigate_to,
            args=("Browse Books",)
        )

    else:
        customer_name = st.text_input(
            "Customer name",
            placeholder="Enter your full name"
        )

        customer_email = st.text_input(
            "Email address (optional)",
            placeholder="you@example.com"
        )

        st.markdown("### Tax settings")

        st.caption(
            "Select a rate only after verifying the applicable tax treatment. "
            "The default is 0% for this demonstration."
        )

        gst_rate = st.selectbox(
            "GST rate for this calculation",
            [0, 5, 12, 18, 28],
            index=0,
            format_func=lambda rate: f"{rate}%"
        )

        bill = calculate_bill(st.session_state.cart, gst_rate)

        st.divider()
        st.markdown("### THE BUSINESS BOOKSHOP")
        st.caption(
            f"Demonstration receipt • "
            f"{datetime.now().strftime('%d %b %Y, %I:%M %p')}"
        )
        st.write(f"**Customer:** {customer_name or 'Guest'}")

        if customer_email:
            st.write(f"**Email:** {customer_email}")

        st.divider()

        # FOR LOOP: print every item in the bill.
        for book_id, quantity in st.session_state.cart.items():
            book = get_book(book_id)

            if book:
                price = calculate_price(
                    book.get("mrp", 0),
                    book.get("discount", 0)
                )

                st.write(f"**{book.get('title', 'Book')} × {quantity}**")
                st.caption(
                    f"MRP each: {money(price['mrp'])} | "
                    f"Discount: {price['discount_percent']}%"
                )
                st.write(
                    f"Line total: "
                    f"{money(price['selling_price'] * quantity)}"
                )

        st.divider()

        # BILL SUMMARY
        st.write("Total MRP", money(bill["mrp_total"]))
        st.write("Total discount", f"- {money(bill['discount_total'])}")
        st.write("Subtotal after discount", money(bill["subtotal"]))
        st.write(f"GST ({gst_rate}%)", money(bill["gst_amount"]))

        st.divider()

        st.markdown(
            f"""
            <div class="book-card">
                <div class="book-subject">FINAL AMOUNT PAYABLE</div>
                <div class="book-price" style="font-size:32px">
                    {money(bill["grand_total"])}
                </div>
                <p>Thank you for shopping with us!</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.caption(
            "This is a demonstration receipt, not a tax-compliant invoice. "
            "No payment is collected by this website."
        )

        # CREATE A DOWNLOADABLE RECEIPT.
        receipt_lines = [
            "THE BUSINESS BOOKSHOP",
            "DEMONSTRATION RECEIPT",
            f"Date: {datetime.now().strftime('%d-%m-%Y %H:%M')}",
            f"Customer: {customer_name or 'Guest'}",
            f"Email: {customer_email or 'Not provided'}",
            "-" * 36
        ]

        for book_id, quantity in st.session_state.cart.items():
            book = get_book(book_id)

            if book:
                price = calculate_price(
                    book.get("mrp", 0),
                    book.get("discount", 0)
                )

                receipt_lines.append(
                    f"{book.get('title', 'Book')} x {quantity}"
                )
                receipt_lines.append(
                    money(price["selling_price"] * quantity)
                )

        receipt_lines.extend([
            "-" * 36,
            f"MRP: {money(bill['mrp_total'])}",
            f"Discount: -{money(bill['discount_total'])}",
            f"Subtotal: {money(bill['subtotal'])}",
            f"GST ({gst_rate}%): {money(bill['gst_amount'])}",
            f"TOTAL: {money(bill['grand_total'])}",
            "Thank you for shopping with us!"
        ])

        receipt = "\n".join(receipt_lines)

        st.download_button(
            "📄 Download your bill",
            data=receipt,
            file_name="business_bookshop_bill.txt",
            mime="text/plain",
            use_container_width=True
        )

        if st.button("Confirm demo order", use_container_width=True):
            # IF / ELSE: validate customer details.
            if not customer_name.strip():
                st.warning("Please enter your name first.")
            else:
                st.session_state.last_order = {
                    "customer": customer_name,
                    "email": customer_email,
                    "total": bill["grand_total"],
                    "date": datetime.now().strftime("%d %b %Y, %I:%M %p")
                }
                st.success("Demo order confirmed! No payment was taken.")

        if st.session_state.last_order:
            order = st.session_state.last_order
            st.info(
                f"Last confirmed demo order: {order.get('customer', 'Guest')} "
                f"— {money(order.get('total', 0))}"
            )

            st.button(
                "Start a new shopping session",
                on_click=lambda: (
                    st.session_state.cart.clear(),
                    st.session_state.update({
                        "last_order": None,
                        "page": "Home",
                        "selected_subject": "All Subjects"
                    })
                )
            )


# ====================== ABOUT PAGE ====================

elif st.session_state.page == "About Us":

    st.markdown("## About The Business Bookshop")

    st.write("""
    The Business Bookshop is a student-friendly online bookstore
    that brings academic learning resources together in one place.

    Our collection covers economics, accounting, mathematics,
    programming, business law, media studies and management.

    With searchable categories, attractive book covers, a shopping
    cart and a transparent billing calculator, our goal is to make
    learning resources easier to discover.
    """)

    a, b, c = st.columns(3)

    with a:
        st.markdown("### 📚 Learning")
        st.write("Discover academic resources.")

    with b:
        st.markdown("### 🧮 Pricing")
        st.write("View discounts and bill calculations.")

    with c:
        st.markdown("### 🌱 Growth")
        st.write("Learn something new every day.")


# ====================== FOOTER ========================

st.divider()

st.markdown("""
<div class="footer">
    <strong>The Business Bookshop</strong><br>
    Read better. Learn smarter. Grow further.<br>
    <span style="font-size:12px">
        A student project built with Python and Streamlit
    </span>
</div>
""", unsafe_allow_html=True)
