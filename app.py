
import re
from datetime import datetime

import pandas as pd
import streamlit as st
from rapidfuzz import fuzz, process

# ============================================================
# PAGENEST BOOKS & LEARNING
# Text-only bookstore with fuzzy search and shopping cart
# ============================================================

st.set_page_config(
    page_title="PageNest Books & Learning",
    page_icon="📚",
    layout="wide",
)

st.markdown("""
<style>
.main-title {
    font-size: 40px;
    font-weight: 800;
    text-align: center;
}
.subtitle {
    text-align: center;
    font-size: 17px;
    margin-bottom: 20px;
}
div.stButton > button {
    width: 100%;
}
</style>
""", unsafe_allow_html=True)

st.markdown(
    '<div class="main-title">📚 PageNest Books & Learning</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="subtitle">Find books for every subject, degree and competitive exam.</div>',
    unsafe_allow_html=True,
)

# ============================================================
# BOOK DATABASE
# Format: Title, Author/Publisher, Category, Price in INR
# Prices are illustrative and must be verified before sale.
# ============================================================

BOOKS = [
    # MATHEMATICS (10)
    ("NCERT Mathematics Class 11", "NCERT", "Mathematics", 250),
    ("NCERT Mathematics Class 12", "NCERT", "Mathematics", 280),
    ("Mathematics for Class 11", "R.D. Sharma", "Mathematics", 650),
    ("Mathematics for Class 12", "R.D. Sharma", "Mathematics", 700),
    ("Quantitative Aptitude", "R.S. Aggarwal", "Mathematics", 550),
    ("Higher Algebra", "Hall and Knight", "Mathematics", 600),
    ("Plane Trigonometry", "S.L. Loney", "Mathematics", 500),
    ("Problems in Calculus of One Variable", "I.A. Maron", "Mathematics", 650),
    ("Advanced Problems in Mathematics", "Vikas Gupta and Pankaj Joshi", "Mathematics", 750),
    ("Mathematical Techniques for Competitive Examinations", "Various authors", "Mathematics", 650),

    # SCIENCE (10)
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

    # COMMERCE & ACCOUNTING (10)
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

    # ECONOMICS (10)
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

    # BUSINESS & MANAGEMENT (10)
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

    # CAT & MBA ENTRANCE (10)
    ("How to Prepare for Quantitative Aptitude for CAT", "Arun Sharma", "CAT & MBA Entrance", 850),
    ("How to Prepare for Verbal Ability and Reading Comprehension for CAT", "Arun Sharma and Meenakshi Upadhyay", "CAT & MBA Entrance", 850),
    ("How to Prepare for Data Interpretation for CAT", "Arun Sharma", "CAT & MBA Entrance", 800),
    ("How to Prepare for Logical Reasoning for CAT", "Arun Sharma", "CAT & MBA Entrance", 800),
    ("Quantitative Aptitude for CAT", "Nishit K. Sinha", "CAT & MBA Entrance", 750),
    ("Verbal Ability and Reading Comprehension for CAT", "Nishit K. Sinha", "CAT & MBA Entrance", 750),
    ("Word Power Made Easy", "Norman Lewis", "CAT & MBA Entrance", 250),
    ("A Modern Approach to Logical Reasoning", "R.S. Aggarwal", "CAT & MBA Entrance", 500),
    ("The Official Guide to the GMAT", "GMAC", "CAT & MBA Entrance", 1000),
    ("CAT Previous Years' Solved Papers", "Arihant Experts", "CAT & MBA Entrance", 450),

    # JEE ENGINEERING ENTRANCE (10)
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

    # NEET MEDICAL ENTRANCE (10)
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

    # UPSC & CIVIL SERVICES (10)
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

    # OTHER COMPETITIVE EXAMS (10)
    ("UGC NET Commerce Guide", "Arihant Experts", "Other Competitive Exams", 700),
    ("UGC NET Management Guide", "Trueman's", "Other Competitive Exams", 700),
    ("NTA CUET (UG) English", "Verify current publisher", "Other Competitive Exams", 450),
    ("NTA CUET (UG) General Test", "Verify current publisher", "Other Competitive Exams", 450),
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

# Give each catalogue entry a unique ID, even when titles repeat.
df.insert(0, "ID", range(1, len(df) + 1))

# ============================================================
# SEARCH ALIASES
# Add common misspellings, nicknames, subjects and exam terms.
# ============================================================

ALIASES = {
    "Principles of Microeconomics": [
        "mankiw micro", "micro economics", "microeco",
        "micro econ", "mankiw", "principles micro"
    ],
    "Principles of Macroeconomics": [
        "mankiw macro", "macro economics", "macroecon",
        "macro econ", "principles macro"
    ],
    "Concepts of Physics Volume 1": [
        "hc verma", "h c verma", "hc varma",
        "h c varma", "physics concepts", "jee physics"
    ],
    "Concepts of Physics Volume 2": [
        "hc verma volume 2", "h c verma vol 2",
        "hc verma second volume"
    ],
    "Indian Polity": [
        "laxmikanth", "laxmikant", "laxmi kant",
        "laxmi kanth", "polity book", "upsc polity",
        "constitution for upsc"
    ],
    "How to Prepare for Quantitative Aptitude for CAT": [
        "arun sharma quant", "cat maths", "cat math",
        "cat quantitative", "cat quants", "quant aptitude cat"
    ],
    "How to Prepare for Verbal Ability and Reading Comprehension for CAT": [
        "arun sharma verbal", "cat english", "cat varc",
        "reading comprehension cat"
    ],
    "How to Prepare for Data Interpretation for CAT": [
        "arun sharma di", "cat data interpretation", "cat charts"
    ],
    "How to Prepare for Logical Reasoning for CAT": [
        "arun sharma lr", "cat logical reasoning", "cat logic"
    ],
    "Quantitative Aptitude": [
        "rs aggarwal maths", "r s aggarwal", "aptitude maths",
        "competitive maths", "quant"
    ],
    "Word Power Made Easy": [
        "norman lewis", "vocabulary book", "english words",
        "vocab", "word power"
    ],
    "Financial Accounting": [
        "accounts book", "accountancy", "accounting textbook",
        "financial accounts", "commerce accounts"
    ],
    "Business Law": [
        "business legal studies", "commercial law", "law for commerce"
    ],
    "Marketing Management": [
        "kotler marketing", "philip kotler",
        "marketing book", "marketing textbook"
    ],
    "Python Crash Course": [
        "python coding", "learn python", "python programming book"
    ],
    "Microsoft Excel Step by Step": [
        "excel book", "ms excel", "microsoft excel",
        "excel for beginners"
    ],
    "NCERT Biology Class 11": [
        "11th biology ncert", "class 11 bio",
        "neet biology 11", "biology textbook"
    ],
    "NCERT Biology Class 12": [
        "12th biology ncert", "class 12 bio",
        "neet biology 12"
    ],
    "NCERT Mathematics Class 11": [
        "class 11 maths", "11th maths", "eleventh mathematics",
        "11th math ncert"
    ],
    "NCERT Mathematics Class 12": [
        "class 12 maths", "12th maths", "twelfth mathematics",
        "12th math ncert"
    ],
    "Indian Economy": [
        "ramesh singh economy", "upsc economy",
        "indian economics", "economy for civil services"
    ],
    "UGC NET Commerce Guide": [
        "net commerce", "ugc net accounts", "commerce net exam"
    ],
    "UGC NET Management Guide": [
        "net management", "management net exam"
    ],
    "NTA CUET (UG) General Test": [
        "cuet general test", "cuet gt", "cuet entrance"
    ],
    "GRE Prep": [
        "gre exam", "graduate record examination", "gre preparation"
    ],
    "Official Guide to the TOEFL iBT Test": [
        "toefl", "toefl english test", "english proficiency exam"
    ],
    "A Brief History of Modern India": [
        "spectrum modern history", "rajiv ahir", "modern history upsc"
    ],
    "Objective General Knowledge": [
        "lucent gk", "general knowledge", "gk book"
    ],
    "Cengage Mathematics for JEE Main and Advanced": [
        "cengage maths", "jee cengage", "jee advanced mathematics"
    ],
    "NCERT Science Class 10": [
        "10th science", "class 10 science", "tenth science ncert"
    ],
    "Financial Management": [
        "i m pandey", "im pandey finance", "finance management"
    ],
}

# ============================================================
# SEARCH HELPERS
# ============================================================

def normalize(text):
    """Normalize punctuation, spaces and case for search."""
    text = str(text).lower().replace("&", " and ")
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def searchable_text(row):
    """Create a searchable field from title, author, category and aliases."""
    parts = [
        row["Book"],
        row["Author / Publisher"],
        row["Category"],
    ]

    parts.extend(ALIASES.get(row["Book"], []))

    # Search for abbreviations and subject names.
    if row["Category"] == "CAT & MBA Entrance":
        parts.extend(["cat", "mba", "management entrance"])
    elif row["Category"] == "JEE Engineering Entrance":
        parts.extend(["jee", "engineering entrance"])
    elif row["Category"] == "NEET Medical Entrance":
        parts.extend(["neet", "medical entrance"])
    elif row["Category"] == "UPSC & Civil Services":
        parts.extend(["upsc", "civil services", "ias"])
    elif row["Category"] == "Commerce & Accounting":
        parts.extend(["commerce", "accounts", "accounting"])
    elif row["Category"] == "Mathematics":
        parts.extend(["math", "maths", "mathematics"])
    elif row["Category"] == "Science":
        parts.extend(["science", "physics", "chemistry", "biology"])

    return normalize(" ".join(parts))


def search_catalogue(catalogue, query):
    """
    Return exact and fuzzy matches in relevance order.
    Fuzzy matching helps with typos and incomplete names.
    """
    if not query.strip():
        result = catalogue.copy()
        result["Match Score"] = 100
        return result

    query_norm = normalize(query)
    query_tokens = query_norm.split()
    scored_rows = []

    for _, row in catalogue.iterrows():
        candidate = searchable_text(row)
        candidate_tokens = candidate.split()

        # Exact phrase match gets the highest score.
        if query_norm in candidate:
            score = 100
        else:
            score = fuzz.WRatio(query_norm, candidate)

            # Match individual query words against catalogue words.
            # This helps when customers type words in a different order.
            token_scores = []

            for token in query_tokens:
                if len(token) <= 2:
                    # Short words such as "11" and "12" should match exactly.
                    best = max(
                        [100 if token == word else 0
                         for word in candidate_tokens] or [0]
                    )
                else:
                    best = max(
                        [fuzz.ratio(token, word)
                         for word in candidate_tokens] or [0]
                    )
                token_scores.append(best)

            if token_scores:
                word_score = sum(token_scores) / len(token_scores)

                # Penalize searches where most words don't match.
                good_words = sum(s >= 65 for s in token_scores)
                coverage = good_words / len(token_scores)

                score = max(score, word_score * coverage)

        # Keep plausible matches. A low threshold helps with misspellings,
        # so results should be checked by title and author.
        if score >= 43:
            scored_rows.append((row["ID"], score))

    scored_rows.sort(key=lambda item: item[1], reverse=True)

    if not scored_rows:
        return catalogue.iloc[0:0].assign(
            **{"Match Score": pd.Series(dtype=float)}
        )

    score_map = {book_id: score for book_id, score in scored_rows}

    result = catalogue[
        catalogue["ID"].isin(score_map)
    ].copy()

    result["Match Score"] = result["ID"].map(score_map)
    result = result.sort_values("Match Score", ascending=False)

    return result


# ============================================================
# SESSION STATE
# ============================================================

if "cart" not in st.session_state:
    st.session_state.cart = {}

if "customer_name" not in st.session_state:
    st.session_state.customer_name = ""

# ============================================================
# SIDEBAR
# ============================================================

page = st.sidebar.radio(
    "Navigate",
    [
        "Book Catalogue",
        "Shopping Cart & Billing",
        "Study Bundles",
        "Business Calculator",
        "About PageNest",
    ],
)

st.sidebar.divider()
st.sidebar.metric("Book Entries", len(df))
st.sidebar.metric("Categories", df["Category"].nunique())
st.sidebar.metric(
    "Cart Items",
    sum(item["quantity"] for item in st.session_state.cart.values()),
)

# ============================================================
# HELPER FUNCTIONS FOR CART
# ============================================================

def add_to_cart(book_id):
    row = df[df["ID"] == book_id].iloc[0]
    key = str(book_id)

    if key in st.session_state.cart:
        st.session_state.cart[key]["quantity"] += 1
    else:
        st.session_state.cart[key] = {
            "id": int(book_id),
            "book": row["Book"],
            "author": row["Author / Publisher"],
            "category": row["Category"],
            "price": float(row["Price"]),
            "quantity": 1,
        }


def cart_subtotal():
    return sum(
        item["price"] * item["quantity"]
        for item in st.session_state.cart.values()
    )


# ============================================================
# PAGE: BOOK CATALOGUE
# ============================================================

if page == "Book Catalogue":

    st.header("Find Your Book")

    st.write(
        "Search using a book title, partial title, author, publisher, "
        "subject, exam name or common misspelling."
    )

    with st.expander("Search examples"):
        st.write(
            "- `mankiw micro` → Principles of Microeconomics\n"
            "- `laxmikant polity` → Indian Polity\n"
            "- `hc varma` → Concepts of Physics\n"
            "- `cat quants` → CAT quantitative aptitude books\n"
            "- `11th maths` → Class 11 mathematics books\n"
            "- `lucent gk` → Objective General Knowledge"
        )

    query = st.text_input(
        "Search books",
        placeholder="Enter a title, author, publisher or exam...",
    )

    categories = ["All Categories"] + sorted(
        df["Category"].unique().tolist()
    )

    selected_category = st.selectbox(
        "Choose a category",
        categories,
    )

    max_price = st.slider(
        "Maximum price (₹)",
        min_value=0,
        max_value=2000,
        value=2000,
        step=50,
    )

    catalogue = df.copy()

    if selected_category != "All Categories":
        catalogue = catalogue[
            catalogue["Category"] == selected_category
        ]

    catalogue = catalogue[catalogue["Price"] <= max_price]

    results = search_catalogue(catalogue, query)

    sort_choice = st.selectbox(
        "Sort results",
        [
            "Most relevant",
            "Book name A–Z",
            "Price: low to high",
            "Price: high to low",
        ],
    )

    if sort_choice == "Book name A–Z":
        results = results.sort_values("Book")
    elif sort_choice == "Price: low to high":
        results = results.sort_values("Price")
    elif sort_choice == "Price: high to low":
        results = results.sort_values("Price", ascending=False)
    else:
        results = results.sort_values("Match Score", ascending=False)

    st.write(f"**{len(results)} matching book entries**")

    if query.strip() and results.empty:
        st.warning(
            "No close match found. Try fewer words, another spelling, "
            "an author name or the subject/exam name."
        )

    for _, book in results.iterrows():
        with st.container(border=True):
            left, middle, right = st.columns([5, 2, 1])

            with left:
                st.markdown(f"**{book['Book']}**")
                st.caption(f"Author / Publisher: {book['Author / Publisher']}")
                st.caption(f"Category: {book['Category']}")

                if query.strip():
                    st.caption(
                        f"Text similarity: {book['Match Score']:.0f}% "
                        "(not a guarantee of an exact match)"
                    )

            with middle:
                st.markdown(f"### ₹{book['Price']:.0f}")

            with right:
                if st.button("Add", key=f"add_{book['ID']}"):
                    add_to_cart(book["ID"])
                    st.toast(f"Added {book['Book']} to your cart.")

    st.caption(
        "Prices are illustrative. Verify the edition, ISBN, author, "
        "publisher and current selling price before purchasing."
    )

# ============================================================
# PAGE: SHOPPING CART & BILLING
# ============================================================

elif page == "Shopping Cart & Billing":

    st.header("Shopping Cart & Billing")

    st.session_state.customer_name = st.text_input(
        "Customer name",
        value=st.session_state.customer_name,
    )

    if not st.session_state.cart:
        st.info("Your cart is empty. Browse the catalogue to add books.")

    else:
        for key, item in list(st.session_state.cart.items()):
            with st.container(border=True):
                left, middle, right = st.columns([4, 2, 2])

                with left:
                    st.markdown(f"**{item['book']}**")
                    st.caption(item["author"])
                    st.caption(item["category"])

                with middle:
                    st.write(f"₹{item['price']:.2f} each")

                with right:
                    quantity = st.number_input(
                        "Quantity",
                        min_value=1,
                        max_value=99,
                        value=item["quantity"],
                        key=f"qty_{key}",
                    )
                    st.session_state.cart[key]["quantity"] = quantity

                    if st.button("Remove", key=f"remove_{key}"):
                        del st.session_state.cart[key]
                        st.rerun()

        subtotal = cart_subtotal()

        col1, col2 = st.columns(2)

        with col1:
            discount_percent = st.number_input(
                "Discount (%)",
                min_value=0.0,
                max_value=100.0,
                value=0.0,
                step=1.0,
            )

        with col2:
            gst_percent = st.number_input(
                "Estimated GST (%)",
                min_value=0.0,
                max_value=100.0,
                value=0.0,
                step=1.0,
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
        c4.metric("Total", f"₹{total:,.2f}")

        receipt_lines = [
            "PAGENEST BOOKS & LEARNING",
            "=" * 42,
            f"Date: {datetime.now().strftime('%d-%m-%Y %H:%M')}",
            f"Customer: {st.session_state.customer_name or 'Walk-in Customer'}",
            "-" * 42,
        ]

        for item in st.session_state.cart.values():
            line_total = item["price"] * item["quantity"]
            receipt_lines.append(
                f"{item['book']} | Qty {item['quantity']} | "
                f"₹{line_total:.2f}"
            )

        receipt_lines.extend([
            "-" * 42,
            f"Subtotal: ₹{subtotal:.2f}",
            f"Discount: ₹{discount:.2f}",
            f"Estimated GST: ₹{gst:.2f}",
            f"TOTAL: ₹{total:.2f}",
            "=" * 42,
            "Thank you for shopping with PageNest!",
        ])

        receipt = "\n".join(receipt_lines)

        st.download_button(
            "Download Receipt",
            data=receipt,
            file_name="pagenest_receipt.txt",
            mime="text/plain",
        )

        if st.button("Clear Entire Cart"):
            st.session_state.cart = {}
            st.rerun()

        st.caption(
            "GST is an estimate. Confirm the applicable tax treatment "
            "and rate before using this as a real invoice."
        )

# ============================================================
# PAGE: STUDY BUNDLES
# ============================================================

elif page == "Study Bundles":

    st.header("Study Bundles")
    st.write("Suggested book combinations for common study goals.")

    bundles = {
        "Mathematics Starter": [
            "NCERT Mathematics Class 11",
            "NCERT Mathematics Class 12",
            "Quantitative Aptitude",
        ],
        "Science Foundation": [
            "NCERT Science Class 10",
            "NCERT Physics Class 11",
            "NCERT Chemistry Class 11",
        ],
        "Commerce Starter": [
            "Financial Accounting",
            "Business Law",
            "Financial Management",
        ],
        "Economics Starter": [
            "Principles of Microeconomics",
            "Principles of Macroeconomics",
            "Indian Economy",
        ],
        "CAT Preparation": [
            "How to Prepare for Quantitative Aptitude for CAT",
            "How to Prepare for Verbal Ability and Reading Comprehension for CAT",
            "How to Prepare for Data Interpretation for CAT",
        ],
        "UPSC Foundation": [
            "Indian Polity",
            "A Brief History of Modern India",
            "Indian Economy",
        ],
    }

    for bundle_name, titles in bundles.items():
        bundle_df = df[df["Book"].isin(titles)].drop_duplicates(
            subset=["Book"]
        )

        subtotal = bundle_df["Price"].sum()
        bundle_price = subtotal * 0.90

        with st.container(border=True):
            st.subheader(bundle_name)

            for _, row in bundle_df.iterrows():
                st.write(f"• {row['Book']} — ₹{row['Price']:.0f}")

            st.write(f"Regular total: ₹{subtotal:.0f}")
            st.write(f"Illustrative 10% discount: ₹{subtotal * 0.10:.0f}")
            st.markdown(f"**Bundle price: ₹{bundle_price:.0f}**")

            if st.button("Add Bundle", key=f"bundle_{bundle_name}"):
                for _, row in bundle_df.iterrows():
                    add_to_cart(row["ID"])
                st.toast(f"Added {bundle_name} to your cart.")

    st.caption("Bundle prices are illustrative.")

# ============================================================
# PAGE: BUSINESS CALCULATOR
# ============================================================

elif page == "Business Calculator":

    st.header("Business Calculator")

    mode = st.selectbox(
        "Choose calculator",
        [
            "Basic Calculator",
            "Discount Calculator",
            "GST Calculator",
            "Profit Margin Calculator",
        ],
    )

    if mode == "Basic Calculator":
        a = st.number_input("First number", value=0.0)
        b = st.number_input("Second number", value=0.0)

        operation = st.selectbox(
            "Operation",
            ["Add", "Subtract", "Multiply", "Divide"],
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
        discount_rate = st.number_input(
            "Discount (%)", min_value=0.0, max_value=100.0, value=10.0
        )

        savings = price * discount_rate / 100
        st.metric("Savings", f"₹{savings:.2f}")
        st.metric("Final price", f"₹{price - savings:.2f}")

    elif mode == "GST Calculator":
        amount = st.number_input(
            "Amount before GST (₹)", min_value=0.0, value=1000.0
        )
        rate = st.number_input(
            "GST rate (%)", min_value=0.0, max_value=100.0, value=18.0
        )

        tax = amount * rate / 100
        st.metric("GST amount", f"₹{tax:.2f}")
        st.metric("Total including GST", f"₹{amount + tax:.2f}")

    elif mode == "Profit Margin Calculator":
        cost = st.number_input(
            "Cost price (₹)", min_value=0.0, value=500.0
        )
        selling = st.number_input(
            "Selling price (₹)", min_value=0.0, value=700.0
        )

        profit = selling - cost
        margin = (profit / selling * 100) if selling else 0

        st.metric("Profit / Loss", f"₹{profit:.2f}")
        st.metric("Profit margin", f"{margin:.2f}%")

# ============================================================
# PAGE: ABOUT PAGENEST
# ============================================================

elif page == "About PageNest":

    st.header("About PageNest Books & Learning")

    st.write("""
    PageNest is a text-based bookstore catalogue for students, university
    learners and competitive-exam candidates.

    It covers mathematics, science, commerce, accounting, economics,
    business management, CAT, JEE, NEET, UPSC and other competitive exams.

    Search supports partial names, common spelling errors, author names,
    subjects, aliases and exam-related keywords.
    """)

    st.subheader("Category Summary")

    summary = (
        df.groupby("Category")
        .agg(
            Book_Entries=("ID", "count"),
            Lowest_Price=("Price", "min"),
            Highest_Price=("Price", "max"),
        )
        .reset_index()
    )

    summary = summary.rename(columns={
        "Category": "Category",
        "Book_Entries": "Book Entries",
        "Lowest_Price": "Lowest Price (₹)",
        "Highest_Price": "Highest Price (₹)",
    })

    st.dataframe(summary, use_container_width=True, hide_index=True)

    st.caption(
        "This is a demonstration catalogue. Verify all bibliographic "
        "details, editions, ISBNs, publishers and prices before commercial use."
    )

# ============================================================
# FOOTER
# ============================================================

st.divider()
st.markdown(
    "<center>📚 PageNest Books & Learning | Learn • Explore • Grow</center>",
    unsafe_allow_html=True,
)
