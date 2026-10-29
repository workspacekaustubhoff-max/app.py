import streamlit as st
import requests
from pathlib import Path

st.set_page_config(page_title="PageNest | The Global Bookstore", page_icon="📚", layout="wide")

st.markdown("""
<style>
.stApp {background:#faf8f4;color:#27352e}
.block-container {padding-top:1.25rem;max-width:1600px}
.brand {font-size:42px;font-weight:800;letter-spacing:-1.5px;color:#244c3e;margin:0}
.tagline {color:#748078;margin-top:-4px;margin-bottom:14px}
div[data-testid="stVerticalBlockBorderWrapper"] {border-radius:14px;border-color:#e6e2d9;background:#fffefa}
div.stButton>button {border-radius:9px}
div.stButton>button[kind="primary"] {background:#244c3e;color:white;border-color:#244c3e}
[data-testid="stMetric"] {background:#f0f3ec;border-radius:10px;padding:10px}
</style>
""", unsafe_allow_html=True)

# Fields: number, title, author/publisher, collection, exam/subject, indicative price (INR), listed price range
RAW_BOOKS = [
(1,"CUET UG General Aptitude Test","Arihant Experts","Undergraduate entrance","CUET-UG",550,""),
(2,"CUET UG English Language","Arihant Experts","Undergraduate entrance","CUET-UG English",500,""),
(3,"CUET UG Accountancy Question Bank","Oswaal Books","Undergraduate entrance","Accountancy",650,""),
(4,"Introductory Microeconomics, Class XI","NCERT","Undergraduate entrance","Economics",120,""),
(5,"Introductory Macroeconomics, Class XII","NCERT","Undergraduate entrance","Economics",120,""),
(6,"Quantitative Aptitude for Competitive Examinations","R.S. Aggarwal","Undergraduate entrance","BBA/BMS entrances",650,""),
(7,"Verbal and Non-Verbal Reasoning","R.S. Aggarwal","Undergraduate entrance","Aptitude exams",650,""),
(8,"A Modern Approach to Verbal & Non-Verbal Reasoning","R.S. Aggarwal","Undergraduate entrance","Reasoning",650,""),
(9,"Objective General English","S.P. Bakshi","Undergraduate entrance","English aptitude",550,""),
(10,"High School English Grammar and Composition","Wren & Martin","Undergraduate entrance","Grammar and English",450,""),
(11,"Business Studies, Class XI","NCERT","Undergraduate entrance","Commerce foundation",120,""),
(12,"Accountancy, Class XI","NCERT","Undergraduate entrance","Commerce foundation",120,""),
(13,"Accountancy, Class XII","NCERT","Undergraduate entrance","Commerce foundation",120,""),
(14,"Introductory Statistics, Class XI","NCERT","Undergraduate entrance","Statistics",120,""),
(15,"Indian Economic Development, Class XI/XII syllabus edition","NCERT","Undergraduate entrance","Economics",120,""),
(16,"How to Prepare for Quantitative Aptitude for CAT","Arun Sharma","Postgraduate & MBA entrance","CAT, MBA",850,""),
(17,"How to Prepare for Data Interpretation for CAT","Arun Sharma","Postgraduate & MBA entrance","CAT, MBA",800,""),
(18,"How to Prepare for Verbal Ability and Reading Comprehension for CAT","Arun Sharma","Postgraduate & MBA entrance","CAT, MBA",850,""),
(19,"Quantitative Aptitude for CAT","Nishit K. Sinha","Postgraduate & MBA entrance","CAT, MBA",850,""),
(20,"Logical Reasoning and Data Interpretation for CAT","Nishit K. Sinha","Postgraduate & MBA entrance","CAT, MBA",850,""),
(21,"Word Power Made Easy","Norman Lewis","Postgraduate & MBA entrance","CAT, GRE, verbal aptitude",300,""),
(22,"The Official GMAT Guide","GMAC","Postgraduate & MBA entrance","GMAT",1400,""),
(23,"Official GRE Super Power Pack","ETS","Postgraduate & MBA entrance","GRE",1800,""),
(24,"CUET-PG Economics preparation guide","Arihant Experts","Postgraduate & MBA entrance","CUET-PG Economics",650,""),
(25,"CUET-PG Commerce preparation guide","Arihant Experts","Postgraduate & MBA entrance","CUET-PG Commerce",650,""),
(26,"NTA UGC NET Commerce Paper II Exam Guide","Arihant Experts","Postgraduate & MBA entrance","UGC NET/JRF Commerce",650,""),
(27,"NTA UGC NET Management Paper II Exam Guide","Arihant Experts","Postgraduate & MBA entrance","UGC NET/JRF Management",650,""),
(28,"NTA UGC NET Paper I Teaching and Research Aptitude","Trueman's / other current editions","Postgraduate & MBA entrance","UGC NET Paper I",600,""),
(29,"UGC NET Paper I: Teaching and Research Aptitude","KVS Madaan","Postgraduate & MBA entrance","UGC NET",600,""),
(30,"UGC NET Economics preparation guide","Current specialist publisher edition","Postgraduate & MBA entrance","NET/JRF Economics",650,""),
(31,"Financial Accounting","S.N. Maheshwari and S.K. Maheshwari","Commerce, accounting & taxation","Accounting",750,"₹500–₹1,000"),
(32,"Corporate Accounting","J.R. Monga","Commerce, accounting & taxation","Accounting",750,"₹500–₹1,000"),
(33,"Cost and Management Accounting","M.N. Arora","Commerce, accounting & taxation","Accounting",675,"₹500–₹850"),
(34,"Financial Management","M.Y. Khan and P.K. Jain","Commerce, accounting & taxation","Finance",900,"₹600–₹1,200"),
(35,"Fundamentals of Financial Management","R.P. Rustagi","Commerce, accounting & taxation","Finance",700,"₹500–₹900"),
(36,"Income Tax: Law and Practice","H.C. Mehrotra and S.P. Goyal","Commerce, accounting & taxation","Taxation",750,"₹500–₹1,000"),
(37,"Direct Taxes Ready Reckoner","V.K. Singhania and Monica Singhania","Commerce, accounting & taxation","Taxation",1150,"₹800–₹1,500"),
(38,"GST Law and Practice","V.S. Datey","Commerce, accounting & taxation","GST",1100,"₹700–₹1,500"),
(39,"Auditing and Assurance","B.N. Tandon","Commerce, accounting & taxation","Auditing",750,"₹500–₹1,000"),
(40,"Advanced Accounting","M.C. Shukla, T.S. Grewal and S.C. Gupta","Commerce, accounting & taxation","Accounting",900,"₹600–₹1,200"),
(41,"Principles of Economics","N. Gregory Mankiw","Economics, mathematics & statistics","Economics",1300,"₹700–₹2,000"),
(42,"Managerial Economics","H.L. Ahuja","Economics, mathematics & statistics","Economics",900,"₹600–₹1,200"),
(43,"Microeconomics","Robert S. Pindyck and Daniel L. Rubinfeld","Economics, mathematics & statistics","Economics",1750,"₹1,000–₹2,500"),
(44,"Macroeconomics","N. Gregory Mankiw","Economics, mathematics & statistics","Economics",1400,"₹800–₹2,000"),
(45,"Intermediate Microeconomics","Hal R. Varian","Economics, mathematics & statistics","Economics",1750,"₹1,000–₹2,500"),
(46,"Business Statistics","N.D. Vohra","Economics, mathematics & statistics","Statistics",750,"₹500–₹1,000"),
(47,"Statistics for Management","Richard I. Levin and David S. Rubin","Economics, mathematics & statistics","Statistics",1300,"₹800–₹1,800"),
(48,"Operations Research","Hamdy A. Taha","Economics, mathematics & statistics","Operations research",1750,"₹1,000–₹2,500"),
(49,"Fundamentals of Mathematical Statistics","S.C. Gupta and V.K. Kapoor","Economics, mathematics & statistics","Statistics",900,"₹600–₹1,200"),
(50,"Quantitative Methods for Business","David R. Anderson and co-authors","Economics, mathematics & statistics","Business mathematics",1750,"₹1,000–₹2,500"),
(51,"Principles of Management","P.C. Tripathi and P.N. Reddy","Business, management & strategy","Management",600,"₹400–₹800"),
(52,"Organizational Behavior","Stephen P. Robbins and Timothy A. Judge","Business, management & strategy","Management",1700,"₹900–₹2,500"),
(53,"Marketing Management","Philip Kotler and Kevin Lane Keller","Business, management & strategy","Marketing",1650,"₹800–₹2,500"),
(54,"Strategic Management","Azhar Kazmi","Business, management & strategy","Strategy",750,"₹500–₹1,000"),
(55,"Business Environment","C.B. Gupta","Business, management & strategy","Business",600,"₹400–₹800"),
(56,"Business Laws","M.C. Kuchhal","Business, management & strategy","Business law",375,"₹250–₹500"),
(57,"Human Resource Management","Gary Dessler","Business, management & strategy","Human resources",1700,"₹900–₹2,500"),
(58,"International Business","Charles W.L. Hill and G. Tomas M. Hult","Business, management & strategy","International business",2100,"₹1,200–₹3,000"),
(59,"Entrepreneurship","Robert D. Hisrich, Michael P. Peters and Dean A. Shepherd","Business, management & strategy","Entrepreneurship",1700,"₹900–₹2,500"),
(60,"Fundamentals of Corporate Finance","Richard A. Brealey, Stewart C. Myers and Alan J. Marcus","Business, management & strategy","Corporate finance",2100,"₹1,200–₹3,000"),
(61,"Investments","Zvi Bodie, Alex Kane and Alan J. Marcus","Finance, investment & professional","CFA and finance",1800,""),
(62,"Investment Analysis and Portfolio Management","Prasanna Chandra","Finance, investment & professional","Finance",1100,""),
(63,"International Financial Management","V.K. Bhalla","Finance, investment & professional","International finance",900,""),
(64,"CFA Program Curriculum, Level I","CFA Institute","Finance, investment & professional","CFA Level I",2500,""),
(65,"CFA Program Curriculum, Level II","CFA Institute","Finance, investment & professional","CFA Level II",2500,""),
(66,"CFA Program Curriculum, Level III","CFA Institute","Finance, investment & professional","CFA Level III",2500,""),
(67,"FRM Study Materials, Part I","GARP / approved prep providers","Finance, investment & professional","FRM Part I",2000,""),
(68,"FRM Study Materials, Part II","GARP / approved prep providers","Finance, investment & professional","FRM Part II",2000,""),
(69,"Cost Accounting","M.N. Arora","Finance, investment & professional","CMA and commerce",700,""),
(70,"Company Law","Avtar Singh","Finance, investment & professional","Corporate law and commerce",800,""),
(71,"Research Methodology: Methods and Techniques","C.R. Kothari and Gaurav Garg","Research & academic writing","Research methods",600,"₹400–₹800"),
(72,"Business Research Methods","Donald R. Cooper and Pamela S. Schindler","Research & academic writing","Research methods",1400,"₹800–₹2,000"),
(73,"Research Methods for Business Students","Mark Saunders, Philip Lewis and Adrian Thornhill","Research & academic writing","Research methods",2250,"₹1,000–₹3,500"),
(74,"Marketing Research: An Applied Orientation","Naresh K. Malhotra","Research & academic writing","Marketing research",1750,"₹1,000–₹2,500"),
(75,"Multivariate Data Analysis","Joseph F. Hair Jr. and co-authors","Research & academic writing","Data analysis",3500,"₹2,000–₹5,000"),
(76,"The Craft of Research","Wayne C. Booth, Gregory G. Colomb and Joseph M. Williams","Research & academic writing","Academic writing",1400,"₹800–₹2,000"),
(77,"Publication Manual of the American Psychological Association, 7th Edition","American Psychological Association","Research & academic writing","APA style",3000,"₹2,000–₹4,000"),
(78,"The Elements of Style","William Strunk Jr. and E.B. White","Research & academic writing","Writing",550,"₹300–₹800"),
(79,"Writing for Social Scientists","Howard S. Becker","Research & academic writing","Academic writing",1300,"₹800–₹1,800"),
(80,"A Manual for Writers of Research Papers, Theses, and Dissertations","Kate L. Turabian","Research & academic writing","Academic writing",1750,"₹1,000–₹2,500"),
(81,"UGC NET Paper I Teaching and Research Aptitude","KVS Madaan","National & international research exams","India / UGC NET",600,""),
(82,"UGC NET Commerce Paper II Guide","Arihant Experts","National & international research exams","India / UGC NET",650,""),
(83,"UGC NET Management Paper II Guide","Arihant Experts","National & international research exams","India / UGC NET",650,""),
(84,"UGC NET Economics Paper II Guide","Current specialist publisher edition","National & international research exams","India / UGC NET",650,""),
(85,"PhD Entrance Examination Research Aptitude Guide","Current university-specific edition","National & international research exams","India / PhD entrance",600,""),
(86,"GRE Official Guide","ETS","National & international research exams","International graduate admissions",1200,""),
(87,"GMAT Official Guide","GMAC","National & international research exams","International business schools",1400,""),
(88,"IELTS Academic Official Practice Materials","Cambridge University Press and Assessment","National & international research exams","International admissions",900,""),
(89,"TOEFL TestReady and Official Preparation Materials","ETS","National & international research exams","International admissions",900,""),
(90,"Academic Writing for Graduate Students","John M. Swales and Christine B. Feak","National & international research exams","Research writing",1200,""),
(91,"Python Crash Course","Eric Matthes","Computing, data & business research tools","Python",1100,"₹800–₹1,500"),
(92,"Automate the Boring Stuff with Python","Al Sweigart","Computing, data & business research tools","Python",1100,"₹700–₹1,500"),
(93,"Practical Statistics for Data Scientists","Peter Bruce, Andrew Bruce and Peter Gedeck","Computing, data & business research tools","Data science",1450,"₹900–₹2,000"),
(94,"An Introduction to Statistical Learning","Gareth James and co-authors","Computing, data & business research tools","Statistics / data science",1400,"₹800–₹2,000"),
(95,"Discovering Statistics Using IBM SPSS Statistics","Andy Field","Computing, data & business research tools","SPSS / statistics",2500,"₹1,500–₹3,500"),
(96,"Data Science for Business","Foster Provost and Tom Fawcett","Computing, data & business research tools","Business analytics",1450,"₹900–₹2,000"),
(97,"Storytelling with Data","Cole Nussbaumer Knaflic","Computing, data & business research tools","Data visualisation",1100,"₹800–₹1,500"),
(98,"Business Analytics","James R. Evans","Computing, data & business research tools","Business analytics",1450,"₹900–₹2,000"),
(99,"Excel 365 Bible","Michael Alexander, Richard Kusleika and John Walkenbach","Computing, data & business research tools","Microsoft Excel",1500,"₹1,000–₹2,000"),
(100,"Tableau for Dummies","Molly Monsey and Paul Sochan","Computing, data & business research tools","Tableau / visualisation",1150,"₹800–₹1,500"),
]

# Image themes are decorative category images, not guaranteed exact book-cover images.
IMAGE_BY_CATEGORY = {
    "Undergraduate entrance": "https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=500",
    "Postgraduate & MBA entrance": "https://images.unsplash.com/photo-1516979187457-637abb4f9353?w=500",
    "Commerce, accounting & taxation": "https://images.unsplash.com/photo-1455390582262-044cdead277a?w=500",
    "Economics, mathematics & statistics": "https://images.unsplash.com/photo-1509228468518-180dd4864904?w=500",
    "Business, management & strategy": "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?w=500",
    "Finance, investment & professional": "https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=500",
    "Research & academic writing": "https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?w=500",
    "National & international research exams": "https://images.unsplash.com/photo-1512820790803-83ca734da794?w=500",
    "Computing, data & business research tools": "https://images.unsplash.com/photo-1515879218367-8466d910aaa4?w=500",
}

BOOKS = []
for number, title, author, collection, exam, price, price_range in RAW_BOOKS:
    BOOKS.append({
        "id": str(number),
        "number": number,
        "title": title,
        "author": author,
        "collection": collection,
        "exam": exam,
        "price": float(price),
        "price_range": price_range,
        "image": IMAGE_BY_CATEGORY[collection],
    })

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------
if "cart" not in st.session_state:
    st.session_state.cart = {}
if "query" not in st.session_state:
    st.session_state.query = ""
if "online_results" not in st.session_state:
    st.session_state.online_results = []
if "online_searched" not in st.session_state:
    st.session_state.online_searched = False
if "discount_pct" not in st.session_state:
    st.session_state.discount_pct = 0
if "gst_pct" not in st.session_state:
    st.session_state.gst_pct = 0

def money(value):
    return f"₹{value:,.2f}"

def add_book(book):
    book_id = str(book["id"])
    if book_id in st.session_state.cart:
        st.session_state.cart[book_id]["qty"] += 1
    else:
        st.session_state.cart[book_id] = {**book, "qty": 1}

def get_bill():
    subtotal = sum(item["price"] * item["qty"] for item in st.session_state.cart.values())
    discount = subtotal * st.session_state.discount_pct / 100
    taxable = subtotal - discount
    tax = taxable * st.session_state.gst_pct / 100
    return {
        "subtotal": subtotal, "discount": discount, "taxable": taxable,
        "tax": tax, "total": taxable + tax,
        "count": sum(item["qty"] for item in st.session_state.cart.values())
    }

@st.cache_data(ttl=1800, show_spinner=False)
def google_books_search(query):
    response = requests.get(
        "https://www.googleapis.com/books/v1/volumes",
        params={"q": query, "maxResults": 20, "orderBy": "relevance", "printType": "books"},
        timeout=12,
    )
    response.raise_for_status()
    data = response.json()
    results = []
    for entry in data.get("items", []):
        info = entry.get("volumeInfo", {})
        image_links = info.get("imageLinks", {})
        cover = image_links.get("thumbnail") or image_links.get("smallThumbnail") or ""
        if cover.startswith("http://"):
            cover = "https://" + cover[7:]
        results.append({
            "id": "online-" + entry.get("id", ""),
            "number": "Online",
            "title": info.get("title", "Untitled book"),
            "author": ", ".join(info.get("authors", ["Author not listed"])),
            "collection": "Online discovery",
            "exam": ", ".join(info.get("categories", ["Global Library"])),
            "price": 399.0,
            "price_range": "Demo price",
            "image": cover or IMAGE_BY_CATEGORY["Undergraduate entrance"],
            "link": info.get("infoLink", ""),
        })
    return results

def matches(book, query):
    terms = query.lower().strip().split()
    searchable = " ".join([
        str(book.get("number", "")), book["title"], book["author"],
        book["collection"], book["exam"], book.get("price_range", "")
    ]).lower()
    return all(term in searchable for term in terms)

def render_book(book, key_prefix):
    with st.container(border=True):
        st.image(book["image"], use_container_width=True)
        st.caption(f"#{book['number']} · {book['collection']}")
        st.markdown(f"**{book['title']}**")
        st.caption(book["author"])
        st.write(f"**{money(book['price'])}**")
        if book.get("price_range"):
            st.caption(f"Indicative range: {book['price_range']}")
        if book.get("link"):
            st.markdown(f"[Book details ↗]({book['link']})")
        if st.button("＋ Add to Bill", key=f"{key_prefix}_{book['id']}", type="primary", use_container_width=True):
            add_book(book)
            st.rerun()

def render_bill():
    bill = get_bill()
    st.markdown("## 🧾 Your Bill")
    st.caption("Always visible while browsing.")
    st.metric("Books selected", bill["count"])
    if not st.session_state.cart:
        st.info("Add a book to start your bill.")
    else:
        for book_id in list(st.session_state.cart.keys()):
            item = st.session_state.cart[book_id]
            with st.container(border=True):
                st.markdown(f"**{item['title']}**")
                st.caption(f"{money(item['price'])} each")
                c1, c2, c3 = st.columns([1, 1, 1])
                with c1:
                    if st.button("−", key=f"minus_{book_id}", use_container_width=True):
                        item["qty"] -= 1
                        if item["qty"] <= 0:
                            del st.session_state.cart[book_id]
                        st.rerun()
                with c2:
                    st.markdown(f"<div style='text-align:center;padding-top:8px'><b>{item['qty']}</b></div>", unsafe_allow_html=True)
                with c3:
                    if st.button("＋", key=f"plus_{book_id}", use_container_width=True):
                        item["qty"] += 1
                        st.rerun()
                st.write(f"Line total: **{money(item['price'] * item['qty'])}**")
                if st.button("Remove", key=f"remove_{book_id}", use_container_width=True):
                    del st.session_state.cart[book_id]
                    st.rerun()

    st.markdown("---")
    st.markdown("### Bill summary")
    st.session_state.discount_pct = st.number_input(
        "Discount (%)", min_value=0, max_value=100,
        value=int(st.session_state.discount_pct), step=1, key="discount_widget"
    )
    st.session_state.gst_pct = st.number_input(
        "GST (%)", min_value=0, max_value=28,
        value=int(st.session_state.gst_pct), step=1, key="gst_widget"
    )
    bill = get_bill()
    st.write(f"Subtotal: {money(bill['subtotal'])}")
    st.write(f"Discount: −{money(bill['discount'])}")
    st.write(f"Taxable amount: {money(bill['taxable'])}")
    st.write(f"GST: {money(bill['tax'])}")
    st.markdown(f"## Total: {money(bill['total'])}")

    if st.session_state.cart:
        bill_lines = [
            "PAGENEST — ESTIMATED BILL", "=" * 32, ""
        ]
        for item in st.session_state.cart.values():
            bill_lines.append(
                f"{item['title']} | Qty {item['qty']} | {money(item['price'] * item['qty'])}"
            )
        bill_lines.extend([
            "", f"Subtotal: {money(bill['subtotal'])}",
            f"Discount: -{money(bill['discount'])}",
            f"GST: {money(bill['tax'])}", f"TOTAL: {money(bill['total'])}",
            "", "Demo bill only; not a tax invoice or payment receipt."
        ])
        st.download_button(
            "⬇ Download Bill", "\n".join(bill_lines),
            file_name="pagenest_bill.txt", mime="text/plain",
            use_container_width=True
        )
        if st.button("Clear Bill", use_container_width=True):
            st.session_state.cart = {}
            st.rerun()
    st.caption("Sample prices are indicative, not live retailer quotes. Verify current editions, availability and tax treatment.")

def clear_search_state():
    st.session_state.query = ""
    st.session_state.online_results = []
    st.session_state.online_searched = False

# --------------------------------------------------
# HEADER AND SEARCH
# --------------------------------------------------
st.markdown('<div class="brand">PageNest 📚</div>', unsafe_allow_html=True)
st.markdown('<div class="tagline">THE GLOBAL BOOKSTORE · Find your next chapter.</div>', unsafe_allow_html=True)
st.write("100 curated titles for entrance exams, university study, finance, research and data analytics.")

# Add book_covers_collage.png to the same GitHub repository as this app.py file.
# This displays the exact cover-sheet image supplied for the bookstore homepage.
cover_sheet = Path(__file__).with_name("book_covers_collage.png")
if cover_sheet.exists():
    with st.expander("🖼️ View the book-cover collection supplied for PageNest", expanded=True):
        st.image(str(cover_sheet), caption="PageNest book-cover collection preview", use_container_width=True)
else:
    st.info("To display your supplied book-cover image, upload it to GitHub in the same folder as app.py and name it book_covers_collage.png.")

st.text_input(
    "Search all 100 books",
    key="query",
    placeholder="Search title, author, exam, subject or category — e.g. CAT, UGC NET, economics, Python...",
)

# One search field filters all 100 titles. Global discovery is optional.
top_left, top_right = st.columns([3, 1])
with top_left:
    category_options = ["All categories"] + list(dict.fromkeys(book["collection"] for book in BOOKS))
    chosen_category = st.selectbox("Category", category_options)
with top_right:
    sort_option = st.selectbox("Sort by", ["Recommended", "Price: low to high", "Price: high to low", "Title A–Z"])

online_col, reset_col = st.columns([1, 1])
with online_col:
    online_button = st.button("🌍 Search additional online books", use_container_width=True)
with reset_col:
    st.button(
        "Show all 100 books",
        on_click=clear_search_state,
        use_container_width=True,
    )

if online_button and st.session_state.query.strip():
    try:
        with st.spinner("Searching Google Books..."):
            st.session_state.online_results = google_books_search(st.session_state.query.strip())
            st.session_state.online_searched = True
    except (requests.RequestException, ValueError):
        st.warning("Online search is temporarily unavailable. The 100-book catalogue still works.")
filtered = [book for book in BOOKS if matches(book, st.session_state.query)]
if chosen_category != "All categories":
    filtered = [book for book in filtered if book["collection"] == chosen_category]
if sort_option == "Price: low to high":
    filtered.sort(key=lambda b: b["price"])
elif sort_option == "Price: high to low":
    filtered.sort(key=lambda b: b["price"], reverse=True)
elif sort_option == "Title A–Z":
    filtered.sort(key=lambda b: b["title"].lower())

st.markdown("---")
catalogue_col, bill_col = st.columns([2.1, 1], gap="large")

with catalogue_col:
    if st.session_state.query.strip():
        st.markdown(f"## Search results · {len(filtered)} catalogue match(es)")
    else:
        st.markdown("## Explore the collection")
    st.caption("Catalogue cards use subject-themed images. The supplied cover-sheet image is available above as a collection preview.")

    if not filtered:
        st.info("No catalogue matches. Try fewer words or search additional books online.")
    else:
        # Show 18 titles initially to keep the homepage tidy; all 100 remain searchable.
        visible = filtered[:18]
        for start in range(0, len(visible), 3):
            row = st.columns(3, gap="medium")
            for offset, column in enumerate(row):
                index = start + offset
                if index < len(visible):
                    with column:
                        render_book(visible[index], f"catalog_{visible[index]['id']}")
        if len(filtered) > len(visible):
            st.caption(f"Showing {len(visible)} of {len(filtered)} matches. Refine your search or category to find the rest.")

    if st.session_state.online_searched:
        st.markdown("## 🌐 Additional global search results")
        st.caption("Online results are discovery listings, not verified stock or retail prices.")
        online = st.session_state.online_results
        for start in range(0, len(online), 3):
            row = st.columns(3, gap="medium")
            for offset, column in enumerate(row):
                index = start + offset
                if index < len(online):
                    with column:
                        render_book(online[index], f"online_{index}")

with bill_col:
    with st.container(border=True):
        render_bill()

st.markdown("---")
st.caption("PageNest · The Global Bookstore · Prices are indicative demo prices. Confirm actual editions, availability, prices and applicable taxes before selling.")
