import streamlit as st
import pandas as pd
from datetime import datetime
from html import escape
from urllib.parse import quote_plus
from pathlib import Path

st.set_page_config(
    page_title="PageNest | Global Bookstore",
    page_icon="📚",
    layout="wide"
)

FIRM = "PAGENEST BOOKS & LEARNING"
TAGLINE = "Your next chapter starts here"

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
html,body,[class*="css"]{font-family:Inter,Arial,sans-serif}
.stApp{background:#F5F7F4;color:#24352D}
.block-container{max-width:1600px;padding-top:1.2rem}
.hero{padding:25px;border-radius:16px;color:white;
background:linear-gradient(110deg,#183B32,#36745C);margin-bottom:18px}
.hero h1{color:white;font-size:38px;margin:0}
.hero p{color:#E4F0E8;margin:6px 0 0}
div[data-testid="stVerticalBlockBorderWrapper"]{
border-radius:13px;border-color:#DDE5DC;background:#FFFEFA}
div.stButton>button{border-radius:9px}
div.stButton>button[kind="primary"]{
background:#285B47;color:white;border-color:#285B47}
div[data-testid="stMetric"]{
background:white;border:1px solid #DDE5DC;padding:12px;border-radius:10px}
.receipt{background:#fffdf5;color:#202020;border:1px solid #ccc;
padding:18px;font-family:monospace;font-size:12px}
</style>
<div class="hero">
<h1>📚 PageNest</h1>
<p>Books for ambitious minds — India and the world.</p>
<p>Competitive exams · Commerce · Business · Finance · Research · Technology</p>
</div>
""", unsafe_allow_html=True)

# -------------------------------------------------
# BOOK DATABASE: 100 BOOKS
# Format: title, author, category, subject, price
# Prices are illustrative; verify before selling.
# -------------------------------------------------

GROUPS = {
"Undergraduate Entrance": [
("CUET UG General Aptitude Test","Arihant","CUET",550),
("CUET UG English Language","Arihant","English",500),
("CUET UG Accountancy Question Bank","Oswaal","Accountancy",650),
("Introductory Microeconomics","NCERT","Economics",120),
("Introductory Macroeconomics","NCERT","Economics",120),
("Quantitative Aptitude","R.S. Aggarwal","Aptitude",650),
("Verbal and Non-Verbal Reasoning","R.S. Aggarwal","Reasoning",650),
("A Modern Approach to Reasoning","R.S. Aggarwal","Reasoning",650),
("Objective General English","S.P. Bakshi","English",550),
("High School English Grammar","Wren & Martin","English",450),
("Business Studies Class XI","NCERT","Business Studies",120),
("Accountancy Class XI","NCERT","Accountancy",120),
("Accountancy Class XII","NCERT","Accountancy",120),
("Introductory Statistics","NCERT","Statistics",120),
("Indian Economic Development","NCERT","Economics",120),
],
"PG & MBA Entrance": [
("CAT Quantitative Aptitude","Arun Sharma","CAT",850),
("CAT Data Interpretation","Arun Sharma","CAT",800),
("CAT Verbal Ability and Reading Comprehension","Arun Sharma","CAT",850),
("Quantitative Aptitude for CAT","Nishit K. Sinha","CAT",850),
("Logical Reasoning and Data Interpretation","Nishit K. Sinha","CAT",850),
("Word Power Made Easy","Norman Lewis","Vocabulary",300),
("Official GMAT Guide","GMAC","GMAT",1400),
("Official GRE Super Power Pack","ETS","GRE",1800),
("CUET-PG Economics Guide","Arihant","CUET PG",650),
("CUET-PG Commerce Guide","Arihant","CUET PG",650),
("UGC NET Commerce Guide","Arihant","UGC NET",650),
("UGC NET Management Guide","Arihant","UGC NET",650),
("UGC NET Paper I Teaching and Research Aptitude","Trueman's","UGC NET",600),
("UGC NET Paper I Guide","KVS Madaan","UGC NET",600),
("UGC NET Economics Guide","Various authors","UGC NET",650),
],
"Commerce & Taxation": [
("Financial Accounting","S.N. Maheshwari","Accounting",750),
("Corporate Accounting","J.R. Monga","Accounting",750),
("Cost and Management Accounting","M.N. Arora","Accounting",675),
("Financial Management","M.Y. Khan","Finance",900),
("Fundamentals of Financial Management","R.P. Rustagi","Finance",700),
("Income Tax Law and Practice","H.C. Mehrotra","Taxation",750),
("Direct Taxes Ready Reckoner","V.K. Singhania","Taxation",1150),
("GST Law and Practice","V.S. Datey","GST",1100),
("Auditing and Assurance","B.N. Tandon","Auditing",750),
("Advanced Accounting","Shukla and Grewal","Accounting",900),
],
"Economics & Statistics": [
("Principles of Economics","N. Gregory Mankiw","Economics",1300),
("Managerial Economics","H.L. Ahuja","Economics",900),
("Microeconomics","Pindyck and Rubinfeld","Economics",1750),
("Macroeconomics","N. Gregory Mankiw","Economics",1400),
("Intermediate Microeconomics","Hal R. Varian","Economics",1750),
("Business Statistics","N.D. Vohra","Statistics",750),
("Statistics for Management","Levin and Rubin","Statistics",1300),
("Operations Research","Hamdy A. Taha","Operations Research",1750),
("Mathematical Statistics","S.C. Gupta and V.K. Kapoor","Statistics",900),
("Quantitative Methods for Business","Anderson et al.","Business Mathematics",1750),
],
"Business & Management": [
("Principles of Management","P.C. Tripathi","Management",600),
("Organizational Behavior","Robbins and Judge","Management",1700),
("Marketing Management","Kotler and Keller","Marketing",1650),
("Strategic Management","Azhar Kazmi","Strategy",750),
("Business Environment","C.B. Gupta","Business",600),
("Business Laws","M.C. Kuchhal","Law",375),
("Human Resource Management","Gary Dessler","HR",1700),
("International Business","Hill and Hult","International Business",2100),
("Entrepreneurship","Hisrich et al.","Entrepreneurship",1700),
("Fundamentals of Corporate Finance","Brealey et al.","Finance",2100),
],
"Finance & Professional": [
("Investments","Bodie, Kane and Marcus","Investments",1800),
("Investment Analysis and Portfolio Management","Prasanna Chandra","Investments",1100),
("International Financial Management","V.K. Bhalla","Finance",900),
("CFA Curriculum Level I","CFA Institute","CFA",2500),
("CFA Curriculum Level II","CFA Institute","CFA",2500),
("CFA Curriculum Level III","CFA Institute","CFA",2500),
("FRM Part I Study Materials","GARP","FRM",2000),
("FRM Part II Study Materials","GARP","FRM",2000),
("Cost Accounting","M.N. Arora","Accounting",700),
("Company Law","Avtar Singh","Law",800),
],
"Research & Academic Writing": [
("Research Methodology","C.R. Kothari","Research",600),
("Business Research Methods","Cooper and Schindler","Research",1400),
("Research Methods for Business Students","Saunders et al.","Research",2250),
("Marketing Research","Naresh K. Malhotra","Marketing Research",1750),
("Multivariate Data Analysis","Hair et al.","Data Analysis",3500),
("The Craft of Research","Booth et al.","Research",1400),
("APA Publication Manual 7th Edition","APA","Academic Writing",3000),
("The Elements of Style","Strunk and White","Writing",550),
("Writing for Social Scientists","Howard S. Becker","Writing",1300),
("A Manual for Writers","Kate L. Turabian","Writing",1750),
],
"Global & National Exams": [
("UGC NET Paper I","KVS Madaan","UGC NET",600),
("UGC NET Commerce Paper II","Arihant","UGC NET",650),
("UGC NET Management Paper II","Arihant","UGC NET",650),
("UGC NET Economics Paper II","Various authors","UGC NET",650),
("PhD Entrance Research Aptitude Guide","Various authors","PhD",600),
("GRE Official Guide","ETS","GRE",1200),
("GMAT Official Guide","GMAC","GMAT",1400),
("IELTS Academic Practice Materials","Cambridge","IELTS",900),
("TOEFL Official Preparation","ETS","TOEFL",900),
("Academic Writing for Graduate Students","Swales and Feak","Writing",1200),
],
"Computing & Data": [
("Python Crash Course","Eric Matthes","Python",1100),
("Automate the Boring Stuff with Python","Al Sweigart","Python",1100),
("Practical Statistics for Data Scientists","Bruce et al.","Data Science",1450),
("An Introduction to Statistical Learning","James et al.","Statistics",1400),
("Discovering Statistics Using SPSS","Andy Field","SPSS",2500),
("Data Science for Business","Provost and Fawcett","Data Science",1450),
("Storytelling with Data","Cole Nussbaumer Knaflic","Visualisation",1100),
("Business Analytics","James R. Evans","Analytics",1450),
("Excel 365 Bible","Alexander et al.","Excel",1500),
("Tableau for Dummies","Monsey and Sochan","Tableau",1150),
],
}

IMAGE_BY_CATEGORY = {
"Undergraduate Entrance": "https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=500",
"PG & MBA Entrance": "https://images.unsplash.com/photo-1516979187457-637abb4f9353?w=500",
"Commerce & Taxation": "https://images.unsplash.com/photo-1455390582262-044cdead277a?w=500",
"Economics & Statistics": "https://images.unsplash.com/photo-1509228468518-180dd4864904?w=500",
"Business & Management": "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?w=500",
"Finance & Professional": "https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=500",
"Research & Academic Writing": "https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?w=500",
"Global & National Exams": "https://images.unsplash.com/photo-1512820790803-83ca734da794?w=500",
"Computing & Data": "https://images.unsplash.com/photo-1515879218367-8466d910aaa4?w=500",
}

BOOKS = []
for category, entries in GROUPS.items():
    for title, author, subject, price in entries:
        BOOKS.append({
            "id": str(len(BOOKS) + 1),
            "title": title,
            "author": author,
            "category": category,
            "subject": subject,
            "price": float(price),
            "image": IMAGE_BY_CATEGORY[category],
        })

def money(value):
    return f"₹{value:,.2f}"

if "cart" not in st.session_state:
    st.session_state.cart = {}
if "discount" not in st.session_state:
    st.session_state.discount = 0
if "gst" not in st.session_state:
    st.session_state.gst = 0

def add_book(book):
    key = book["id"]
    if key in st.session_state.cart:
        st.session_state.cart[key]["qty"] += 1
    else:
        st.session_state.cart[key] = {**book, "qty": 1}

def calculate_bill():
    subtotal = sum(x["price"] * x["qty"] for x in st.session_state.cart.values())
    discount = subtotal * st.session_state.discount / 100
    taxable = subtotal - discount
    tax = taxable * st.session_state.gst / 100
    return subtotal, discount, tax, taxable + tax

# Sidebar settings
with st.sidebar:
    st.header("⚙️ Order Settings")
    customer = st.text_input("Customer name", placeholder="Enter name")
    discount_name = st.selectbox("Discount", ["No discount", "5% off", "10% off"])
    st.session_state.discount = {"No discount": 0, "5% off": 5, "10% off": 10}[discount_name]
    st.session_state.gst = st.selectbox("Estimated GST (%)", [0, 5, 12, 18, 28])
    payment = st.selectbox("Payment method", ["UPI", "Cash", "Card", "Pay on delivery"])
    st.caption("Demo checkout only. No payment is processed.")

# Search and category filter
search = st.text_input("🔎 Search books", placeholder="Search title, author, exam or subject")
categories = ["All categories"] + list(GROUPS.keys())
category = st.selectbox("🌍 Browse book sections", categories)

matches = [
    book for book in BOOKS
    if search.lower() in (
        book["title"] + " " + book["author"] + " " +
        book["category"] + " " + book["subject"]
    ).lower()
    and (category == "All categories" or book["category"] == category)
]

catalogue, bill_column = st.columns([1.65, 1], gap="large")

with catalogue:
    st.subheader(f"📚 Book Catalogue · {len(matches)} results")

    for start in range(0, len(matches), 3):
        cols = st.columns(3)
        for i, col in enumerate(cols):
            index = start + i
            if index >= len(matches):
                continue

            book = matches[index]
            with col:
                with st.container(border=True):
                    st.image(book["image"], use_container_width=True)
                    st.caption(book["category"])
                    st.markdown(f"**{book['title']}**")
                    st.caption(f"Author: {book['author']}")
                    st.caption(f"Subject: {book['subject']}")
                    st.markdown(f"### {money(book['price'])}")
                    if st.button("＋ Add to Bill", key="add_" + book["id"], type="primary", use_container_width=True):
                        add_book(book)
                        st.rerun()

with bill_column:
    with st.container(border=True):
        st.subheader("🧾 Your Bill")

        if not st.session_state.cart:
            st.info("Your bill is empty. Add books from the catalogue.")
        else:
            for key in list(st.session_state.cart):
                item = st.session_state.cart[key]
                st.markdown(f"**{item['title']}**")
                st.caption(money(item["price"]) + " per book")

                left, middle, right = st.columns([1, 1, 1])
                with left:
                    if st.button("−", key="minus_" + key):
                        item["qty"] -= 1
                        if item["qty"] <= 0:
                            del st.session_state.cart[key]
                        st.rerun()
                with middle:
                    st.write(f"Qty: {item['qty']}")
                with right:
                    if st.button("＋", key="plus_" + key):
                        item["qty"] += 1
                        st.rerun()

                st.write("Line total:", money(item["price"] * item["qty"]))
                st.divider()

        subtotal, discount, tax, total = calculate_bill()
        st.write(f"Subtotal: **{money(subtotal)}**")
        st.write(f"Discount: **−{money(discount)}**")
        st.write(f"Estimated GST: **{money(tax)}**")
        st.markdown(f"## Total: {money(total)}")

        if st.button("🗑️ Clear bill", use_container_width=True):
            st.session_state.cart = {}
            st.rerun()

        if st.session_state.cart:
            st.markdown("---")
            st.markdown(f"### {FIRM}")
            st.caption(TAGLINE)

            now = datetime.now()
            bill_no = now.strftime("PN%Y%m%d%H%M%S")
            customer_name = customer.strip() or "Walk-in customer"

            st.write(f"Bill No: `{bill_no}`")
            st.write(f"Date: {now.strftime('%d-%m-%Y %I:%M %p')}")
            st.write(f"Customer: {customer_name}")
            st.write(f"Payment method: {payment}")

            receipt_rows = []
            for item in st.session_state.cart.values():
                receipt_rows.append({
                    "Book": item["title"],
                    "Author": item["author"],
                    "Quantity": item["qty"],
                    "Unit Price": item["price"],
                    "Line Total": item["price"] * item["qty"],
                })

            receipt_df = pd.DataFrame(receipt_rows)

            receipt_text = [
                FIRM,
                TAGLINE,
                "=" * 45,
                f"Bill No: {bill_no}",
                f"Date: {now.strftime('%d-%m-%Y %I:%M %p')}",
                f"Customer: {customer_name}",
                f"Payment: {payment}",
                "-" * 45,
            ]

            for item in st.session_state.cart.values():
                receipt_text.append(
                    f"{item['title']} x {item['qty']} = "
                    f"{money(item['price'] * item['qty'])}"
                )

            receipt_text += [
                "-" * 45,
                f"Subtotal: {money(subtotal)}",
                f"Discount: -{money(discount)}",
                f"Estimated GST: {money(tax)}",
                f"TOTAL PAYABLE: {money(total)}",
                "",
                "Thank you for shopping at PageNest!",
                "Demo bill, not a tax invoice or payment receipt.",
            ]

            st.download_button(
                "⬇️ Download Bill (TXT)",
                data="\n".join(receipt_text),
                file_name=f"PageNest_{bill_no}.txt",
                mime="text/plain",
                use_container_width=True,
            )

            st.download_button(
                "⬇️ Download Bill (CSV)",
                data=receipt_df.to_csv(index=False).encode("utf-8"),
                file_name=f"PageNest_{bill_no}.csv",
                mime="text/csv",
                use_container_width=True,
            )

            html_rows = ""
            for item in st.session_state.cart.values():
                html_rows += (
                    "<tr>"
                    f"<td>{escape(item['title'])}</td>"
                    f"<td>{item['qty']}</td>"
                    f"<td>{money(item['price'])}</td>"
                    f"<td>{money(item['price'] * item['qty'])}</td>"
                    "</tr>"
                )

            html_receipt = f"""
            <!DOCTYPE html><html><head><meta charset="utf-8">
            <title>PageNest Bill</title>
            <style>
            body{{font-family:Arial;max-width:800px;margin:30px auto;color:#24352D}}
            h1{{color:#285B47}}
            table{{width:100%;border-collapse:collapse}}
            th,td{{border-bottom:1px solid #ddd;padding:10px;text-align:left}}
            .total{{font-size:23px;font-weight:bold}}
            @media print{{button{{display:none}}}}
            </style></head><body>
            <h1>{FIRM}</h1><p>{TAGLINE}</p><hr>
            <p>Bill: {bill_no}<br>
            Date: {now.strftime('%d-%m-%Y %I:%M %p')}<br>
            Customer: {escape(customer_name)}<br>
            Payment: {escape(payment)}</p>
            <table><thead><tr><th>Book</th><th>Qty</th>
            <th>Unit price</th><th>Amount</th></tr></thead>
            <tbody>{html_rows}</tbody></table>
            <p>Subtotal: {money(subtotal)}</p>
            <p>Discount: -{money(discount)}</p>
            <p>Estimated GST: {money(tax)}</p>
            <p class="total">TOTAL: {money(total)}</p>
            <p>Thank you for shopping with PageNest!</p>
            <p>Demo bill, not a tax invoice or proof of payment.</p>
            <button onclick="window.print()">Print / Save as PDF</button>
            </body></html>
            """

            st.download_button(
                "🖨️ Download Printable Bill",
                data=html_receipt,
                file_name=f"PageNest_{bill_no}.html",
                mime="text/html",
                use_container_width=True,
            )

# Calculator
st.markdown("---")
with st.expander("🧮 Open Calculator"):
    a, b, op = st.columns(3)
    with a:
        first = st.number_input("First number", value=0.0)
    with b:
        second = st.number_input("Second number", value=0.0)
    with op:
        operation = st.selectbox("Operation", ["Add", "Subtract", "Multiply", "Divide"])

    if operation == "Add":
        result = first + second
    elif operation == "Subtract":
        result = first - second
    elif operation == "Multiply":
        result = first * second
    else:
        result = None if second == 0 else first / second

    if result is None:
        st.warning("Cannot divide by zero.")
    else:
        st.metric("Calculator result", f"{result:,.2f}")

# Book bundles
st.markdown("---")
st.subheader("🎁 Curated Book Bundles")
bundle_options = {
    "CAT Starter Bundle": ["CAT Quantitative Aptitude", "CAT Data Interpretation", "Word Power Made Easy"],
    "Commerce Foundation Bundle": ["Financial Accounting", "Business Statistics", "Principles of Economics"],
    "Research Starter Bundle": ["Research Methodology", "Business Research Methods", "The Craft of Research"],
    "Data Skills Bundle": ["Python Crash Course", "Business Analytics", "Excel 365 Bible"],
}

bundle_cols = st.columns(4)
for i, (bundle_name, titles) in enumerate(bundle_options.items()):
    with bundle_cols[i]:
        with st.container(border=True):
            st.markdown(f"**{bundle_name}**")
            available = [b for b in BOOKS if b["title"] in titles]
            bundle_total = sum(b["price"] for b in available)
            st.write(f"{money(bundle_total * 0.95)}")
            st.caption("Illustrative 5% bundle discount")
            if st.button("Add bundle", key="bundle_" + str(i), use_container_width=True):
                for book in available:
                    add_book(book)
                st.session_state.discount = 5
                st.rerun()

# Sample price comparison
st.markdown("---")
st.subheader("🌍 Compare Sample Basket Prices")
st.caption("The following provider multipliers are simulations, not live prices or verified quotes.")

selected = st.multiselect(
    "Choose books to compare",
    [b["title"] for b in BOOKS],
    default=["Principles of Economics", "Python Crash Course", "Research Methodology"]
)

if selected:
    providers = {
        "PageNest sample": 1.00,
        "Online bookstore estimate A": 1.04,
        "Online bookstore estimate B": 0.98,
        "Online bookstore estimate C": 1.02,
    }
    comparison = []
    for title in selected:
        book = next(b for b in BOOKS if b["title"] == title)
        row = {"Book": title}
        for provider, multiplier in providers.items():
            row[provider] = round(book["price"] * multiplier, 2)
        comparison.append(row)

    st.dataframe(pd.DataFrame(comparison), hide_index=True, use_container_width=True)

    totals = {
        provider: sum(
            next(b for b in BOOKS if b["title"] == title)["price"] * multiplier
            for title in selected
        )
        for provider, multiplier in providers.items()
    }

    cols = st.columns(len(totals))
    for i, (provider, amount) in enumerate(totals.items()):
        with cols[i]:
            st.metric(provider, money(amount))

# Online book discovery
st.markdown("---")
st.subheader("🔎 Discover More Books Worldwide")
online_query = st.text_input(
    "Search Google Books",
    placeholder="Enter a title, author, or subject"
)

if st.button("Search global books"):
    if online_query.strip():
        try:
            with st.spinner("Searching the online catalogue..."):
                response = __import__("requests").get(
                    "https://www.googleapis.com/books/v1/volumes",
                    params={"q": online_query, "maxResults": 12},
                    timeout=12,
                )
                response.raise_for_status()
                data = response.json()

            results = data.get("items", [])
            if not results:
                st.info("No matching online books found.")
            else:
                cols = st.columns(3)
                for i, entry in enumerate(results):
                    info = entry.get("volumeInfo", {})
                    image = info.get("imageLinks", {}).get("thumbnail")
                    with cols[i % 3]:
                        with st.container(border=True):
                            if image:
                                st.image(image, use_container_width=True)
                            st.markdown(f"**{info.get('title', 'Untitled')}**")
                            st.caption(", ".join(info.get("authors", ["Author not listed"])))
                            link = info.get("infoLink")
                            if link:
                                st.markdown(f"[View book details]({link})")
                            st.caption("Online listing; price and availability not verified.")
        except Exception:
            st.error("Could not reach Google Books. Please try again later.")
    else:
        st.warning("Enter a title or subject to search.")

# User's cover collage
st.markdown("---")
st.subheader("📖 Our Book Cover Collection")
collage = Path(__file__).with_name("book_covers_collage.png")
if collage.exists():
    st.image(str(collage), use_container_width=True)
else:
    st.info("Upload book_covers_collage.png to your GitHub repository to display your collection.")

st.markdown("---")
st.caption(
    "PageNest Books & Learning | Sample catalogue and prices. "
    "Images are illustrative category images, not guaranteed exact covers. "
    "Verify editions, prices, stock, discounts, and applicable taxes before commercial use. "
    "This prototype does not process payments or issue a legally compliant tax invoice."
)
