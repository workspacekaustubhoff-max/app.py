
import streamlit as st
import difflib
import io
import csv
from datetime import datetime

st.set_page_config(
    page_title="PageNest Books & Learning",
    page_icon="📚",
    layout="wide"
)

# -------------------- BOOK CATALOGUE --------------------

RAW_BOOKS = [
    # MATHEMATICS
    ("Mathematics", "NCERT Mathematics Class 11", "NCERT", 180, "class 11 maths ncert"),
    ("Mathematics", "NCERT Mathematics Class 12", "NCERT", 210, "class 12 maths ncert"),
    ("Mathematics", "RD Sharma Mathematics Class 11", "R. D. Sharma", 650, "rd sharma school maths"),
    ("Mathematics", "RD Sharma Mathematics Class 12", "R. D. Sharma", 750, "rd sharma calculus"),
    ("Mathematics", "Higher Engineering Mathematics", "B. S. Grewal", 850, "engineering maths"),
    ("Mathematics", "Advanced Engineering Mathematics", "Erwin Kreyszig", 950, "advanced engineering maths"),
    ("Mathematics", "Business Mathematics", "J. K. Sharma", 550, "business maths"),
    ("Mathematics", "Statistics for Business and Economics", "Anderson et al.", 900, "statistics data"),
    ("Mathematics", "Calculus", "James Stewart", 1100, "calculus differentiation integration"),
    ("Mathematics", "Discrete Mathematics", "Kenneth Rosen", 950, "discrete maths logic"),

    # SCIENCE
    ("Science", "NCERT Physics Class 11", "NCERT", 190, "physics class 11"),
    ("Science", "NCERT Physics Class 12", "NCERT", 220, "physics class 12"),
    ("Science", "Concepts of Physics Volume 1", "H. C. Verma", 450, "hc verma physics"),
    ("Science", "Concepts of Physics Volume 2", "H. C. Verma", 480, "hc verma physics"),
    ("Science", "NCERT Chemistry Class 11", "NCERT", 190, "chemistry class 11"),
    ("Science", "NCERT Chemistry Class 12", "NCERT", 220, "chemistry class 12"),
    ("Science", "Organic Chemistry", "Morrison and Boyd", 850, "organic chemistry"),
    ("Science", "Physical Chemistry", "P. Bahadur", 700, "physical chemistry"),
    ("Science", "Fundamentals of Biology", "NCERT", 250, "biology life science"),
    ("Science", "A Brief History of Time", "Stephen Hawking", 399, "space astronomy universe"),

    # COMMERCE
    ("Commerce", "Accountancy Class 11", "T. S. Grewal", 650, "accounts accounting"),
    ("Commerce", "Accountancy Class 12", "T. S. Grewal", 750, "accounts accounting"),
    ("Commerce", "Business Studies Class 11", "NCERT", 180, "business studies bst"),
    ("Commerce", "Business Studies Class 12", "NCERT", 220, "business studies bst"),
    ("Commerce", "Introduction to Financial Accounting", "Charles T. Horngren", 950, "financial accounts"),
    ("Commerce", "Cost Accounting", "M. N. Arora", 850, "cost accounting"),
    ("Commerce", "Corporate Accounting", "S. N. Maheshwari", 900, "corporate accounts"),
    ("Commerce", "Auditing and Assurance", "Vikas Oswal", 650, "audit"),
    ("Commerce", "Taxation", "V. K. Singhania", 950, "income tax taxation"),
    ("Commerce", "Fundamentals of Accounting", "S. N. Maheshwari", 600, "basic accounts"),

    # ECONOMICS
    ("Economics", "Principles of Microeconomics", "N. Gregory Mankiw", 750, "micro economics demand supply"),
    ("Economics", "Principles of Macroeconomics", "N. Gregory Mankiw", 750, "macro economics gdp inflation"),
    ("Economics", "Economics", "Paul A. Samuelson", 950, "economics principles"),
    ("Economics", "Intermediate Microeconomics", "Hal R. Varian", 1100, "microeconomic theory"),
    ("Economics", "Macroeconomics", "Olivier Blanchard", 1050, "macroeconomic theory"),
    ("Economics", "Indian Economy", "Ramesh Singh", 850, "indian economy upsc"),
    ("Economics", "Development Economics", "Debraj Ray", 950, "economic development"),
    ("Economics", "International Economics", "Dominick Salvatore", 900, "trade global economy"),
    ("Economics", "Public Finance", "H. L. Bhatia", 750, "government taxation budget"),
    ("Economics", "Econometrics", "Damodar Gujarati", 1000, "econometric statistics"),

    # BUSINESS AND MANAGEMENT
    ("Business & Management", "Principles of Management", "Harold Koontz", 650, "management business"),
    ("Business & Management", "Management", "Stephen P. Robbins", 950, "organizational management"),
    ("Business & Management", "Marketing Management", "Philip Kotler", 1200, "marketing"),
    ("Business & Management", "Financial Management", "I. M. Pandey", 850, "corporate finance"),
    ("Business & Management", "Human Resource Management", "Gary Dessler", 1000, "hr hrm people"),
    ("Business & Management", "Operations Management", "Heizer, Render and Munson", 950, "operations supply chain"),
    ("Business & Management", "Organizational Behaviour", "Stephen P. Robbins", 900, "organizational behavior"),
    ("Business & Management", "Business Research Methods", "Donald R. Cooper", 1000, "research methodology"),
    ("Business & Management", "Entrepreneurship", "Hisrich, Peters and Shepherd", 850, "startup innovation"),
    ("Business & Management", "Business Communication", "Meenakshi Raman", 550, "communication writing"),

    # CAT / MBA
    ("CAT / MBA Entrance", "How to Prepare for Quantitative Aptitude for CAT", "Arun Sharma", 750, "cat maths quant"),
    ("CAT / MBA Entrance", "How to Prepare for Data Interpretation for CAT", "Arun Sharma", 700, "cat di data interpretation"),
    ("CAT / MBA Entrance", "How to Prepare for Verbal Ability and Reading Comprehension", "Arun Sharma", 750, "cat verbal varc english"),
    ("CAT / MBA Entrance", "Quantitative Aptitude for Competitive Examinations", "R. S. Aggarwal", 650, "aptitude maths"),
    ("CAT / MBA Entrance", "A Modern Approach to Verbal and Non-Verbal Reasoning", "R. S. Aggarwal", 600, "reasoning"),
    ("CAT / MBA Entrance", "Logical Reasoning and Data Interpretation for CAT", "Nishit K. Sinha", 700, "cat logical reasoning"),
    ("CAT / MBA Entrance", "CAT Previous Years' Papers", "Various Authors", 450, "cat past papers"),
    ("CAT / MBA Entrance", "MBA Entrance Exam Practice Guide", "Various Authors", 500, "mba entrance mock tests"),

    # JEE
    ("JEE Entrance", "Understanding Physics", "D. C. Pandey", 650, "jee physics"),
    ("JEE Entrance", "Problems in General Physics", "I. E. Irodov", 550, "jee advanced physics problems"),
    ("JEE Entrance", "Objective Mathematics", "R. D. Sharma", 850, "jee maths"),
    ("JEE Entrance", "IIT Mathematics", "M. L. Khanna", 750, "jee mathematics"),
    ("JEE Entrance", "Organic Chemistry", "O. P. Tandon", 700, "jee organic chemistry"),
    ("JEE Entrance", "Physical Chemistry", "O. P. Tandon", 700, "jee physical chemistry"),
    ("JEE Entrance", "Concise Inorganic Chemistry", "J. D. Lee", 850, "inorganic chemistry"),
    ("JEE Entrance", "JEE Main Previous Years' Questions", "Various Authors", 500, "jee pyq past papers"),

    # NEET
    ("NEET Entrance", "Objective Biology", "Dinesh", 750, "neet biology"),
    ("NEET Entrance", "Trueman's Biology Volume 1", "M. P. Tyagi et al.", 850, "neet biology"),
    ("NEET Entrance", "Trueman's Biology Volume 2", "M. P. Tyagi et al.", 850, "neet biology"),
    ("NEET Entrance", "Objective Physics for NEET", "D. C. Pandey", 700, "neet physics"),
    ("NEET Entrance", "Objective Chemistry for NEET", "R. K. Gupta", 700, "neet chemistry"),
    ("NEET Entrance", "NCERT Biology Class 11", "NCERT", 180, "neet ncert bio"),
    ("NEET Entrance", "NCERT Biology Class 12", "NCERT", 220, "neet ncert bio"),
    ("NEET Entrance", "NEET Previous Years' Questions", "Various Authors", 500, "neet pyq past papers"),

    # UPSC
    ("UPSC / Civil Services", "Indian Polity", "M. Laxmikanth", 850, "upsc polity constitution"),
    ("UPSC / Civil Services", "A Brief History of Modern India", "Spectrum", 650, "upsc modern history"),
    ("UPSC / Civil Services", "Certificate Physical and Human Geography", "Goh Cheng Leong", 550, "upsc geography"),
    ("UPSC / Civil Services", "India's Struggle for Independence", "Bipan Chandra", 600, "indian history"),
    ("UPSC / Civil Services", "Indian Economy", "Ramesh Singh", 850, "upsc economy"),
    ("UPSC / Civil Services", "Environment", "Shankar IAS Academy", 650, "upsc ecology environment"),
    ("UPSC / Civil Services", "Oxford Student Atlas for India", "Oxford University Press", 350, "maps atlas"),
    ("UPSC / Civil Services", "General Studies Manual", "Various Authors", 900, "upsc gs prelims mains"),

    # OTHER EXAMS
    ("Other Competitive Exams", "Objective General English", "S. P. Bakshi", 550, "english grammar"),
    ("Other Competitive Exams", "Lucent's General Knowledge", "Lucent", 350, "gk general knowledge"),
    ("Other Competitive Exams", "Fast Track Objective Arithmetic", "Rajesh Verma", 550, "arithmetic maths"),
    ("Other Competitive Exams", "A Modern Approach to Verbal Reasoning", "R. S. Aggarwal", 450, "verbal reasoning"),
    ("Other Competitive Exams", "General Knowledge 2026", "Various Authors", 400, "current affairs gk"),
    ("Other Competitive Exams", "Banking Awareness", "Arihant Experts", 350, "bank po banking"),
    ("Other Competitive Exams", "SSC CGL Practice Guide", "Arihant Experts", 500, "ssc cgl"),
    ("Other Competitive Exams", "Railway Recruitment Exam Guide", "Arihant Experts", 450, "railway rrb"),
]

BOOKS = []
for i, row in enumerate(RAW_BOOKS, start=1):
    category, title, author, price, keywords = row
    BOOKS.append({
        "id": i,
        "category": category,
        "title": title,
        "author": author,
        "price": price,
        "keywords": keywords,
    })

CATEGORIES = ["All Categories"] + sorted({b["category"] for b in BOOKS})

# -------------------- SEARCH --------------------

def normalise(text):
    return " ".join(
        "".join(ch.lower() if ch.isalnum() else " " for ch in str(text)).split()
    )

def fuzzy_match(query, book):
    query = normalise(query)
    if not query:
        return 1.0

    searchable = normalise(
        book["title"] + " " + book["author"] + " "
        + book["category"] + " " + book["keywords"]
    )

    if query in searchable:
        return 1.0

    query_words = query.split()
    words = searchable.split()
    scores = []

    for qword in query_words:
        if qword in words:
            scores.append(1.0)
            continue

        matches = difflib.get_close_matches(qword, words, n=1, cutoff=0.55)
        if matches:
            scores.append(difflib.SequenceMatcher(
                None, qword, matches[0]
            ).ratio())
        else:
            scores.append(0.0)

    return sum(scores) / len(scores) if scores else 0.0

def search_books(query, books):
    if not query.strip():
        return books

    ranked = []
    for book in books:
        score = fuzzy_match(query, book)
        if score >= 0.55:
            ranked.append((score, book))

    ranked.sort(key=lambda item: (-item[0], item[1]["title"]))
    return [book for score, book in ranked]

# -------------------- SESSION STATE --------------------

if "cart" not in st.session_state:
    st.session_state.cart = {}

if "page" not in st.session_state:
    st.session_state.page = "Bookstore"

def add_to_cart(book_id):
    st.session_state.cart[book_id] = (
        st.session_state.cart.get(book_id, 0) + 1
    )

def remove_from_cart(book_id):
    st.session_state.cart.pop(book_id, None)

def money(amount):
    return f"₹{amount:,.2f}"

# -------------------- HEADER --------------------

st.title("📚 PageNest Books & Learning")
st.caption("Discover your next book. Learn something new. Grow every day.")

with st.sidebar:
    st.title("📖 PageNest")
    page = st.radio(
        "Navigate",
        ["Bookstore", "Shopping Cart", "Bundles", "Calculator", "About"]
    )

    st.divider()
    st.metric("Books in Catalogue", len(BOOKS))
    st.metric("Items in Cart", sum(st.session_state.cart.values()))

# -------------------- BOOKSTORE --------------------

if page == "Bookstore":
    st.header("Explore the Catalogue")

    search_query = st.text_input(
        "🔎 Search books",
        placeholder="Try: microeconomics, cat maths, upsc polity..."
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        selected_category = st.selectbox("Category", CATEGORIES)

    with col2:
        min_price = st.number_input(
            "Minimum price (₹)", min_value=0, value=0, step=100
        )

    with col3:
        max_price = st.number_input(
            "Maximum price (₹)", min_value=0, value=2000, step=100
        )

    if min_price > max_price:
        st.warning("Minimum price cannot be greater than maximum price.")
        filtered_books = []
    else:
        filtered_books = [
            b for b in BOOKS
            if (selected_category == "All Categories"
                or b["category"] == selected_category)
            and min_price <= b["price"] <= max_price
        ]

        filtered_books = search_books(search_query, filtered_books)

    st.write(f"**{len(filtered_books)} books found**")

    if not filtered_books:
        st.info("No books found. Try another spelling or remove a filter.")
    else:
        for start in range(0, len(filtered_books), 3):
            columns = st.columns(3)

            for col, book in zip(columns, filtered_books[start:start + 3]):
                with col:
                    with st.container(border=True):
                        st.subheader(book["title"])
                        st.caption(book["category"])
                        st.write(f"**Author/Publisher:** {book['author']}")
                        st.write(f"**Price:** {money(book['price'])}")

                        if st.button(
                            "➕ Add to Cart",
                            key=f"add_{book['id']}",
                            use_container_width=True
                        ):
                            add_to_cart(book["id"])
                            st.toast(f"Added {book['title']} to your cart!")

# -------------------- SHOPPING CART --------------------

elif page == "Shopping Cart":
    st.header("🛒 Your Shopping Cart")

    cart_items = []
    for book_id, quantity in list(st.session_state.cart.items()):
        book = next((b for b in BOOKS if b["id"] == book_id), None)
        if book:
            cart_items.append((book, quantity))

    if not cart_items:
        st.info("Your cart is empty. Visit the Bookstore to add books.")
    else:
        subtotal = 0

        for book, quantity in cart_items:
            col1, col2, col3, col4 = st.columns([4, 2, 2, 1])

            with col1:
                st.write(f"**{book['title']}**")
                st.caption(book["category"])

            with col2:
                st.write(f"{money(book['price'])} each")

            with col3:
                new_quantity = st.number_input(
                    "Quantity",
                    min_value=1,
                    max_value=99,
                    value=quantity,
                    key=f"qty_{book['id']}"
                )
                st.session_state.cart[book["id"]] = new_quantity

            with col4:
                if st.button("🗑️", key=f"remove_{book['id']}"):
                    remove_from_cart(book["id"])
                    st.rerun()

            subtotal += book["price"] * st.session_state.cart[book["id"]]

        st.divider()

        discount_rate = 0.10 if subtotal >= 2000 else 0.05 if subtotal >= 1000 else 0
        discount = subtotal * discount_rate
        taxable_amount = subtotal - discount

        # Illustrative estimate only; actual book tax treatment may differ.
        gst_rate = st.slider("Estimated GST (%)", 0, 18, 0)
        gst = taxable_amount * gst_rate / 100
        total = taxable_amount + gst

        st.subheader("Bill Summary")
        st.write(f"Subtotal: {money(subtotal)}")
        st.write(f"Discount: -{money(discount)} ({discount_rate * 100:.0f}%)")
        st.write(f"Estimated GST: {money(gst)}")
        st.markdown(f"### Total: {money(total)}")

        st.caption(
            "GST is an editable estimate, not a tax determination. "
            "Confirm applicable rates before issuing an actual invoice."
        )

        if st.button("Clear Cart", type="secondary"):
            st.session_state.cart = {}
            st.rerun()

        if st.button("Generate Receipt", type="primary"):
            receipt = io.StringIO()
            writer = csv.writer(receipt)

            writer.writerow(["PageNest Books & Learning"])
            writer.writerow(["Receipt generated", datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
            writer.writerow([])
            writer.writerow(["Book", "Author/Publisher", "Quantity", "Unit Price", "Line Total"])

            for book, quantity in cart_items:
                actual_qty = st.session_state.cart[book["id"]]
                writer.writerow([
                    book["title"], book["author"], actual_qty,
                    book["price"], book["price"] * actual_qty
                ])

            writer.writerow([])
            writer.writerow(["Subtotal", "", "", "", f"{subtotal:.2f}"])
            writer.writerow(["Discount", "", "", "", f"-{discount:.2f}"])
            writer.writerow(["Estimated GST", "", "", "", f"{gst:.2f}"])
            writer.writerow(["Total", "", "", "", f"{total:.2f}"])

            st.download_button(
                "⬇️ Download Receipt (CSV)",
                data=receipt.getvalue(),
                file_name="pagenest_receipt.csv",
                mime="text/csv",
                use_container_width=True
            )

# -------------------- BUNDLES --------------------

elif page == "Bundles":
    st.header("📦 Book Bundles")
    st.write("Curated collections for different learning goals.")

    bundles = [
        {
            "name": "Commerce Starter Bundle",
            "description": "Accountancy, Business Studies and Business Mathematics.",
            "ids": [21, 23, 27],
        },
        {
            "name": "Economics Learner Bundle",
            "description": "Microeconomics, Macroeconomics and Indian Economy.",
            "ids": [31, 32, 36],
        },
        {
            "name": "CAT Preparation Bundle",
            "description": "Quantitative Aptitude, Verbal Ability and Data Interpretation.",
            "ids": [41, 42, 43],
        },
        {
            "name": "UPSC Foundation Bundle",
            "description": "Indian Polity, Modern History and Geography.",
            "ids": [57, 58, 59],
        },
    ]

    for bundle in bundles:
        books = [b for b in BOOKS if b["id"] in bundle["ids"]]
        original_price = sum(b["price"] for b in books)
        bundle_price = round(original_price * 0.90)

        with st.container(border=True):
            st.subheader(bundle["name"])
            st.write(bundle["description"])
            for book in books:
                st.write(f"• {book['title']} — {money(book['price'])}")
            st.write(f"Regular total: ~~{money(original_price)}~~")
            st.write(f"**Bundle estimate: {money(bundle_price)}**")

            if st.button("Add Bundle to Cart", key=f"bundle_{bundle['name']}"):
                for book in books:
                    add_to_cart(book["id"])
                st.toast("Bundle books added to cart. Bundle discount is displayed as an estimate.")

    st.caption(
        "Bundle prices are estimates. The standard cart bill applies its own "
        "discount rules and does not automatically apply the displayed bundle price."
    )

# -------------------- CALCULATOR --------------------

elif page == "Calculator":
    st.header("🧮 Book Budget Calculator")

    col1, col2 = st.columns(2)

    with col1:
        book_budget = st.number_input(
            "Your budget (₹)", min_value=0, value=2000, step=100
        )

    with col2:
        estimated_book_price = st.number_input(
            "Average price per book (₹)", min_value=1, value=500, step=50
        )

    affordable = int(book_budget // estimated_book_price)

    st.metric("Books you can afford", affordable)
    st.write(
        f"You can buy approximately **{affordable} books** "
        f"at {money(estimated_book_price)} each."
    )
    st.write(f"Estimated remaining budget: {money(book_budget - affordable * estimated_book_price)}")

# -------------------- ABOUT --------------------

elif page == "About":
    st.header("About PageNest")
    st.write(
        "PageNest Books & Learning is a student-friendly bookstore concept "
        "for school, undergraduate, postgraduate and competitive-exam learning."
    )

    st.subheader("What you can explore")
    st.markdown(
        """
        - Mathematics and Science
        - Commerce and Economics
        - Business and Management
        - CAT and MBA entrance preparation
        - JEE and NEET preparation
        - UPSC and other competitive examinations
        """
    )

    st.subheader("Website features")
    st.markdown(
        """
        - Search with basic typo tolerance
        - Filter by category and price
        - Add books to a shopping cart
        - Estimate discounts and GST
        - Download a CSV receipt
        - Explore themed book bundles
        """
    )

    st.warning(
        "This is a demo bookstore. Prices and catalogue entries are illustrative, "
        "not live inventory or verified current editions. Check ISBN, edition, "
        "publisher and availability before purchasing."
    )

st.divider()
st.caption("© 2026 PageNest Books & Learning | Built with Streamlit")
