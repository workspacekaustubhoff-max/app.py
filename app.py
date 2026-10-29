
import streamlit as st
import pandas as pd
from datetime import datetime
from io import BytesIO

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="PageNest Books & Learning",
    page_icon="📚",
    layout="wide"
)

# --------------------------------------------------
# CUSTOM STYLING - TEXT ONLY, NO IMAGES
# --------------------------------------------------

st.markdown("""
<style>
    .main-title {
        font-size: 42px;
        font-weight: 800;
        text-align: center;
        margin-bottom: 0;
    }
    .subtitle {
        text-align: center;
        font-size: 17px;
        margin-bottom: 25px;
    }
    .book-label {
        padding: 12px;
        border: 1px solid #d9d9d9;
        border-radius: 10px;
        margin-bottom: 8px;
    }
    .price {
        font-weight: bold;
        font-size: 18px;
    }
    div.stButton > button {
        width: 100%;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# BOOK DATABASE: 100 BOOKS
# --------------------------------------------------

BOOKS = [
    # MICROECONOMICS
    ("Principles of Microeconomics", "Microeconomics", 650),
    ("Microeconomics", "Microeconomics", 750),
    ("Intermediate Microeconomics", "Microeconomics", 950),
    ("Microeconomic Theory", "Microeconomics", 1100),
    ("Advanced Microeconomic Theory", "Microeconomics", 1250),
    ("Managerial Economics", "Microeconomics", 700),
    ("Game Theory for Applied Economists", "Microeconomics", 850),
    ("Microeconomics: Theory and Applications", "Microeconomics", 800),

    # MACROECONOMICS
    ("Principles of Macroeconomics", "Macroeconomics", 650),
    ("Macroeconomics", "Macroeconomics", 750),
    ("Macroeconomics: A European Perspective", "Macroeconomics", 950),
    ("Advanced Macroeconomics", "Macroeconomics", 1200),
    ("Macroeconomics: Policy and Practice", "Macroeconomics", 900),
    ("Monetary Theory and Policy", "Macroeconomics", 1050),
    ("International Economics", "Macroeconomics", 850),
    ("The Economics of Money, Banking and Financial Markets", "Macroeconomics", 1000),

    # BUSINESS STUDIES
    ("Business Studies", "Business Studies", 500),
    ("Business Environment", "Business Studies", 650),
    ("Business Organisation and Management", "Business Studies", 600),
    ("Business Policy and Strategic Management", "Business Studies", 900),
    ("International Business", "Business Studies", 800),
    ("Entrepreneurship: Successfully Launching New Ventures", "Business Studies", 950),
    ("Business Communication Today", "Business Studies", 850),
    ("Essentials of Business", "Business Studies", 700),

    # PRINCIPLES OF MANAGEMENT
    ("Principles of Management", "Principles of Management", 650),
    ("Management", "Principles of Management", 850),
    ("Fundamentals of Management", "Principles of Management", 750),
    ("Organizational Behavior", "Principles of Management", 900),
    ("Management: A Practical Introduction", "Principles of Management", 800),
    ("Human Resource Management", "Principles of Management", 950),
    ("Operations Management", "Principles of Management", 1000),
    ("Strategic Management", "Principles of Management", 1050),

    # LEGAL ASPECTS OF BUSINESS
    ("Business Law", "Legal Aspects of Business", 700),
    ("Legal Aspects of Business", "Legal Aspects of Business", 650),
    ("Business and Corporate Laws", "Legal Aspects of Business", 800),
    ("Company Law", "Legal Aspects of Business", 950),
    ("The Legal Environment of Business", "Legal Aspects of Business", 900),
    ("Corporate Governance", "Legal Aspects of Business", 850),
    ("Intellectual Property Rights", "Legal Aspects of Business", 750),
    ("Law of Contract", "Legal Aspects of Business", 800),

    # FINANCIAL ACCOUNTING
    ("Financial Accounting", "Financial Accounting", 700),
    ("Accounting Principles", "Financial Accounting", 650),
    ("Financial Accounting: An Introduction", "Financial Accounting", 750),
    ("Introduction to Financial Accounting", "Financial Accounting", 850),
    ("Cost Accounting", "Financial Accounting", 800),
    ("Management Accounting", "Financial Accounting", 900),
    ("Accounting for Managers", "Financial Accounting", 850),
    ("Corporate Accounting", "Financial Accounting", 950),

    # BUSINESS MATHEMATICS AND STATISTICS
    ("Business Mathematics", "Business Mathematics", 600),
    ("Mathematics for Business and Economics", "Business Mathematics", 750),
    ("Business Mathematics and Statistics", "Business Mathematics", 700),
    ("Quantitative Methods for Business", "Business Mathematics", 850),
    ("Business Statistics", "Business Mathematics", 650),
    ("Statistics for Business and Economics", "Business Mathematics", 900),
    ("Fundamentals of Business Statistics", "Business Mathematics", 700),
    ("Applied Mathematics for Business", "Business Mathematics", 800),

    # VERBAL, WRITTEN AND COMMUNICATION
    ("Verbal Ability and Reading Comprehension", "Communication Skills", 550),
    ("Word Power Made Easy", "Communication Skills", 250),
    ("High School English Grammar and Composition", "Communication Skills", 350),
    ("Business Communication", "Communication Skills", 600),
    ("Written Communication", "Communication Skills", 650),
    ("Technical Communication", "Communication Skills", 750),
    ("The Elements of Style", "Communication Skills", 400),
    ("English Vocabulary in Use", "Communication Skills", 600),

    # TECHNOLOGY, EXCEL, PYTHON AND DIGITAL BUSINESS
    ("Excel 365 Bible", "Technology and Analytics", 950),
    ("Microsoft Excel Step by Step", "Technology and Analytics", 800),
    ("Excel Formulas and Functions", "Technology and Analytics", 700),
    ("Python Crash Course", "Technology and Analytics", 850),
    ("Automate the Boring Stuff with Python", "Technology and Analytics", 900),
    ("Learning Python", "Technology and Analytics", 1200),
    ("Python for Data Analysis", "Technology and Analytics", 1000),
    ("Data Science from Scratch", "Technology and Analytics", 950),
    ("Business Analytics", "Technology and Analytics", 900),
    ("Data Analytics for Business", "Technology and Analytics", 850),
    ("Digital Transformation", "Technology and Analytics", 950),
    ("Competing in the Age of AI", "Technology and Analytics", 800),

    # MEDIA, SOCIETY, RESEARCH AND COMPETITIVE EXAMS
    ("Media and Society", "Media and Society", 650),
    ("Media, Culture and Society", "Media and Society", 850),
    ("Media and Communication Research Methods", "Media and Society", 900),
    ("Mass Communication Theory", "Media and Society", 800),
    ("The Sociological Imagination", "Media and Society", 700),
    ("Research Methodology", "Research and Competitive Exams", 750),
    ("Research Design", "Research and Competitive Exams", 900),
    ("The Craft of Research", "Research and Competitive Exams", 800),
    ("How to Write and Publish a Scientific Paper", "Research and Competitive Exams", 850),
    ("Publication Manual of the APA", "Research and Competitive Exams", 1200),
    ("Quantitative Research Methods", "Research and Competitive Exams", 950),
    ("Qualitative Research Methods", "Research and Competitive Exams", 900),
    ("UGC NET Commerce Guide", "Research and Competitive Exams", 700),
    ("UGC NET Management Guide", "Research and Competitive Exams", 700),
    ("CAT Quantitative Aptitude", "Research and Competitive Exams", 650),
    ("CAT Verbal Ability and Reading Comprehension", "Research and Competitive Exams", 650),
    ("GMAT Official Guide", "Research and Competitive Exams", 1100),
    ("GRE General Test Preparation", "Research and Competitive Exams", 950),
    ("CFA Program Curriculum", "Research and Competitive Exams", 1500),
    ("Financial Markets and Institutions", "Research and Competitive Exams", 900),
    ("Investment Analysis and Portfolio Management", "Research and Competitive Exams", 1000),
    ("Corporate Finance", "Research and Competitive Exams", 950),
    ("International Financial Management", "Research and Competitive Exams", 1050),
    ("Principles of Marketing", "Research and Competitive Exams", 750),
    ("Marketing Management", "Research and Competitive Exams", 950),
    ("Consumer Behavior", "Research and Competitive Exams", 850),
    ("Supply Chain Management", "Research and Competitive Exams", 900),
    ("Project Management", "Research and Competitive Exams", 850),
]

book_df = pd.DataFrame(
    BOOKS,
    columns=["Book Name", "Category", "Price"]
)

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "cart" not in st.session_state:
    st.session_state.cart = {}

if "customer_name" not in st.session_state:
    st.session_state.customer_name = ""

# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.markdown(
    '<div class="main-title">📚 PageNest Books & Learning</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Your destination for commerce, business, '
    'economics, technology and competitive exam books.</div>',
    unsafe_allow_html=True
)

st.divider()

# --------------------------------------------------
# NAVIGATION
# --------------------------------------------------

page = st.sidebar.radio(
    "Navigate",
    [
        "Book Catalogue",
        "Shopping Cart & Billing",
        "Book Bundles",
        "Business Calculator",
        "About PageNest"
    ]
)

st.sidebar.divider()
st.sidebar.metric("Books in Catalogue", len(book_df))
st.sidebar.metric("Different Categories", book_df["Category"].nunique())

# --------------------------------------------------
# HELPER FUNCTIONS
# --------------------------------------------------

def add_to_cart(book_name, price):
    if book_name in st.session_state.cart:
        st.session_state.cart[book_name]["quantity"] += 1
    else:
        st.session_state.cart[book_name] = {
            "price": float(price),
            "quantity": 1
        }


def cart_subtotal():
    return sum(
        item["price"] * item["quantity"]
        for item in st.session_state.cart.values()
    )


def make_receipt(customer, items, discount_rate, gst_rate):
    subtotal = sum(
        item["price"] * item["quantity"]
        for item in items.values()
    )
    discount = subtotal * discount_rate
    taxable_amount = subtotal - discount
    gst = taxable_amount * gst_rate
    total = taxable_amount + gst

    lines = [
        "PAGENEST BOOKS & LEARNING",
        "=" * 36,
        f"Receipt date: {datetime.now().strftime('%d-%m-%Y %H:%M')}",
        f"Customer: {customer or 'Walk-in Customer'}",
        "-" * 36,
        "ITEMS:"
    ]

    for name, item in items.items():
        line_total = item["price"] * item["quantity"]
        lines.append(
            f"{name} | Qty: {item['quantity']} | "
            f"Rs. {line_total:.2f}"
        )

    lines.extend([
        "-" * 36,
        f"Subtotal: Rs. {subtotal:.2f}",
        f"Discount: Rs. {discount:.2f}",
        f"GST estimate: Rs. {gst:.2f}",
        f"TOTAL: Rs. {total:.2f}",
        "=" * 36,
        "Thank you for shopping with PageNest!"
    ])

    return "\n".join(lines)


# --------------------------------------------------
# PAGE 1: BOOK CATALOGUE
# --------------------------------------------------

if page == "Book Catalogue":

    st.header("Book Catalogue")
    st.write(
        "Search for books by title or filter by category and price. "
        "All books are displayed as text labels."
    )

    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        search_term = st.text_input(
            "Search by book name",
            placeholder="e.g. Microeconomics, Excel, Python..."
        )

    with col2:
        categories = ["All Categories"] + sorted(
            book_df["Category"].unique().tolist()
        )
        selected_category = st.selectbox(
            "Category",
            categories
        )

    with col3:
        max_price = st.number_input(
            "Maximum price (₹)",
            min_value=0,
            max_value=100000,
            value=2000,
            step=100
        )

    filtered_df = book_df.copy()

    if search_term:
        filtered_df = filtered_df[
            filtered_df["Book Name"].str.contains(
                search_term,
                case=False,
                na=False
            )
        ]

    if selected_category != "All Categories":
        filtered_df = filtered_df[
            filtered_df["Category"] == selected_category
        ]

    filtered_df = filtered_df[
        filtered_df["Price"] <= max_price
    ]

    st.write(f"**{len(filtered_df)} books found**")

    sort_option = st.selectbox(
        "Sort books",
        ["Name: A to Z", "Price: Low to High", "Price: High to Low"]
    )

    if sort_option == "Name: A to Z":
        filtered_df = filtered_df.sort_values("Book Name")
    elif sort_option == "Price: Low to High":
        filtered_df = filtered_df.sort_values("Price")
    else:
        filtered_df = filtered_df.sort_values(
            "Price",
            ascending=False
        )

    if filtered_df.empty:
        st.warning("No books match your search. Try different filters.")
    else:
        for _, book in filtered_df.iterrows():
            with st.container(border=True):
                col1, col2, col3 = st.columns([5, 2, 1])

                with col1:
                    st.markdown(f"**{book['Book Name']}**")
                    st.caption(book["Category"])

                with col2:
                    st.markdown(
                        f"<div class='price'>₹{book['Price']:.2f}</div>",
                        unsafe_allow_html=True
                    )

                with col3:
                    if st.button(
                        "Add",
                        key=f"add_{book['Book Name']}"
                    ):
                        add_to_cart(
                            book["Book Name"],
                            book["Price"]
                        )
                        st.toast(
                            f"Added {book['Book Name']} to your cart!"
                        )

    st.divider()
    st.caption(
        "Prices are illustrative catalogue prices, not verified current "
        "market prices. Check the edition, ISBN and availability before "
        "purchasing."
    )

# --------------------------------------------------
# PAGE 2: CART AND BILLING
# --------------------------------------------------

elif page == "Shopping Cart & Billing":

    st.header("Shopping Cart & Billing")

    st.session_state.customer_name = st.text_input(
        "Customer name",
        value=st.session_state.customer_name
    )

    if not st.session_state.cart:
        st.info(
            "Your cart is empty. Open Book Catalogue to add books."
        )

    else:
        cart_rows = []

        for name, item in st.session_state.cart.items():
            cart_rows.append({
                "Book Name": name,
                "Unit Price (₹)": item["price"],
                "Quantity": item["quantity"],
                "Total (₹)": item["price"] * item["quantity"]
            })

        cart_df = pd.DataFrame(cart_rows)
        st.dataframe(
            cart_df,
            use_container_width=True,
            hide_index=True
        )

        st.subheader("Update quantities")

        for name, item in list(st.session_state.cart.items()):
            col1, col2, col3 = st.columns([5, 2, 2])

            with col1:
                st.write(name)

            with col2:
                new_quantity = st.number_input(
                    "Quantity",
                    min_value=1,
                    max_value=99,
                    value=item["quantity"],
                    key=f"qty_{name}"
                )

                st.session_state.cart[name]["quantity"] = new_quantity

            with col3:
                if st.button("Remove", key=f"remove_{name}"):
                    del st.session_state.cart[name]
                    st.rerun()

        st.divider()

        subtotal = cart_subtotal()

        col1, col2 = st.columns(2)

        with col1:
            discount_percent = st.number_input(
                "Discount (%)",
                min_value=0.0,
                max_value=100.0,
                value=0.0,
                step=1.0
            )

        with col2:
            gst_percent = st.number_input(
                "Estimated GST (%)",
                min_value=0.0,
                max_value=100.0,
                value=0.0,
                step=1.0
            )

        discount = subtotal * discount_percent / 100
        taxable_amount = subtotal - discount
        gst = taxable_amount * gst_percent / 100
        total = taxable_amount + gst

        st.subheader("Bill Summary")

        c1, c2, c3, c4 = st.columns(4)

        c1.metric("Subtotal", f"₹{subtotal:,.2f}")
        c2.metric("Discount", f"₹{discount:,.2f}")
        c3.metric("Estimated GST", f"₹{gst:,.2f}")
        c4.metric("Final Total", f"₹{total:,.2f}")

        st.caption(
            "GST is an estimate controlled by you. Confirm the applicable "
            "tax treatment and rate before using this as a real invoice."
        )

        receipt = make_receipt(
            st.session_state.customer_name,
            st.session_state.cart,
            discount_percent / 100,
            gst_percent / 100
        )

        st.download_button(
            "Download Receipt (.txt)",
            data=receipt,
            file_name="pagenest_receipt.txt",
            mime="text/plain"
        )

        if st.button("Clear Entire Cart"):
            st.session_state.cart = {}
            st.rerun()

# --------------------------------------------------
# PAGE 3: BOOK BUNDLES
# --------------------------------------------------

elif page == "Book Bundles":

    st.header("Curated Book Bundles")
    st.write("Explore suggested reading bundles for students and learners.")

    bundles = {
        "Economics Starter Bundle": [
            "Principles of Microeconomics",
            "Principles of Macroeconomics",
            "Managerial Economics"
        ],
        "Business Management Bundle": [
            "Principles of Management",
            "Organizational Behavior",
            "Strategic Management"
        ],
        "Accounting and Finance Bundle": [
            "Financial Accounting",
            "Management Accounting",
            "Corporate Finance"
        ],
        "Excel and Python Bundle": [
            "Microsoft Excel Step by Step",
            "Python Crash Course",
            "Python for Data Analysis"
        ],
        "Research Skills Bundle": [
            "Research Methodology",
            "The Craft of Research",
            "How to Write and Publish a Scientific Paper"
        ],
        "Competitive Exam Bundle": [
            "UGC NET Commerce Guide",
            "CAT Quantitative Aptitude",
            "CAT Verbal Ability and Reading Comprehension"
        ]
    }

    for bundle_name, titles in bundles.items():
        available_titles = book_df[
            book_df["Book Name"].isin(titles)
        ]

        bundle_price = available_titles["Price"].sum()
        bundle_discount = bundle_price * 0.10
        final_price = bundle_price - bundle_discount

        with st.container(border=True):
            st.subheader(bundle_name)

            for _, row in available_titles.iterrows():
                st.write(
                    f"• {row['Book Name']} — ₹{row['Price']:.2f}"
                )

            st.write(f"Regular total: ₹{bundle_price:.2f}")
            st.write("Bundle discount: 10%")
            st.markdown(f"**Bundle price: ₹{final_price:.2f}**")

            if st.button(
                "Add Bundle to Cart",
                key=f"bundle_{bundle_name}"
            ):
                for _, row in available_titles.iterrows():
                    add_to_cart(row["Book Name"], row["Price"])

                st.toast(
                    f"{bundle_name} books added to your cart."
                )

    st.caption(
        "Bundle discounts are illustrative. The cart bill applies any "
        "additional discount you choose."
    )

# --------------------------------------------------
# PAGE 4: BUSINESS CALCULATOR
# --------------------------------------------------

elif page == "Business Calculator":

    st.header("Business Calculator")
    st.write(
        "Calculate totals, discounts, taxes and profit margins."
    )

    calculation_type = st.selectbox(
        "Choose calculation",
        [
            "Basic Calculator",
            "Discount Calculator",
            "GST Calculator",
            "Profit Margin Calculator"
        ]
    )

    if calculation_type == "Basic Calculator":

        col1, col2 = st.columns(2)

        with col1:
            a = st.number_input("First number", value=0.0)

        with col2:
            b = st.number_input("Second number", value=0.0)

        operation = st.selectbox(
            "Operation",
            ["Add", "Subtract", "Multiply", "Divide"]
        )

        if st.button("Calculate"):
            if operation == "Add":
                result = a + b
                st.success(f"Result: {result:.2f}")
            elif operation == "Subtract":
                result = a - b
                st.success(f"Result: {result:.2f}")
            elif operation == "Multiply":
                result = a * b
                st.success(f"Result: {result:.2f}")
            elif operation == "Divide":
                if b == 0:
                    st.error("Cannot divide by zero.")
                else:
                    st.success(f"Result: {a / b:.2f}")

    elif calculation_type == "Discount Calculator":

        price = st.number_input(
            "Original price (₹)",
            min_value=0.0,
            value=1000.0
        )

        discount_rate = st.number_input(
            "Discount (%)",
            min_value=0.0,
            max_value=100.0,
            value=10.0
        )

        discount_amount = price * discount_rate / 100
        final_price = price - discount_amount

        st.metric("Discount amount", f"₹{discount_amount:.2f}")
        st.metric("Price after discount", f"₹{final_price:.2f}")

    elif calculation_type == "GST Calculator":

        amount = st.number_input(
            "Amount before GST (₹)",
            min_value=0.0,
            value=1000.0
        )

        tax_rate = st.number_input(
            "GST rate (%)",
            min_value=0.0,
            max_value=100.0,
            value=18.0
        )

        tax_amount = amount * tax_rate / 100

        st.metric("GST amount", f"₹{tax_amount:.2f}")
        st.metric("Total including GST", f"₹{amount + tax_amount:.2f}")

    elif calculation_type == "Profit Margin Calculator":

        cost = st.number_input(
            "Cost price (₹)",
            min_value=0.0,
            value=500.0
        )

        selling_price = st.number_input(
            "Selling price (₹)",
            min_value=0.0,
            value=700.0
        )

        profit = selling_price - cost
        margin = (
            profit / selling_price * 100
            if selling_price > 0 else 0
        )

        st.metric("Profit / Loss", f"₹{profit:.2f}")
        st.metric("Profit margin", f"{margin:.2f}%")

# --------------------------------------------------
# PAGE 5: ABOUT
# --------------------------------------------------

elif page == "About PageNest":

    st.header("About PageNest Books & Learning")

    st.write("""
    PageNest Books & Learning is a text-based bookstore catalogue concept
    designed for commerce, management, economics, finance, technology,
    research and competitive examination books.

    The website helps users:
    - Browse books by category.
    - Search titles and filter by price.
    - Add books to a shopping cart.
    - Calculate discounts and estimated taxes.
    - Explore curated study bundles.
    - Generate and download a basic receipt.
    - Use simple business calculators.
    """)

    st.subheader("Subjects Covered")

    subject_list = sorted(book_df["Category"].unique().tolist())

    for subject in subject_list:
        st.write(f"• {subject}")

    st.subheader("Catalogue Information")

    st.write(f"Total book entries: {len(book_df)}")
    st.write(f"Categories: {book_df['Category'].nunique()}")

    st.caption(
        "This is a demonstration bookstore. Book titles and prices should "
        "be checked against publishers, editions, ISBNs and sellers before "
        "being used for actual sales."
    )

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.markdown(
    "<center>📚 PageNest Books & Learning | "
    "Learn • Explore • Grow</center>",
    unsafe_allow_html=True
)
