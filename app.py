
import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="PageNest Books & Learning",
    page_icon="📚",
    layout="wide"
)

# --------------------------------------------------
# BOOK DATABASE
# 10 BOOKS IN EACH OF 10 CATEGORIES
# Prices are illustrative INR prices.
# --------------------------------------------------

BOOKS = [
    # 1. MATHEMATICS
    ("NCERT Mathematics Class 11", "NCERT", "Mathematics", 250),
    ("NCERT Mathematics Class 12", "NCERT", "Mathematics", 280),
    ("Mathematics for Class 11", "R.D. Sharma", "Mathematics", 650),
    ("Mathematics for Class 12", "R.D. Sharma", "Mathematics", 700),
    ("Quantitative Aptitude", "R.S. Aggarwal", "Mathematics", 550),
    ("Higher Algebra", "Hall and Knight", "Mathematics", 600),
    ("Plane Trigonometry", "S.L. Loney", "Mathematics", 500),
    ("Problems in Calculus of One Variable", "I.A. Maron", "Mathematics", 650),
    ("Advanced Problems in Mathematics", "Vikas Gupta and Pankaj Joshi", "Mathematics", 750),
    ("Mathematical Techniques for Competitive Examinations", "Soudeep Deb and Debangan Dey", "Mathematics", 650),

    # 2. SCIENCE
    ("NCERT Science Class 10", "NCERT", "Science", 250),
    ("NCERT Physics Class 11", "NCERT", "Science", 280),
    ("NCERT Physics Class 12", "NCERT", "Science", 300),
    ("Concepts of Physics Volume 1", "H.C. Verma", "Science", 500),
    ("Concepts of Physics Volume 2", "H.C. Verma", "Science", 550),
    ("NCERT Chemistry Class 11", "NCERT", "Science", 280),
    ("NCERT Chemistry Class 12", "NCERT", "Science", 300),
    ("Concise Inorganic Chemistry", "J.D. Lee", "Science", 850),
    ("Organic Chemistry", "Morrison and Boyd", "Science", 950),
    ("Trueman's Elementary Biology", "K.N. Bhatia and M.P. Tyagi", "Science", 750),

    # 3. COMMERCE AND ACCOUNTING
    ("Financial Accounting", "S.N. Maheshwari and S.K. Maheshwari", "Commerce & Accounting", 700),
    ("Accounting Principles", "Jerry J. Weygandt and colleagues", "Commerce & Accounting", 850),
    ("Cost Accounting", "M.N. Arora", "Commerce & Accounting", 800),
    ("Management Accounting", "Khan and Jain", "Commerce & Accounting", 900),
    ("Corporate Accounting", "S.N. Maheshwari", "Commerce & Accounting", 750),
    ("Business Law", "M.C. Kuchhal", "Commerce & Accounting", 650),
    ("Company Law", "Avtar Singh", "Commerce & Accounting", 850),
    ("Financial Management", "I.M. Pandey", "Commerce & Accounting", 900),
    ("Fundamentals of Financial Management", "Eugene F. Brigham and Joel F. Houston", "Commerce & Accounting", 950),
    ("Financial Markets and Institutions", "Frederic S. Mishkin and Stanley G. Eakins", "Commerce & Accounting", 1000),

    # 4. ECONOMICS
    ("Principles of Microeconomics", "N. Gregory Mankiw", "Economics", 650),
    ("Principles of Macroeconomics", "N. Gregory Mankiw", "Economics", 650),
    ("Microeconomics", "Robert S. Pindyck and Daniel L. Rubinfeld", "Economics", 950),
    ("Macroeconomics", "Olivier Blanchard", "Economics", 900),
    ("Intermediate Microeconomics", "Hal R. Varian", "Economics", 850),
    ("Advanced Macroeconomics", "David Romer", "Economics", 1100),
    ("Managerial Economics", "Dominick Salvatore", "Economics", 800),
    ("International Economics", "Paul Krugman, Maurice Obstfeld and Marc Melitz", "Economics", 1000),
    ("The Economics of Money, Banking and Financial Markets", "Frederic S. Mishkin", "Economics", 950),
    ("Indian Economy", "Ramesh Singh", "Economics", 750),

    # 5. BUSINESS AND MANAGEMENT
    ("Principles of Management", "Harold Koontz and Heinz Weihrich", "Business & Management", 700),
    ("Management", "Stephen P. Robbins and Mary Coulter", "Business & Management", 850),
    ("Organizational Behavior", "Stephen P. Robbins and Timothy A. Judge", "Business & Management", 950),
    ("Marketing Management", "Philip Kotler and Kevin Lane Keller", "Business & Management", 1000),
    ("Principles of Marketing", "Philip Kotler and Gary Armstrong", "Business & Management", 900),
    ("Human Resource Management", "Gary Dessler", "Business & Management", 950),
    ("Operations Management", "Jay Heizer, Barry Render and Chuck Munson", "Business & Management", 1000),
    ("Strategic Management", "Fred R. David and Forest R. David", "Business & Management", 900),
    ("Entrepreneurship: Successfully Launching New Ventures", "Bruce R. Barringer and R. Duane Ireland", "Business & Management", 950),
    ("Business Communication Today", "Courtland L. Bovee and John V. Thill", "Business & Management", 800),

    # 6. CAT AND MBA ENTRANCE
    ("How to Prepare for Quantitative Aptitude for CAT", "Arun Sharma", "CAT & MBA Entrance", 850),
    ("How to Prepare for Verbal Ability and Reading Comprehension for CAT", "Arun Sharma and Meenakshi Upadhyay", "CAT & MBA Entrance", 850),
    ("How to Prepare for Data Interpretation for CAT", "Arun Sharma", "CAT & MBA Entrance", 800),
    ("How to Prepare for Logical Reasoning for CAT", "Arun Sharma", "CAT & MBA Entrance", 800),
    ("Quantitative Aptitude for CAT", "Nishit K. Sinha", "CAT & MBA Entrance", 750),
    ("Verbal Ability and Reading Comprehension for CAT", "Nishit K. Sinha", "CAT & MBA Entrance", 750),
    ("Word Power Made Easy", "Norman Lewis", "CAT & MBA Entrance", 250),
    ("A Modern Approach to Logical Reasoning", "R.S. Aggarwal", "CAT & MBA Entrance", 500),
    ("How to Prepare for the GMAT", "Official GMAT Review", "CAT & MBA Entrance", 1000),
    ("CAT Previous Years' Solved Papers", "Arihant Experts", "CAT & MBA Entrance", 450),

    # 7. JEE ENGINEERING ENTRANCE
    ("NCERT Mathematics Class 11", "NCERT", "JEE Engineering Entrance", 250),
    ("NCERT Mathematics Class 12", "NCERT", "JEE Engineering Entrance", 280),
    ("Cengage Mathematics for JEE Main and Advanced", "G. Tewani", "JEE Engineering Entrance", 950),
    ("Problems Plus in IIT Mathematics", "A. Das Gupta", "JEE Engineering Entrance", 750),
    ("Concepts of Physics Volume 1", "H.C. Verma", "JEE Engineering Entrance", 500),
    ("Concepts of Physics Volume 2", "H.C. Verma", "JEE Engineering Entrance", 550),
    ("Understanding Physics", "D.C. Pandey", "JEE Engineering Entrance", 750),
    ("Modern Approach to Chemical Calculations", "R.C. Mukherjee", "JEE Engineering Entrance", 650),
    ("Physical Chemistry", "O.P. Tandon", "JEE Engineering Entrance", 800),
    ("Advanced Problems in Organic Chemistry", "M.S. Chauhan", "JEE Engineering Entrance", 750),

    # 8. NEET MEDICAL ENTRANCE
    ("NCERT Biology Class 11", "NCERT", "NEET Medical Entrance", 280),
    ("NCERT Biology Class 12", "NCERT", "NEET Medical Entrance", 300),
    ("NCERT Physics Class 11", "NCERT", "NEET Medical Entrance", 280),
    ("NCERT Physics Class 12", "NCERT", "NEET Medical Entrance", 300),
    ("NCERT Chemistry Class 11", "NCERT", "NEET Medical Entrance", 280),
    ("NCERT Chemistry Class 12", "NCERT", "NEET Medical Entrance", 300),
    ("Objective Biology for NEET", "Dinesh", "NEET Medical Entrance", 750),
    ("Trueman's Objective Biology", "M.P. Tyagi", "NEET Medical Entrance", 700),
    ("Concepts of Physics", "H.C. Verma", "NEET Medical Entrance", 500),
    ("NEET Previous Years' Solved Papers", "Arihant Experts", "NEET Medical Entrance", 450),

    # 9. UPSC AND CIVIL SERVICES
    ("Indian Polity", "M. Laxmikanth", "UPSC & Civil Services", 850),
    ("A Brief History of Modern India", "Spectrum / Rajiv Ahir", "UPSC & Civil Services", 600),
    ("India's Struggle for Independence", "Bipan Chandra and colleagues", "UPSC & Civil Services", 700),
    ("Certificate Physical and Human Geography", "G.C. Leong", "UPSC & Civil Services", 550),
    ("Indian Economy", "Ramesh Singh", "UPSC & Civil Services", 750),
    ("Environment", "Shankar IAS Academy", "UPSC & Civil Services", 650),
    ("Introduction to the Constitution of India", "D.D. Basu", "UPSC & Civil Services", 800),
    ("Oxford Student Atlas for India", "Oxford University Press", "UPSC & Civil Services", 400),
    ("Ethics, Integrity and Aptitude", "Subba Rao and P.N. Roy Chowdhury", "UPSC & Civil Services", 650),
    ("General Studies Manual", "Arihant Experts", "UPSC & Civil Services", 750),

    # 10. OTHER COMPETITIVE EXAMS
    ("UGC NET Commerce Guide", "Arihant Experts", "Other Competitive Exams", 700),
    ("UGC NET Management Guide", "Trueman's", "Other Competitive Exams", 700),
    ("NTA CUET (UG) English", "Universities Press", "Other Competitive Exams", 450),
    ("NTA CUET (UG) General Test", "Universities Press", "Other Competitive Exams", 450),
    ("Objective General English", "S.P. Bakshi", "Other Competitive Exams", 500),
    ("Quantitative Aptitude for Competitive Examinations", "R.S. Aggarwal", "Other Competitive Exams", 550),
    ("A Modern Approach to Verbal and Non-Verbal Reasoning", "R.S. Aggarwal", "Other Competitive Exams", 600),
    ("Objective General Knowledge", "Lucent Publications", "Other Competitive Exams", 350),
    ("GRE Prep", "The Princeton Review", "Other Competitive Exams", 900),
    ("Official Guide to the TOEFL iBT Test", "ETS", "Other Competitive Exams", 1000),
]

df = pd.DataFrame(
    BOOKS,
    columns=["Book", "Author / Publisher", "Category", "Price"]
)

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "cart" not in st.session_state:
    st.session_state.cart = {}

if "customer" not in st.session_state:
    st.session_state.customer = ""

# --------------------------------------------------
# HEADER AND STYLING
# --------------------------------------------------

st.markdown("""
<style>
.main-title {
    font-size: 42px;
    font-weight: 800;
    text-align: center;
}
.subtitle {
    text-align: center;
    font-size: 17px;
}
</style>
""", unsafe_allow_html=True)

st.markdown(
    '<div class="main-title">📚 PageNest Books & Learning</div>',
    unsafe_allow_html=True
)
st.markdown(
    '<div class="subtitle">Find the right book for every subject and exam.</div>',
    unsafe_allow_html=True
)

st.divider()

# --------------------------------------------------
# SIDEBAR NAVIGATION
# --------------------------------------------------

page = st.sidebar.radio(
    "Navigation",
    [
        "Book Catalogue",
        "Shopping Cart",
        "Book Bundles",
        "Business Calculator",
        "About Us"
    ]
)

st.sidebar.metric("Total Book Entries", len(df))
st.sidebar.metric("Categories", df["Category"].nunique())
st.sidebar.metric(
    "Items in Cart",
    sum(item["quantity"] for item in st.session_state.cart.values())
)

# --------------------------------------------------
# HELPER FUNCTIONS
# --------------------------------------------------

def add_to_cart(book, author, price):
    if book in st.session_state.cart:
        st.session_state.cart[book]["quantity"] += 1
    else:
        st.session_state.cart[book] = {
            "author": author,
            "price": float(price),
            "quantity": 1
        }


def calculate_subtotal():
    return sum(
        item["price"] * item["quantity"]
        for item in st.session_state.cart.values()
    )


# --------------------------------------------------
# BOOK CATALOGUE
# --------------------------------------------------

if page == "Book Catalogue":

    st.header("Explore the Book Catalogue")

    st.write(
        "Choose a subject or examination category. Each category "
        "contains 10 book entries."
    )

    category_counts = df.groupby("Category").size().reset_index(
        name="Books"
    )
    st.dataframe(category_counts, use_container_width=True, hide_index=True)

    col1, col2 = st.columns([2, 1])

    with col1:
        search = st.text_input(
            "Search books or authors",
            placeholder="Try 'Mankiw', 'Physics', 'CAT'..."
        )

    with col2:
        category_options = ["All Categories"] + sorted(
            df["Category"].unique().tolist()
        )
        selected_category = st.selectbox(
            "Select category",
            category_options
        )

    max_price = st.slider(
        "Maximum book price (₹)",
        min_value=0,
        max_value=2000,
        value=2000,
        step=50
    )

    results = df.copy()

    if selected_category != "All Categories":
        results = results[results["Category"] == selected_category]

    if search:
        mask = (
            results["Book"].str.contains(search, case=False, na=False)
            | results["Author / Publisher"].str.contains(
                search, case=False, na=False
            )
            | results["Category"].str.contains(search, case=False, na=False)
        )
        results = results[mask]

    results = results[results["Price"] <= max_price]

    sort_choice = st.selectbox(
        "Sort results",
        ["Book name", "Price: Low to High", "Price: High to Low"]
    )

    if sort_choice == "Price: Low to High":
        results = results.sort_values("Price")
    elif sort_choice == "Price: High to Low":
        results = results.sort_values("Price", ascending=False)
    else:
        results = results.sort_values("Book")

    st.write(f"**{len(results)} books found**")

    for _, book in results.iterrows():
        with st.container(border=True):
            left, middle, right = st.columns([5, 2, 1])

            with left:
                st.markdown(f"**{book['Book']}**")
                st.caption(
                    f"Author/Publisher: {book['Author / Publisher']}"
                )
                st.caption(f"Category: {book['Category']}")

            with middle:
                st.markdown(f"### ₹{book['Price']:.0f}")

            with right:
                if st.button("Add", key=f"add_{book.name}"):
                    add_to_cart(
                        book["Book"],
                        book["Author / Publisher"],
                        book["Price"]
                    )
                    st.toast(f"Added: {book['Book']}")

    st.caption(
        "Titles, author details and prices are catalogue suggestions. "
        "Verify exact editions, ISBNs and current prices before purchase."
    )

# --------------------------------------------------
# SHOPPING CART AND BILLING
# --------------------------------------------------

elif page == "Shopping Cart":

    st.header("Shopping Cart")

    st.session_state.customer = st.text_input(
        "Customer name",
        value=st.session_state.customer
    )

    if not st.session_state.cart:
        st.info("Your cart is empty. Add books from the catalogue.")

    else:
        for book, item in list(st.session_state.cart.items()):
            with st.container(border=True):
                col1, col2, col3, col4 = st.columns([4, 2, 2, 1])

                with col1:
                    st.write(f"**{book}**")
                    st.caption(item["author"])

                with col2:
                    st.write(f"₹{item['price']:.2f} each")

                with col3:
                    quantity = st.number_input(
                        "Quantity",
                        min_value=1,
                        max_value=99,
                        value=item["quantity"],
                        key=f"quantity_{book}"
                    )
                    st.session_state.cart[book]["quantity"] = quantity

                with col4:
                    if st.button("Remove", key=f"remove_{book}"):
                        del st.session_state.cart[book]
                        st.rerun()

        st.divider()

        subtotal = calculate_subtotal()

        col1, col2 = st.columns(2)

        with col1:
            discount_percent = st.number_input(
                "Discount (%)",
                min_value=0.0,
                max_value=100.0,
                value=0.0
            )

        with col2:
            gst_percent = st.number_input(
                "Estimated GST (%)",
                min_value=0.0,
                max_value=100.0,
                value=0.0
            )

        discount = subtotal * discount_percent / 100
        taxable = subtotal - discount
        gst = taxable * gst_percent / 100
        total = taxable + gst

        st.subheader("Bill Summary")

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Subtotal", f"₹{subtotal:,.2f}")
        c2.metric("Discount", f"₹{discount:,.2f}")
        c3.metric("Estimated GST", f"₹{gst:,.2f}")
        c4.metric("Total", f"₹{total:,.2f}")

        receipt = [
            "PAGENEST BOOKS & LEARNING",
            "=" * 40,
            f"Date: {datetime.now().strftime('%d-%m-%Y %H:%M')}",
            f"Customer: {st.session_state.customer or 'Walk-in Customer'}",
            "-" * 40
        ]

        for book, item in st.session_state.cart.items():
            line_total = item["price"] * item["quantity"]
            receipt.append(
                f"{book} | Qty: {item['quantity']} | "
                f"₹{line_total:.2f}"
            )

        receipt.extend([
            "-" * 40,
            f"Subtotal: ₹{subtotal:.2f}",
            f"Discount: ₹{discount:.2f}",
            f"Estimated GST: ₹{gst:.2f}",
            f"Total: ₹{total:.2f}",
            "=" * 40,
            "Thank you for shopping at PageNest!"
        ])

        receipt_text = "\n".join(receipt)

        st.download_button(
            "Download Receipt",
            data=receipt_text,
            file_name="pagenest_receipt.txt",
            mime="text/plain"
        )

        if st.button("Clear Cart"):
            st.session_state.cart = {}
            st.rerun()

        st.caption(
            "GST is an estimate. Confirm the applicable rate before "
            "using this calculation for an actual sale."
        )

# --------------------------------------------------
# BOOK BUNDLES
# --------------------------------------------------

elif page == "Book Bundles":

    st.header("Study Bundles")

    bundles = {
        "School Mathematics": [
            "NCERT Mathematics Class 11",
            "NCERT Mathematics Class 12",
            "Quantitative Aptitude"
        ],
        "Science Foundation": [
            "NCERT Science Class 10",
            "NCERT Physics Class 11",
            "NCERT Chemistry Class 11"
        ],
        "Commerce Starter": [
            "Financial Accounting",
            "Business Law",
            "Financial Management"
        ],
        "Economics Starter": [
            "Principles of Microeconomics",
            "Principles of Macroeconomics",
            "Indian Economy"
        ],
        "CAT Preparation": [
            "How to Prepare for Quantitative Aptitude for CAT",
            "How to Prepare for Verbal Ability and Reading Comprehension for CAT",
            "How to Prepare for Data Interpretation for CAT"
        ],
        "UPSC Foundation": [
            "Indian Polity",
            "A Brief History of Modern India",
            "Indian Economy"
        ]
    }

    for bundle_name, titles in bundles.items():
        bundle_df = df[df["Book"].isin(titles)]

        # Use the first matching entry for each selected title.
        bundle_df = bundle_df.drop_duplicates(subset=["Book"])
        subtotal = bundle_df["Price"].sum()
        bundle_price = subtotal * 0.90

        with st.container(border=True):
            st.subheader(bundle_name)

            for _, row in bundle_df.iterrows():
                st.write(
                    f"• {row['Book']} — ₹{row['Price']:.0f}"
                )

            st.write(f"Regular total: ₹{subtotal:.0f}")
            st.markdown(f"**Illustrative bundle price: ₹{bundle_price:.0f}**")

            if st.button("Add Bundle", key=f"bundle_{bundle_name}"):
                for _, row in bundle_df.iterrows():
                    add_to_cart(
                        row["Book"],
                        row["Author / Publisher"],
                        row["Price"]
                    )
                st.toast(f"Added {bundle_name} to cart.")

    st.caption("Bundle prices show a sample 10% discount.")

# --------------------------------------------------
# BUSINESS CALCULATOR
# --------------------------------------------------

elif page == "Business Calculator":

    st.header("Business Calculator")

    mode = st.selectbox(
        "Select calculator",
        [
            "Basic Calculator",
            "Discount Calculator",
            "GST Calculator",
            "Profit Margin Calculator"
        ]
    )

    if mode == "Basic Calculator":

        a = st.number_input("First number", value=0.0)
        b = st.number_input("Second number", value=0.0)

        operation = st.selectbox(
            "Operation",
            ["Add", "Subtract", "Multiply", "Divide"]
        )

        if st.button("Calculate"):
            if operation == "Add":
                st.success(f"Result: {a + b:.2f}")
            elif operation == "Subtract":
                st.success(f"Result: {a - b:.2f}")
            elif operation == "Multiply":
                st.success(f"Result: {a * b:.2f}")
            elif operation == "Divide":
                if b == 0:
                    st.error("Cannot divide by zero.")
                else:
                    st.success(f"Result: {a / b:.2f}")

    elif mode == "Discount Calculator":

        price = st.number_input(
            "Original price (₹)", min_value=0.0, value=1000.0
        )
        discount = st.number_input(
            "Discount (%)", min_value=0.0, max_value=100.0, value=10.0
        )

        saving = price * discount / 100
        st.metric("You save", f"₹{saving:.2f}")
        st.metric("Final price", f"₹{price - saving:.2f}")

    elif mode == "GST Calculator":

        amount = st.number_input(
            "Price before GST (₹)", min_value=0.0, value=1000.0
        )
        rate = st.number_input(
            "GST (%)", min_value=0.0, max_value=100.0, value=18.0
        )

        tax = amount * rate / 100
        st.metric("GST amount", f"₹{tax:.2f}")
        st.metric("Total price", f"₹{amount + tax:.2f}")

    elif mode == "Profit Margin Calculator":

        cost = st.number_input(
            "Cost price (₹)", min_value=0.0, value=500.0
        )
        selling = st.number_input(
            "Selling price (₹)", min_value=0.0, value=700.0
        )

        profit = selling - cost
        margin = profit / selling * 100 if selling else 0

        st.metric("Profit / Loss", f"₹{profit:.2f}")
        st.metric("Profit margin", f"{margin:.2f}%")

# --------------------------------------------------
# ABOUT US
# --------------------------------------------------

elif page == "About Us":

    st.header("About PageNest Books & Learning")

    st.write("""
    PageNest is a text-based bookstore catalogue designed for learners,
    students and competitive-exam candidates.

    Our categories cover:
    - Mathematics
    - Science
    - Commerce and accounting
    - Economics
    - Business and management
    - CAT and MBA entrance
    - JEE engineering entrance
    - NEET medical entrance
    - UPSC and civil services
    - Other competitive examinations
    """)

    st.subheader("Catalogue Overview")

    overview = (
        df.groupby("Category")
        .agg(
            Number_of_Books=("Book", "count"),
            Lowest_Price=("Price", "min"),
            Highest_Price=("Price", "max")
        )
        .reset_index()
    )

    st.dataframe(overview, use_container_width=True, hide_index=True)

    st.caption(
        "This is a demonstration catalogue. Confirm editions, publishers, "
        "ISBNs and prices before listing books for sale."
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
