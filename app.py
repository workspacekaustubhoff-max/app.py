import streamlit as st
import requests
from pathlib import Path
from datetime import datetime
from html import escape

st.set_page_config(
    page_title="PageNest | Global Bookstore",
    page_icon="📚",
    layout="wide"
)

FIRM_NAME = "PAGENEST BOOKS & LEARNING"
TAGLINE = "Your next chapter starts here"

st.markdown("""
<style>
.stApp {background:#faf8f4;color:#27352e}
.block-container {padding-top:1.2rem;max-width:1600px}
.brand {font-size:42px;font-weight:800;color:#244c3e}
.tagline {color:#748078;margin-top:-15px}
div[data-testid="stVerticalBlockBorderWrapper"] {
    border-radius:14px;border-color:#e6e2d9;background:#fffefa
}
div.stButton>button {border-radius:9px}
div.stButton>button[kind="primary"] {
    background:#244c3e;color:white;border-color:#244c3e
}
[data-testid="stMetric"] {
    background:#f0f3ec;border-radius:10px;padding:10px
}
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# BOOK CATALOGUE
# Format: title, author, category, subject, price in INR
# Prices are sample prices and should be verified.
# --------------------------------------------------

RAW_BOOKS = [
("CUET UG General Aptitude Test","Arihant Experts","Undergraduate Entrance","CUET",550),
("CUET UG English Language","Arihant Experts","Undergraduate Entrance","English",500),
("CUET UG Accountancy Question Bank","Oswaal Books","Undergraduate Entrance","Accountancy",650),
("Introductory Microeconomics","NCERT","Undergraduate Entrance","Economics",120),
("Introductory Macroeconomics","NCERT","Undergraduate Entrance","Economics",120),
("Quantitative Aptitude for Competitive Examinations","R.S. Aggarwal","Undergraduate Entrance","Aptitude",650),
("Verbal and Non-Verbal Reasoning","R.S. Aggarwal","Undergraduate Entrance","Reasoning",650),
("A Modern Approach to Verbal and Non-Verbal Reasoning","R.S. Aggarwal","Undergraduate Entrance","Reasoning",650),
("Objective General English","S.P. Bakshi","Undergraduate Entrance","English",550),
("High School English Grammar and Composition","Wren & Martin","Undergraduate Entrance","English",450),
("Business Studies Class XI","NCERT","Undergraduate Entrance","Business Studies",120),
("Accountancy Class XI","NCERT","Undergraduate Entrance","Accountancy",120),
("Accountancy Class XII","NCERT","Undergraduate Entrance","Accountancy",120),
("Introductory Statistics","NCERT","Undergraduate Entrance","Statistics",120),
("Indian Economic Development","NCERT","Undergraduate Entrance","Economics",120),

("How to Prepare for Quantitative Aptitude for CAT","Arun Sharma","PG & MBA Entrance","CAT",850),
("How to Prepare for Data Interpretation for CAT","Arun Sharma","PG & MBA Entrance","CAT",800),
("How to Prepare for Verbal Ability and Reading Comprehension for CAT","Arun Sharma","PG & MBA Entrance","CAT",850),
("Quantitative Aptitude for CAT","Nishit K. Sinha","PG & MBA Entrance","CAT",850),
("Logical Reasoning and Data Interpretation for CAT","Nishit K. Sinha","PG & MBA Entrance","CAT",850),
("Word Power Made Easy","Norman Lewis","PG & MBA Entrance","GRE CAT English",300),
("The Official GMAT Guide","GMAC","PG & MBA Entrance","GMAT",1400),
("Official GRE Super Power Pack","ETS","PG & MBA Entrance","GRE",1800),
("CUET-PG Economics Preparation Guide","Arihant Experts","PG & MBA Entrance","CUET PG",650),
("CUET-PG Commerce Preparation Guide","Arihant Experts","PG & MBA Entrance","CUET PG",650),
("UGC NET Commerce Paper II Guide","Arihant Experts","PG & MBA Entrance","UGC NET",650),
("UGC NET Management Paper II Guide","Arihant Experts","PG & MBA Entrance","UGC NET",650),
("UGC NET Paper I Teaching and Research Aptitude","Trueman's","PG & MBA Entrance","UGC NET",600),
("UGC NET Paper I Teaching and Research Aptitude","KVS Madaan","PG & MBA Entrance","UGC NET",600),
("UGC NET Economics Preparation Guide","Specialist Publisher","PG & MBA Entrance","UGC NET Economics",650),

("Financial Accounting","S.N. Maheshwari","Commerce & Taxation","Accounting",750),
("Corporate Accounting","J.R. Monga","Commerce & Taxation","Accounting",750),
("Cost and Management Accounting","M.N. Arora","Commerce & Taxation","Accounting",675),
("Financial Management","M.Y. Khan and P.K. Jain","Commerce & Taxation","Finance",900),
("Fundamentals of Financial Management","R.P. Rustagi","Commerce & Taxation","Finance",700),
("Income Tax: Law and Practice","H.C. Mehrotra and S.P. Goyal","Commerce & Taxation","Taxation",750),
("Direct Taxes Ready Reckoner","V.K. Singhania","Commerce & Taxation","Taxation",1150),
("GST Law and Practice","V.S. Datey","Commerce & Taxation","GST",1100),
("Auditing and Assurance","B.N. Tandon","Commerce & Taxation","Auditing",750),
("Advanced Accounting","M.C. Shukla and T.S. Grewal","Commerce & Taxation","Accounting",900),

("Principles of Economics","N. Gregory Mankiw","Economics & Statistics","Economics",1300),
("Managerial Economics","H.L. Ahuja","Economics & Statistics","Economics",900),
("Microeconomics","Pindyck and Rubinfeld","Economics & Statistics","Economics",1750),
("Macroeconomics","N. Gregory Mankiw","Economics & Statistics","Economics",1400),
("Intermediate Microeconomics","Hal R. Varian","Economics & Statistics","Economics",1750),
("Business Statistics","N.D. Vohra","Economics & Statistics","Statistics",750),
("Statistics for Management","Levin and Rubin","Economics & Statistics","Statistics",1300),
("Operations Research","Hamdy A. Taha","Economics & Statistics","Operations Research",1750),
("Fundamentals of Mathematical Statistics","S.C. Gupta and V.K. Kapoor","Economics & Statistics","Statistics",900),
("Quantitative Methods for Business","Anderson and co-authors","Economics & Statistics","Business Mathematics",1750),

("Principles of Management","P.C. Tripathi and P.N. Reddy","Business & Management","Management",600),
("Organizational Behavior","Robbins and Judge","Business & Management","Management",1700),
("Marketing Management","Philip Kotler and Kevin Lane Keller","Business & Management","Marketing",1650),
("Strategic Management","Azhar Kazmi","Business & Management","Strategy",750),
("Business Environment","C.B. Gupta","Business & Management","Business",600),
("Business Laws","M.C. Kuchhal","Business & Management","Business Law",375),
("Human Resource Management","Gary Dessler","Business & Management","HR",1700),
("International Business","Hill and Hult","Business & Management","International Business",2100),
("Entrepreneurship","Hisrich, Peters and Shepherd","Business & Management","Entrepreneurship",1700),
("Fundamentals of Corporate Finance","Brealey, Myers and Marcus","Business & Management","Corporate Finance",2100),

("Investments","Bodie, Kane and Marcus","Finance & Professional","Investments",1800),
("Investment Analysis and Portfolio Management","Prasanna Chandra","Finance & Professional","Investments",1100),
("International Financial Management","V.K. Bhalla","Finance & Professional","Finance",900),
("CFA Program Curriculum Level I","CFA Institute","Finance & Professional","CFA",2500),
("CFA Program Curriculum Level II","CFA Institute","Finance & Professional","CFA",2500),
("CFA Program Curriculum Level III","CFA Institute","Finance & Professional","CFA",2500),
("FRM Study Materials Part I","GARP","Finance & Professional","FRM",2000),
("FRM Study Materials Part II","GARP","Finance & Professional","FRM",2000),
("Cost Accounting","M.N. Arora","Finance & Professional","CMA",700),
("Company Law","Avtar Singh","Finance & Professional","Company Law",800),

("Research Methodology: Methods and Techniques","C.R. Kothari and Gaurav Garg","Research & Academic Writing","Research",600),
("Business Research Methods","Cooper and Schindler","Research & Academic Writing","Research",1400),
("Research Methods for Business Students","Saunders, Lewis and Thornhill","Research & Academic Writing","Research",2250),
("Marketing Research: An Applied Orientation","Naresh K. Malhotra","Research & Academic Writing","Marketing Research",1750),
("Multivariate Data Analysis","Joseph F. Hair Jr. and co-authors","Research & Academic Writing","Data Analysis",3500),
("The Craft of Research","Booth, Colomb and Williams","Research & Academic Writing","Research",1400),
("Publication Manual of the APA 7th Edition","American Psychological Association","Research & Academic Writing","APA",3000),
("The Elements of Style","Strunk and White","Research & Academic Writing","Writing",550),
("Writing for Social Scientists","Howard S. Becker","Research & Academic Writing","Writing",1300),
("A Manual for Writers of Research Papers, Theses and Dissertations","Kate L. Turabian","Research & Academic Writing","Writing",1750),

("UGC NET Paper I Teaching and Research Aptitude","KVS Madaan","Global & National Exams","UGC NET",600),
("UGC NET Commerce Paper II Guide","Arihant Experts","Global & National Exams","UGC NET",650),
("UGC NET Management Paper II Guide","Arihant Experts","Global & National Exams","UGC NET",650),
("UGC NET Economics Paper II Guide","Specialist Publisher","Global & National Exams","UGC NET",650),
("PhD Entrance Examination Research Aptitude Guide","University-specific editions","Global & National Exams","PhD Entrance",600),
("GRE Official Guide","ETS","Global & National Exams","GRE",1200),
("GMAT Official Guide","GMAC","Global & National Exams","GMAT",1400),
("IELTS Academic Official Practice Materials","Cambridge University Press","Global & National Exams","IELTS",900),
("TOEFL Official Preparation Materials","ETS","Global & National Exams","TOEFL",900),
("Academic Writing for Graduate Students","Swales and Feak","Global & National Exams","Academic Writing",1200),

("Python Crash Course","Eric Matthes","Computing & Data","Python",1100),
("Automate the Boring Stuff with Python","Al Sweigart","Computing & Data","Python",1100),
("Practical Statistics for Data Scientists","Bruce, Bruce and Gedeck","Computing & Data","Data Science",1450),
("An Introduction to Statistical Learning","James and co-authors","Computing & Data","Statistics",1400),
("Discovering Statistics Using IBM SPSS Statistics","Andy Field","Computing & Data","SPSS",2500),
("Data Science for Business","Provost and Fawcett","Computing & Data","Data Science",1450),
("Storytelling with Data","Cole Nussbaumer Knaflic","Computing & Data","Data Visualisation",1100),
("Business Analytics","James R. Evans","Computing & Data","Business Analytics",1450),
("Excel 365 Bible","Alexander, Kusleika and Walkenbach","Computing & Data","Excel",1500),
("Tableau for Dummies","Monsey and Sochan","Computing & Data","Tableau",1150),
]

IMAGE_BY_CATEGORY = {
    "Undergraduate Entrance": "https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=600",
    "PG & MBA Entrance": "https://images.unsplash.com/photo-1516979187457-637abb4f9353?w=600",
    "Commerce & Taxation": "https://images.unsplash.com/photo-1455390582262-044cdead277a?w=600",
    "Economics & Statistics": "https://images.unsplash.com/photo-1509228468518-180dd4864904?w=600",
    "Business & Management": "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?w=600",
    "Finance & Professional": "https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=600",
    "Research & Academic Writing": "https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?w=600",
    "Global & National Exams": "https://images.unsplash.com/photo-1512820790803-83ca734da794?w=600",
    "Computing & Data": "https://images.unsplash.com/photo-1515879218367-8466d910aaa4?w=600",
}

BOOKS = []
for i, row in enumerate(RAW_BOOKS, start=1):
    title, author, category, subject, price = row
    BOOKS.append({
        "id": str(i),
        "title": title,
        "author": author,
        "category": category,
        "subject": subject,
        "price": float(price),
        "image": IMAGE_BY_CATEGORY[category],
    })

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "cart" not in st.session_state:
    st.session_state.cart = {}
if "search" not in st.session_state:
    st.session_state.search = ""

def money(amount):
    return f"₹{amount:,.2f}"

def add_to_cart(book):
    key = book["id"]
    if key in st.session_state.cart:
        st.session_state.cart[key]["qty"] += 1
    else:
        st.session_state.cart[key] = {**book, "qty": 1}

def bill_totals():
    subtotal = sum(
        item["price"] * item["qty"]
        for item in st.session_state.cart.values()
    )
    discount = subtotal * st.session_state.discount / 100
    taxable = subtotal - discount
    tax = taxable * st.session_state.gst / 100
    return subtotal, discount, tax, taxable + tax

# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.markdown('<div class="brand">📚 PageNest</div>', unsafe_allow_html=True)
st.markdown(
    f'<div class="tagline">{TAGLINE} · THE GLOBAL BOOKSTORE</div>',
    unsafe_allow_html=True
)
st.write(
    "Discover books for university, competitive exams, commerce, "
    "economics, finance, research and data analytics."
)

# Your collage image: upload it to the same GitHub folder as app.py.
cover_image = Path(__file__).with_name("book_covers_collage.png")
if cover_image.exists():
    with st.expander("🖼️ Browse our book-cover collection", expanded=True):
        st.image(str(cover_image), use_container_width=True)
else:
    st.info(
        "For your cover collage, upload book_covers_collage.png "
        "to the same GitHub folder as app.py."
    )

# --------------------------------------------------
# SEARCH AND FILTERS
# --------------------------------------------------

st.text_input(
    "🔎 Search books",
    key="search",
    placeholder="Try CAT, Python, economics, UGC NET, accounting..."
)

left_filter, right_filter = st.columns(2)
categories = ["All categories"] + sorted(set(b["category"] for b in BOOKS))

with left_filter:
    selected_category = st.selectbox("Choose a category", categories)

with right_filter:
    sort_by = st.selectbox(
        "Sort catalogue",
        ["Recommended", "Price: low to high", "Price: high to low", "Title A–Z"]
    )

# --------------------------------------------------
# CALCULATOR
# --------------------------------------------------

with st.expander("🧮 Quick calculator", expanded=False):
    a, b, op = st.columns(3)
    with a:
        first = st.number_input("First number", value=0.0, key="calc_a")
    with b:
        second = st.number_input("Second number", value=0.0, key="calc_b")
    with op:
        operation = st.selectbox(
            "Operation",
            ["Add (+)", "Subtract (-)", "Multiply (×)", "Divide (÷)"],
            key="calc_op"
        )

    if operation == "Add (+)":
        result = first + second
    elif operation == "Subtract (-)":
        result = first - second
    elif operation == "Multiply (×)":
        result = first * second
    else:
        result = None if second == 0 else first / second

    if result is None:
        st.warning("You cannot divide by zero.")
    else:
        st.metric("Result", f"{result:,.2f}")

# --------------------------------------------------
# FILTER BOOKS
# --------------------------------------------------

query = st.session_state.search.lower().strip()
filtered_books = []

for book in BOOKS:
    searchable = (
        book["title"] + " " + book["author"] + " " +
        book["category"] + " " + book["subject"]
    ).lower()

    if query and not all(word in searchable for word in query.split()):
        continue

    if selected_category != "All categories":
        if book["category"] != selected_category:
            continue

    filtered_books.append(book)

if sort_by == "Price: low to high":
    filtered_books.sort(key=lambda book: book["price"])
elif sort_by == "Price: high to low":
    filtered_books.sort(key=lambda book: book["price"], reverse=True)
elif sort_by == "Title A–Z":
    filtered_books.sort(key=lambda book: book["title"].lower())

st.markdown("---")

catalogue_column, bill_column = st.columns([2.1, 1], gap="large")

# --------------------------------------------------
# BOOK CATALOGUE
# --------------------------------------------------

with catalogue_column:
    st.subheader(f"📚 Book Catalogue ({len(filtered_books)} results)")

    if not filtered_books:
        st.info("No books found. Try another search.")
    else:
        for start in range(0, len(filtered_books), 3):
            columns = st.columns(3, gap="medium")

            for offset, column in enumerate(columns):
                index = start + offset
                if index >= len(filtered_books):
                    continue

                book = filtered_books[index]

                with column:
                    with st.container(border=True):
                        st.image(book["image"], use_container_width=True)
                        st.caption(book["category"])
                        st.markdown(f"**{book['title']}**")
                        st.caption(f"Author: {book['author']}")
                        st.caption(f"Subject: {book['subject']}")
                        st.markdown(f"### {money(book['price'])}")

                        if st.button(
                            "＋ Add to Bill",
                            key=f"add_{book['id']}",
                            type="primary",
                            use_container_width=True
                        ):
                            add_to_cart(book)
                            st.rerun()

# --------------------------------------------------
# BILL PANEL
# --------------------------------------------------

with bill_column:
    with st.container(border=True):
        st.subheader("🧾 Your Bill")

        total_books = sum(
            item["qty"] for item in st.session_state.cart.values()
        )
        st.metric("Books selected", total_books)

        if not st.session_state.cart:
            st.info("Your bill is empty. Add books from the catalogue.")
        else:
            for book_id in list(st.session_state.cart.keys()):
                item = st.session_state.cart[book_id]

                with st.container(border=True):
                    st.markdown(f"**{item['title']}**")
                    st.caption(f"{money(item['price'])} each")

                    minus, quantity, plus = st.columns([1, 1, 1])

                    with minus:
                        if st.button("−", key=f"minus_{book_id}"):
                            item["qty"] -= 1
                            if item["qty"] <= 0:
                                del st.session_state.cart[book_id]
                            st.rerun()

                    with quantity:
                        st.markdown(
                            f"<div style='text-align:center;padding:8px'>"
                            f"<b>{item['qty']}</b></div>",
                            unsafe_allow_html=True
                        )

                    with plus:
                        if st.button("＋", key=f"plus_{book_id}"):
                            item["qty"] += 1
                            st.rerun()

                    st.write(
                        f"Line total: **{money(item['price'] * item['qty'])}**"
                    )

                    if st.button("Remove book", key=f"remove_{book_id}"):
                        del st.session_state.cart[book_id]
                        st.rerun()

        st.markdown("---")
        st.markdown("### 💰 Bill calculation")

        st.number_input(
            "Discount (%)",
            min_value=0,
            max_value=100,
            value=st.session_state.get("discount", 0),
            step=1,
            key="discount"
        )

        st.number_input(
            "GST estimate (%)",
            min_value=0,
            max_value=28,
            value=st.session_state.get("gst", 0),
            step=1,
            key="gst"
        )

        subtotal, discount, tax, total = bill_totals()

        st.write(f"Subtotal: {money(subtotal)}")
        st.write(f"Discount: −{money(discount)}")
        st.write(f"Estimated GST: {money(tax)}")
        st.markdown(f"## Total: {money(total)}")

        # --------------------------------------------------
        # GENERATE AND DOWNLOAD BILL
        # --------------------------------------------------

        if st.session_state.cart:
            customer = st.text_input(
                "Customer name",
                placeholder="Enter customer name",
                key="customer_name"
            )

            bill_time = datetime.now()
            bill_number = "PN-" + bill_time.strftime("%Y%m%d-%H%M%S")
            customer_name = customer.strip() or "Walk-in customer"

            st.markdown("---")
            st.markdown(f"**{FIRM_NAME}**")
            st.caption(TAGLINE)
            st.write(f"Bill number: `{bill_number}`")
            st.write(f"Date: {bill_time.strftime('%d %b %Y, %I:%M %p')}")
            st.write(f"Customer: {customer_name}")

            for item in st.session_state.cart.values():
                st.write(
                    f"{item['title']} × {item['qty']} — "
                    f"{money(item['price'] * item['qty'])}"
                )

            st.markdown(f"**Amount payable: {money(total)}**")

            # Plain-text bill download
            lines = [
                FIRM_NAME,
                TAGLINE,
                "=" * 48,
                f"Bill number: {bill_number}",
                f"Date: {bill_time.strftime('%d %b %Y, %I:%M %p')}",
                f"Customer: {customer_name}",
                "",
                "BOOKS:"
            ]

            for item in st.session_state.cart.values():
                lines.append(
                    f"{item['title']} | Quantity: {item['qty']} | "
                    f"Unit price: {money(item['price'])} | "
                    f"Amount: {money(item['price'] * item['qty'])}"
                )

            lines.extend([
                "",
                f"Subtotal: {money(subtotal)}",
                f"Discount: -{money(discount)}",
                f"Estimated GST: {money(tax)}",
                f"TOTAL PAYABLE: {money(total)}",
                "",
                "Thank you for shopping with PageNest!",
                "This is a demo bill, not a tax invoice or payment receipt.",
                "Verify prices, editions, availability and applicable taxes."
            ])

            st.download_button(
                "⬇️ Download Bill (TXT)",
                data="\n".join(lines),
                file_name=f"PageNest_Bill_{bill_number}.txt",
                mime="text/plain",
                use_container_width=True
            )

            # Printable HTML bill
            table_rows = ""

            for item in st.session_state.cart.values():
                table_rows += (
                    "<tr>"
                    f"<td>{escape(item['title'])}</td>"
                    f"<td>{item['qty']}</td>"
                    f"<td>{money(item['price'])}</td>"
                    f"<td>{money(item['price'] * item['qty'])}</td>"
                    "</tr>"
                )

            html_bill = f"""
            <!DOCTYPE html>
            <html>
            <head>
            <meta charset="utf-8">
            <title>PageNest Bill {bill_number}</title>
            <style>
            body {{
                font-family: Arial, sans-serif;
                max-width: 850px;
                margin: 35px auto;
                padding: 20px;
                color: #24352d;
            }}
            h1 {{ color: #244c3e; }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 24px;
            }}
            th, td {{
                padding: 11px;
                border-bottom: 1px solid #ddd;
                text-align: left;
            }}
            th {{ background: #edf2ed; }}
            .total {{
                font-size: 22px;
                font-weight: bold;
                border-top: 2px solid #244c3e;
                padding-top: 12px;
            }}
            .muted {{ color: #66756d; }}
            @media print {{
                button {{ display: none; }}
                body {{ margin: 0; }}
            }}
            </style>
            </head>
            <body>
                <h1>{FIRM_NAME}</h1>
                <p class="muted">{TAGLINE}</p>
                <hr>
                <p>
                    <b>Bill number:</b> {bill_number}<br>
                    <b>Date:</b> {bill_time.strftime('%d %b %Y, %I:%M %p')}<br>
                    <b>Customer:</b> {escape(customer_name)}
                </p>
                <table>
                    <thead>
                        <tr>
                            <th>Book</th>
                            <th>Quantity</th>
                            <th>Unit price</th>
                            <th>Amount</th>
                        </tr>
                    </thead>
                    <tbody>{table_rows}</tbody>
                </table>
                <p>Subtotal: {money(subtotal)}</p>
                <p>Discount: -{money(discount)}</p>
                <p>Estimated GST: {money(tax)}</p>
                <p class="total">TOTAL PAYABLE: {money(total)}</p>
                <p><b>Thank you for choosing PageNest!</b></p>
                <p class="muted">
                    Demo bill only. Not a tax invoice or proof of payment.
                    Verify prices and applicable taxes before commercial use.
                </p>
                <button onclick="window.print()">Print / Save as PDF</button>
            </body>
            </html>
            """

            st.download_button(
                "🖨️ Download Printable Bill (HTML)",
                data=html_bill,
                file_name=f"PageNest_Bill_{bill_number}.html",
                mime="text/html",
                use_container_width=True
            )

            st.caption(
                "Open the downloaded HTML file in your browser and select "
                "Print → Save as PDF to save or print the bill."
            )

            if st.button("🗑️ Clear Entire Bill", use_container_width=True):
                st.session_state.cart = {}
                st.rerun()

st.markdown("---")
st.caption(
    "PageNest Books & Learning · Sample prices are indicative. "
    "Book images are illustrative category images, not guaranteed exact covers. "
    "Verify actual prices, editions, availability and applicable taxes."
)
