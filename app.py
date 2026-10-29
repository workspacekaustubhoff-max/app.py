
import streamlit as st
import urllib.parse
import urllib.request
import json
import re
from difflib import SequenceMatcher
from datetime import date, timedelta

st.set_page_config(
    page_title="PageNest | Books & Learning",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------- THEME: LIGHT, HIGH-CONTRAST ----------------

st.markdown("""
<style>
.stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
    background: #F5F7FB !important;
    color: #172033 !important;
}
[data-testid="stHeader"] {
    background: #F5F7FB !important;
}
.block-container {
    max-width: 1450px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}
h1, h2, h3, h4, p, label, li,
[data-testid="stMarkdownContainer"],
[data-testid="stWidgetLabel"],
[data-testid="stCaptionContainer"] {
    color: #26344B !important;
}
[data-testid="stSidebar"] {
    background: #E8EEF7 !important;
    border-right: 1px solid #D6DFEC;
}
[data-testid="stSidebar"] * {
    color: #24334B !important;
}
.stTextInput input,
.stTextArea textarea,
.stNumberInput input {
    background: #FFFFFF !important;
    color: #172033 !important;
    -webkit-text-fill-color: #172033 !important;
    border: 1px solid #C8D3E2 !important;
    border-radius: 8px !important;
    caret-color: #2458A6 !important;
}
.stTextInput input::placeholder,
.stTextArea textarea::placeholder {
    color: #758198 !important;
    -webkit-text-fill-color: #758198 !important;
    opacity: 1 !important;
}
[data-baseweb="select"] > div {
    background: #FFFFFF !important;
    color: #172033 !important;
    border-color: #C8D3E2 !important;
}
[data-baseweb="select"] input {
    color: #172033 !important;
    -webkit-text-fill-color: #172033 !important;
}
[data-baseweb="popover"], [data-baseweb="menu"],
[role="listbox"], [role="option"] {
    background: #FFFFFF !important;
    color: #172033 !important;
}
[data-testid="stForm"] {
    background: #FFFFFF !important;
    border: 1px solid #DDE5EF !important;
    border-radius: 14px !important;
    padding: 22px !important;
}
[data-testid="stForm"] label,
[data-testid="stForm"] [data-testid="stWidgetLabel"],
[data-testid="stForm"] [data-testid="stMarkdownContainer"] {
    color: #26344B !important;
}
.stButton > button, .stFormSubmitButton > button,
.stDownloadButton > button {
    background: #2458A6 !important;
    color: #FFFFFF !important;
    border: 1px solid #2458A6 !important;
    border-radius: 9px !important;
    font-weight: 600 !important;
}
.stButton > button *, .stFormSubmitButton > button *,
.stDownloadButton > button * {
    color: #FFFFFF !important;
}
.stButton > button:hover, .stFormSubmitButton > button:hover {
    background: #183F7C !important;
}
[data-testid="stVerticalBlockBorderWrapper"] {
    background: #FFFFFF !important;
    border-color: #DDE5EF !important;
    border-radius: 14px !important;
}
[data-testid="stMetric"] {
    background: #FFFFFF !important;
    padding: 15px;
    border: 1px solid #DDE5EF;
    border-radius: 12px;
}
[data-testid="stMetricLabel"], [data-testid="stMetricValue"] {
    color: #172033 !important;
}
.hero {
    background: linear-gradient(120deg, #17345E, #3268A8);
    border-radius: 18px;
    padding: 30px;
    margin-bottom: 24px;
}
.hero h1 {
    color: #FFFFFF !important;
    font-size: 40px;
}
.hero p {
    color: #EDF4FF !important;
}
.section-title {
    color: #172A46 !important;
    font-size: 28px;
    font-weight: 700;
    margin: 18px 0;
}
.book-title {
    color: #172033 !important;
    font-size: 16px;
    font-weight: 700;
    min-height: 42px;
}
.book-author {
    color: #64718A !important;
    font-size: 13px;
    min-height: 36px;
}
.book-category {
    display: inline-block;
    background: #EAF1FF;
    color: #214E91 !important;
    border-radius: 20px;
    padding: 5px 9px;
    font-size: 11px;
    font-weight: 700;
}
.book-price {
    color: #173F7A !important;
    font-size: 21px;
    font-weight: 700;
    margin: 8px 0;
}
.footer {
    margin-top: 35px;
    padding: 22px;
    text-align: center;
    border-radius: 14px;
    background: #17345E;
    color: #FFFFFF !important;
}
.footer * { color: #FFFFFF !important; }
hr { border-color: #DDE5EF !important; }
</style>
""", unsafe_allow_html=True)

# ---------------- BOOK CATALOGUE ----------------

RAW_BOOKS = [
("Principles of Economics","N. Gregory Mankiw","Economics",899,8),
("Principles of Microeconomics","N. Gregory Mankiw","Economics",799,7),
("Principles of Macroeconomics","N. Gregory Mankiw","Economics",799,6),
("Microeconomics","Robert Pindyck and Daniel Rubinfeld","Economics",1199,5),
("Intermediate Microeconomics","Hal R. Varian","Economics",999,4),
("Macroeconomics","N. Gregory Mankiw","Economics",1099,6),
("Economics","Paul A. Samuelson and William D. Nordhaus","Economics",1299,3),
("Development Economics","Debraj Ray","Economics",999,4),
("International Economics","Dominick Salvatore","Economics",899,5),
("The Wealth of Nations","Adam Smith","Economics",499,9),
("Principles of Management","Harold Koontz and Heinz Weihrich","Business & Management",799,7),
("Management","Stephen P. Robbins and Mary Coulter","Business & Management",999,5),
("Organizational Behavior","Stephen P. Robbins and Timothy Judge","Business & Management",1099,5),
("Marketing Management","Philip Kotler and Kevin Lane Keller","Business & Management",1299,4),
("Human Resource Management","Gary Dessler","Business & Management",999,4),
("Operations Management","Jay Heizer and Barry Render","Business & Management",1099,5),
("Competitive Strategy","Michael E. Porter","Business & Management",899,4),
("The Lean Startup","Eric Ries","Business & Management",499,8),
("Good to Great","Jim Collins","Business & Management",499,6),
("The Personal MBA","Josh Kaufman","Business & Management",599,5),
("Business Model Generation","Alexander Osterwalder and Yves Pigneur","Business & Management",899,3),
("Financial Accounting","Jerry J. Weygandt, Paul D. Kimmel and Donald E. Kieso","Accounting & Finance",999,5),
("Accounting Principles","Jerry J. Weygandt, Paul D. Kimmel and Donald E. Kieso","Accounting & Finance",899,4),
("Fundamentals of Corporate Finance","Stephen A. Ross and others","Accounting & Finance",1199,4),
("Corporate Finance","Jonathan Berk and Peter DeMarzo","Accounting & Finance",1299,3),
("Financial Management","I. M. Pandey","Accounting & Finance",899,6),
("The Intelligent Investor","Benjamin Graham","Accounting & Finance",599,7),
("A Random Walk Down Wall Street","Burton G. Malkiel","Accounting & Finance",599,5),
("Business Mathematics","J. K. Sharma","Mathematics & Statistics",599,7),
("Business Statistics","J. K. Sharma","Mathematics & Statistics",699,6),
("Statistics for Business and Economics","Paul Newbold and others","Mathematics & Statistics",999,4),
("Fundamentals of Mathematical Statistics","S. C. Gupta and V. K. Kapoor","Mathematics & Statistics",899,5),
("Introduction to Probability","Joseph K. Blitzstein and Jessica Hwang","Mathematics & Statistics",999,4),
("Calculus","James Stewart","Mathematics & Statistics",1099,5),
("Linear Algebra and Its Applications","David C. Lay","Mathematics & Statistics",999,4),
("A Brief History of Time","Stephen Hawking","Science & Technology",399,7),
("Cosmos","Carl Sagan","Science & Technology",499,5),
("The Selfish Gene","Richard Dawkins","Science & Technology",599,4),
("The Origin of Species","Charles Darwin","Science & Technology",499,6),
("Concepts of Physics Volume 1","H. C. Verma","Science & Technology",499,8),
("Concepts of Physics Volume 2","H. C. Verma","Science & Technology",499,7),
("Fundamentals of Physics","David Halliday and others","Science & Technology",1199,4),
("Campbell Biology","Lisa A. Urry and others","Science & Technology",1499,3),
("How to Prepare for Quantitative Aptitude for CAT","Arun Sharma","CAT & MBA Entrance",699,8),
("How to Prepare for Data Interpretation for CAT","Arun Sharma","CAT & MBA Entrance",599,7),
("How to Prepare for Verbal Ability and Reading Comprehension for CAT","Arun Sharma","CAT & MBA Entrance",699,8),
("Quantitative Aptitude for CAT","Nishit K. Sinha","CAT & MBA Entrance",699,6),
("Verbal Ability and Reading Comprehension for CAT","Nishit K. Sinha","CAT & MBA Entrance",599,5),
("Word Power Made Easy","Norman Lewis","CAT & MBA Entrance",199,10),
("A Modern Approach to Verbal and Non-Verbal Reasoning","R. S. Aggarwal","CAT & MBA Entrance",499,8),
("Problems in General Physics","I. E. Irodov","JEE Preparation",499,5),
("Physical Chemistry","O. P. Tandon","JEE Preparation",699,6),
("Organic Chemistry","Morrison and Boyd","JEE Preparation",999,3),
("Concise Inorganic Chemistry","J. D. Lee","JEE Preparation",799,4),
("IIT Mathematics","M. L. Khanna","JEE Preparation",799,5),
("Objective Biology","Dinesh","NEET Preparation",699,6),
("Trueman's Elementary Biology","M. P. Tyagi","NEET Preparation",799,5),
("Objective Physics for NEET","D. C. Pandey","NEET Preparation",699,6),
("Objective Chemistry for NEET","D. C. Pandey","NEET Preparation",699,6),
("Indian Polity","M. Laxmikanth","UPSC & Civil Services",799,8),
("Certificate Physical and Human Geography","Goh Cheng Leong","UPSC & Civil Services",499,7),
("A Brief History of Modern India","Rajiv Ahir","UPSC & Civil Services",499,8),
("India's Struggle for Independence","Bipan Chandra","UPSC & Civil Services",599,6),
("Indian Economy","Ramesh Singh","UPSC & Civil Services",899,5),
("Environment","Shankar IAS Academy","UPSC & Civil Services",699,6),
("Introduction to the Constitution of India","D. D. Basu","UPSC & Civil Services",699,4),
("Business Law","Robert W. Emerson","Law & Communication",899,4),
("Business Law Including Company Law","P. C. Tulsian","Law & Communication",799,5),
("Business Communication Today","Courtland L. Bovee and John V. Thill","Law & Communication",999,3),
("The Elements of Style","William Strunk Jr. and E. B. White","Law & Communication",299,7),
("On Writing Well","William Zinsser","Law & Communication",399,5),
("Python Crash Course","Eric Matthes","Programming & Research",799,6),
("Automate the Boring Stuff with Python","Al Sweigart","Programming & Research",699,5),
("Learning Python","Mark Lutz","Programming & Research",1199,3),
("Think Python","Allen B. Downey","Programming & Research",599,5),
("Research Design","John W. Creswell and J. David Creswell","Programming & Research",999,4),
("The Craft of Research","Wayne C. Booth and others","Programming & Research",699,5),
("Research Methodology","C. R. Kothari","Programming & Research",599,7),
]

BOOKS = [
    {"id":i+1,"title":r[0],"author":r[1],"category":r[2],"price":r[3],"stock":r[4]}
    for i,r in enumerate(RAW_BOOKS)
]

PAGES = ["Catalogue","Shopping Cart","Checkout","Find a Book"]

if "page" not in st.session_state or st.session_state.page not in PAGES:
    st.session_state.page = "Catalogue"
if "cart" not in st.session_state:
    st.session_state.cart = {}
if "last_order" not in st.session_state:
    st.session_state.last_order = None
if "find_book_title" not in st.session_state:
    st.session_state.find_book_title = ""

def go(page):
    st.session_state.page = page
    st.rerun()

def get_book(book_id):
    return next(b for b in BOOKS if b["id"] == book_id)

def cart_count():
    return sum(st.session_state.cart.values())

def subtotal():
    return sum(get_book(i)["price"]*q for i,q in st.session_state.cart.items())

def add_to_cart(book_id):
    b = get_book(book_id)
    if st.session_state.cart.get(book_id,0) >= b["stock"]:
        st.warning("Maximum available demo stock reached.")
    else:
        st.session_state.cart[book_id] = st.session_state.cart.get(book_id,0)+1
        st.toast("Added to cart!")

def normalise(text):
    return " ".join(re.sub(r"[^a-zA-Z0-9 ]"," ",str(text).lower()).split())

def similarity(a,b):
    return SequenceMatcher(None,normalise(a),normalise(b)).ratio()

@st.cache_data(ttl=86400,show_spinner=False)
def book_cover(title,author):
    def get_json(url):
        req = urllib.request.Request(url,headers={"User-Agent":"PageNestBookstore/1.0"})
        with urllib.request.urlopen(req,timeout=4) as response:
            return json.loads(response.read().decode("utf-8"))

    try:
        url = "https://www.googleapis.com/books/v1/volumes?" + urllib.parse.urlencode({
            "q":f'intitle:"{title}" inauthor:"{author}"',
            "maxResults":8,"printType":"books"
        })
        data = get_json(url)
        for item in data.get("items",[]):
            info = item.get("volumeInfo",{})
            if similarity(title,info.get("title","")) < 0.58:
                continue
            authors = info.get("authors",[])
            if authors and not any(similarity(author,x)>0.45 for x in authors):
                continue
            links = info.get("imageLinks",{})
            image = links.get("large") or links.get("medium") or links.get("thumbnail") or links.get("smallThumbnail")
            if image:
                return image.replace("http://","https://")
    except Exception:
        pass

    try:
        url = "https://openlibrary.org/search.json?" + urllib.parse.urlencode({
            "title":title,"author":author,"limit":10,
            "fields":"title,author_name,cover_i"
        })
        data = get_json(url)
        for item in data.get("docs",[]):
            if similarity(title,item.get("title","")) < 0.58:
                continue
            authors = item.get("author_name",[])
            if authors and not any(similarity(author,x)>0.45 for x in authors):
                continue
            cover_id = item.get("cover_i")
            if cover_id:
                return f"https://covers.openlibrary.org/b/id/{cover_id}-L.jpg?default=false"
    except Exception:
        pass
    return None

# ---------------- HEADER ----------------

st.markdown("""
<div class="hero">
<h1>📚 PageNest</h1>
<p>Books, ideas and possibilities — all in one place.</p>
<p>Discover textbooks, business classics, competitive exam guides and research resources.</p>
</div>
""",unsafe_allow_html=True)

m1,m2,m3 = st.columns(3)
m1.metric("Books in Catalogue",len(BOOKS))
m2.metric("Subject Categories",len(set(b["category"] for b in BOOKS)))
m3.metric("Items in Your Cart",cart_count())

# ---------------- SIDEBAR ----------------

with st.sidebar:
    st.markdown("## 📚 PageNest")
    st.caption("Your personal bookstore")

    selected_page = st.radio(
        "Navigate",PAGES,index=PAGES.index(st.session_state.page),
        key="navigation_radio"
    )
    if selected_page != st.session_state.page:
        st.session_state.page = selected_page
        st.rerun()

    st.divider()
    st.markdown("### 🔎 Find your next book")
    search_query = st.text_input("Search title or author",placeholder="e.g. Microeconomics")
    categories = ["All Subjects"] + sorted(set(b["category"] for b in BOOKS))
    selected_category = st.selectbox("Subject",categories)
    price_limit = st.slider("Maximum price (₹)",100,1500,1500,100)
    availability = st.selectbox("Availability",["All Books","In Stock","Out of Stock"])

    st.divider()
    st.markdown("### 🛒 Your Cart")
    st.metric("Items",cart_count())
    st.metric("Subtotal",f"₹{subtotal():,.2f}")
    if st.button("View Cart",use_container_width=True):
        go("Shopping Cart")

filtered = BOOKS.copy()
if search_query.strip():
    q = normalise(search_query)
    filtered = [b for b in filtered if q in normalise(b["title"]) or q in normalise(b["author"]) or q in normalise(b["category"])]
if selected_category != "All Subjects":
    filtered = [b for b in filtered if b["category"] == selected_category]
filtered = [b for b in filtered if b["price"] <= price_limit]
if availability == "In Stock":
    filtered = [b for b in filtered if b["stock"] > 0]
elif availability == "Out of Stock":
    filtered = [b for b in filtered if b["stock"] == 0]

# ---------------- CATALOGUE ----------------

if st.session_state.page == "Catalogue":
    st.markdown('<div class="section-title">Explore the Catalogue</div>',unsafe_allow_html=True)
    st.caption(f"Showing {len(filtered)} books.")

    sort_by = st.selectbox("Sort by",["Recommended","Price: Low to High","Price: High to Low","Title A–Z"])
    if sort_by == "Price: Low to High":
        filtered.sort(key=lambda b:b["price"])
    elif sort_by == "Price: High to Low":
        filtered.sort(key=lambda b:b["price"],reverse=True)
    elif sort_by == "Title A–Z":
        filtered.sort(key=lambda b:b["title"].lower())

    if not filtered:
        st.info("No books match your filters. Try changing your search or price.")

    for start in range(0,len(filtered),3):
        cols = st.columns(3)
        for col,book in zip(cols,filtered[start:start+3]):
            with col:
                with st.container(border=True):
                    cover = book_cover(book["title"],book["author"])
                    if cover:
                        st.image(cover,use_container_width=True)
                    else:
                        st.markdown(
                            "<div style='height:190px;display:flex;align-items:center;"
                            "justify-content:center;background:#EAF1FB;border-radius:10px;font-size:50px;'>📚</div>",
                            unsafe_allow_html=True
                        )
                        cover_query = urllib.parse.quote(f'{book["title"]} {book["author"]} book cover')
                        st.markdown(f"[Search for the actual cover](https://www.google.com/search?tbm=isch&q={cover_query})")

                    st.markdown(f'<div class="book-title">{book["title"]}</div>',unsafe_allow_html=True)
                    st.markdown(f'<div class="book-author">{book["author"]}</div>',unsafe_allow_html=True)
                    st.markdown(f'<span class="book-category">{book["category"]}</span>',unsafe_allow_html=True)
                    st.markdown(f'<div class="book-price">₹{book["price"]:,}</div>',unsafe_allow_html=True)

                    if book["stock"] > 0:
                        st.caption(f'{book["stock"]} copies in demo stock')
                        if st.button("＋ Add to Cart",key=f'add_{book["id"]}',use_container_width=True):
                            add_to_cart(book["id"])
                            st.rerun()
                    else:
                        st.warning("Currently unavailable")
                        if st.button("Find Nearby Store",key=f'nearby_{book["id"]}',use_container_width=True):
                            st.session_state.find_book_title = book["title"]
                            go("Find a Book")

# ---------------- SHOPPING CART ----------------

elif st.session_state.page == "Shopping Cart":
    st.markdown('<div class="section-title">Your Shopping Cart</div>',unsafe_allow_html=True)

    if not st.session_state.cart:
        st.info("Your cart is empty.")
        if st.button("Continue Shopping"):
            go("Catalogue")
    else:
        for book_id in list(st.session_state.cart):
            book = get_book(book_id)
            quantity = st.session_state.cart[book_id]
            with st.container(border=True):
                c1,c2,c3,c4 = st.columns([4,1,2,1])
                c1.markdown(f'**{book["title"]}**')
                c1.caption(f'{book["author"]} · {book["category"]}')
                c2.write(f"Qty: {quantity}")
                c3.write(f'₹{book["price"]*quantity:,.2f}')

                if c4.button("Remove",key=f"remove_{book_id}"):
                    del st.session_state.cart[book_id]
                    st.rerun()

                q1,q2,_ = st.columns([1,1,4])
                if q1.button("−",key=f"minus_{book_id}"):
                    if quantity <= 1:
                        del st.session_state.cart[book_id]
                    else:
                        st.session_state.cart[book_id] = quantity-1
                    st.rerun()
                if q2.button("+",key=f"plus_{book_id}"):
                    if quantity < book["stock"]:
                        st.session_state.cart[book_id] = quantity+1
                    else:
                        st.warning("Maximum demo stock reached.")
                    st.rerun()

        st.divider()
        st.markdown(f"### Subtotal: ₹{subtotal():,.2f}")
        c1,c2 = st.columns(2)
        if c1.button("Continue Shopping",use_container_width=True):
            go("Catalogue")
        if c2.button("Proceed to Checkout",use_container_width=True):
            go("Checkout")

# ---------------- CHECKOUT ----------------

elif st.session_state.page == "Checkout":
    st.markdown('<div class="section-title">Checkout</div>',unsafe_allow_html=True)

    if not st.session_state.cart:
        st.info("Your cart is empty.")
        if st.button("Browse Books"):
            go("Catalogue")
    else:
        amount = subtotal()
        st.markdown("### Order Summary")
        for book_id,quantity in st.session_state.cart.items():
            book = get_book(book_id)
            st.write(f'**{book["title"]}** × {quantity} — ₹{book["price"]*quantity:,.2f}')

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
            gstin = st.text_input("GSTIN (optional)",placeholder="Enter GSTIN if applicable")
            discount_code = st.text_input("Discount Code",placeholder="Try PAGENEST10")
            st.caption("Demo checkout only. No payment is processed.")
            submitted = st.form_submit_button("Calculate Total",use_container_width=True)

        if submitted:
            required = [full_name,email,phone,address,city,state,pincode]
            if not all(x.strip() for x in required):
                st.error("Please complete all required delivery fields.")
            elif not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+",email.strip()):
                st.error("Please enter a valid email address.")
            elif not re.fullmatch(r"[0-9+\-\s()]{7,20}",phone.strip()):
                st.error("Please enter a valid phone number.")
            elif not re.fullmatch(r"[0-9A-Za-z -]{4,10}",pincode.strip()):
                st.error("Please enter a valid PIN code.")
            elif gstin.strip() and not re.fullmatch(r"[0-9A-Z]{15}",gstin.strip().upper()):
                st.error("GSTIN should contain 15 alphanumeric characters.")
            else:
                discount = round(amount*0.10,2) if discount_code.strip().upper() == "PAGENEST10" else 0
                if discount_code.strip() and discount == 0:
                    st.warning("Code not recognised. No discount applied.")
                total = max(0,amount-discount)
                st.session_state.last_order = {
                    "name":full_name.strip(),"email":email.strip(),
                    "phone":phone.strip(),"address":address.strip(),
                    "city":city.strip(),"state":state.strip(),
                    "pincode":pincode.strip(),"gstin":gstin.strip().upper(),
                    "subtotal":amount,"discount":discount,"total":total,
                    "items":cart_count(),"order_date":date.today().isoformat()
                }
                c1,c2,c3 = st.columns(3)
                c1.metric("Subtotal",f"₹{amount:,.2f}")
                c2.metric("Discount",f"−₹{discount:,.2f}")
                c3.metric("Total",f"₹{total:,.2f}")
                st.success("Order summary calculated. No payment has been taken.")

        if st.session_state.last_order:
            order = st.session_state.last_order
            st.markdown("### Latest Calculated Order")
            st.write(f'**Customer:** {order["name"]}')
            st.write(f'**Date:** {order["order_date"]}')
            st.write(f'**Delivery:** {order["city"]}, {order["state"]}')
            st.write(f'**Total:** ₹{order["total"]:,.2f}')

            summary = (
                "PAGENEST ORDER SUMMARY\n"
                f'Customer: {order["name"]}\n'
                f'Email: {order["email"]}\n'
                f'Phone: {order["phone"]}\n'
                f'Address: {order["address"]}, {order["city"]}, {order["state"]} {order["pincode"]}\n'
                f'GSTIN: {order["gstin"] or "Not provided"}\n'
                f'Subtotal: INR {order["subtotal"]:.2f}\n'
                f'Discount: INR {order["discount"]:.2f}\n'
                f'Total: INR {order["total"]:.2f}\n'
                f'Date: {order["order_date"]}\n'
                "Demo only. Payment not processed."
            )
            st.download_button(
                "Download Order Summary",data=summary,
                file_name="pagenest_order_summary.txt",mime="text/plain",
                use_container_width=True
            )

# ---------------- FIND A BOOK ----------------

elif st.session_state.page == "Find a Book":
    st.markdown('<div class="section-title">Find a Book</div>',unsafe_allow_html=True)
    st.write("Search online or find bookstores near your chosen area.")

    find_title = st.text_input(
        "Book title",
        value=st.session_state.find_book_title,
        placeholder="Enter the title you need",
        key="find_title_input"
    )
    find_author = st.text_input("Author (optional)")
    search_city = st.text_input("City or area",placeholder="e.g. Sonipat, Haryana")

    if st.button("Search for Book",use_container_width=True):
        if not find_title.strip():
            st.error("Please enter a book title.")
        else:
            term = " ".join(x for x in [find_title.strip(),find_author.strip()] if x)
            online = urllib.parse.quote(term+" buy book India")
            cover = urllib.parse.quote(term+" book cover")
            place = urllib.parse.quote(
                "bookstores near "+search_city.strip()
                if search_city.strip() else "bookstores near me"
            )
            st.markdown("### Search Results")
            st.markdown(f"[Search online for this book](https://www.google.com/search?q={online})")
            st.markdown(f"[Search cover images](https://www.google.com/search?tbm=isch&q={cover})")
            st.markdown(f"[Find bookstores on Google Maps](https://www.google.com/maps/search/?api=1&query={place})")
            estimated_date = date.today()+timedelta(days=7)
            st.markdown("### Estimated Restocking")
            st.write(f"Sample planning estimate: **{estimated_date.strftime('%d %B %Y')}**.")
            st.caption("This is not a confirmed restock date. Contact the seller to verify.")

# ---------------- FOOTER ----------------

st.markdown("""
<div class="footer">
<strong>PageNest | Books & Learning</strong><br>
Find your next idea. Discover your next chapter.<br>
<span style="font-size:12px;">Demo bookstore · Sample prices and inventory</span>
</div>
""",unsafe_allow_html=True)
