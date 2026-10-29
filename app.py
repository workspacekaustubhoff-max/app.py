
import streamlit as st
import requests
from datetime import datetime

# =========================================================
# THE BUSINESS BOOKSHOP | ACADEMIC + EXAM PREP EDITION
# =========================================================

st.set_page_config(
    page_title="The Business Bookshop",
    page_icon="📚",
    layout="wide"
)

# ------------------------ DESIGN --------------------------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@500;600;700&display=swap');

.stApp {background:#F7F5EF;color:#253B30;font-family:'DM Sans',sans-serif;}
h1,h2,h3 {font-family:'Playfair Display',serif!important;color:#234536!important;}
.hero {background:linear-gradient(125deg,#183C2D,#507858);padding:40px 32px;border-radius:20px;margin-bottom:25px;}
.hero h1 {color:#FFF8E9!important;font-size:42px;}
.hero p {color:#E6EDDF;font-size:16px;}
.eyebrow {letter-spacing:3px;font-size:12px;color:#D4E2C5;}
.book-card {background:white;border:1px solid #E8E4D9;border-radius:15px;padding:15px;min-height:150px;margin-bottom:8px;}
.book-title {font-family:'Playfair Display',serif;color:#234536;font-size:18px;font-weight:600;}
.book-subject {color:#65816A;font-size:10px;font-weight:700;letter-spacing:1px;text-transform:uppercase;}
.book-author,.muted {color:#777D73;font-size:12px;}
.book-price {color:#234536;font-size:21px;font-weight:700;}
div.stButton>button {background:#234536;color:white;border:none;border-radius:9px;min-height:38px;}
div.stButton>button:hover {background:#4D7555;color:white;border:none;}
div[data-testid="stMetric"] {background:white;border:1px solid #E8E4D9;padding:13px;border-radius:12px;}
[data-testid="stSidebar"] {background:#F0EEE5;}
.footer {text-align:center;padding:20px;color:#777D73;}
</style>
""", unsafe_allow_html=True)

# ------------------------ SOURCES -------------------------

SOURCES = {
    "BBA Honours curriculum - Nirma University":
        "https://management.nirmauni.ac.in/academics/academic-curriculum/bba-honours-curriculum/",
    "BBA curriculum - Chanakya University":
        "https://chanakyauniversity.edu.in/programme-structure/?program=252",
    "MBA curriculum - IIT Jodhpur":
        "https://www.iitj.ac.in/schools/en/program-curriculum",
    "MBA curriculum - IIT Kharagpur":
        "https://som.iitkgp.ac.in/mba_curriculum.php",
    "CAT preparation books":
        "https://www.mbauniverse.com/cat/preparation-books",
    "GMAT official exam content":
        "https://www.mba.com/exams/gmat-exam/about/exam-content",
    "GRE official test structure":
        "https://www.ets.org/gre/score-users/about/general-test/content-structure.html",
    "UGC NET official documents":
        "https://ugcnet.nta.nic.in/documents/",
    "UGC NET official syllabus":
        "https://www.ugcnetonline.in/",
    "GATE 2027 official syllabus":
        "https://gate2027.iitm.ac.in/exam_papers_and_syllabus"
}

# ------------------------ CATALOGUE -----------------------

BOOKS = {}

def add_book(book_id, title, subject, author, mrp, discount,
             description, search_title=None, exam="Academic"):
    BOOKS[book_id] = {
        "title": title,
        "subject": subject,
        "author": author,
        "mrp": mrp,
        "discount": discount,
        "description": description,
        "search_title": search_title or title,
        "exam": exam
    }


# GENERAL ACADEMIC BOOKS

add_book("A01", "Principles of Microeconomics", "Microeconomics",
         "N. Gregory Mankiw", 799, 10,
         "Demand, supply, consumer choice and markets.")
add_book("A02", "Principles of Macroeconomics", "Macroeconomics",
         "N. Gregory Mankiw", 849, 12,
         "GDP, inflation, unemployment and economic growth.")
add_book("A03", "Business Statistics", "Business Statistics",
         "Academic Reference", 599, 10,
         "Probability, statistical analysis and business data.")
add_book("A04", "Business Mathematics", "Business Mathematics",
         "Academic Reference", 549, 15,
         "Percentages, equations and quantitative business methods.")
add_book("A05", "Financial Accounting", "Financial Accounting",
         "Academic Reference", 699, 10,
         "Accounting entries, ledgers and financial statements.")
add_book("A06", "Python for Everybody", "Python",
         "Charles R. Severance", 649, 15,
         "Learn Python through practical programming examples.")
add_book("A07", "Business Law", "Legal Aspects of Business",
         "Academic Reference", 749, 10,
         "Contracts, regulations and legal principles.")
add_book("A08", "Media, Society and Government",
         "Media, Society and Government", "Academic Reference", 499, 8,
         "Media institutions, public opinion and government.")
add_book("A09", "The Personal MBA", "Business Studies",
         "Josh Kaufman", 699, 12,
         "Business fundamentals, marketing and management.")


# CAT PREPARATION

add_book("CAT01", "How to Prepare for Quantitative Aptitude for CAT",
         "CAT Preparation", "Arun Sharma", 1225, 10,
         "Practice arithmetic, algebra, geometry and CAT quantitative problems.",
         "How to Prepare for Quantitative Aptitude for CAT Arun Sharma",
         "CAT")

add_book("CAT02", "How to Prepare for Verbal Ability and Reading Comprehension",
         "CAT Preparation", "Arun Sharma and Meenakshi Upadhyay", 999, 10,
         "Reading comprehension, verbal ability and vocabulary.",
         "How to Prepare for Verbal Ability and Reading Comprehension CAT",
         "CAT")

add_book("CAT03", "How to Prepare for Data Interpretation",
         "CAT Preparation", "Arun Sharma", 899, 10,
         "Data interpretation sets, tables, charts and numerical reasoning.",
         "How to Prepare for Data Interpretation for CAT Arun Sharma", "CAT")

add_book("CAT04", "Word Power Made Easy", "CAT Preparation",
         "Norman Lewis", 199, 5,
         "Build vocabulary and improve word usage.",
         "Word Power Made Easy Norman Lewis", "CAT")

# GMAT PREPARATION

add_book("GMAT01", "The Official Guide to the GMAT",
         "GMAT Preparation", "GMAC", 1499, 5,
         "Official practice questions for GMAT preparation.",
         "The Official Guide to the GMAT latest edition GMAC", "GMAT")

add_book("GMAT02", "GMAT Official Quantitative Review",
         "GMAT Preparation", "GMAC", 999, 5,
         "Practice arithmetic, algebra and quantitative reasoning.",
         "GMAT Official Guide Quantitative Review GMAC", "GMAT")

add_book("GMAT03", "GMAT Official Verbal Review",
         "GMAT Preparation", "GMAC", 999, 5,
         "Practice reading comprehension and critical reasoning.",
         "GMAT Official Guide Verbal Review GMAC", "GMAT")

# GRE PREPARATION

add_book("GRE01", "The Official Guide to the GRE General Test",
         "GRE Preparation", "ETS", 1199, 5,
         "Official GRE practice for verbal, quantitative and writing skills.",
         "The Official Guide to the GRE General Test ETS", "GRE")

add_book("GRE02", "Official GRE Quantitative Reasoning Practice Questions",
         "GRE Preparation", "ETS", 899, 5,
         "Practice algebra, geometry, arithmetic and data analysis.",
         "Official GRE Quantitative Reasoning Practice Questions ETS", "GRE")

add_book("GRE03", "Official GRE Verbal Reasoning Practice Questions",
         "GRE Preparation", "ETS", 899, 5,
         "Improve vocabulary, comprehension and verbal reasoning.",
         "Official GRE Verbal Reasoning Practice Questions ETS", "GRE")

# UGC NET PREPARATION

add_book("NET01", "Trueman's UGC NET General Paper I",
         "UGC NET Preparation", "Trueman's", 650, 10,
         "Teaching aptitude, research aptitude and general Paper 1 practice.",
         "Truemans UGC NET General Paper 1", "UGC NET")

add_book("NET02", "UGC NET Paper 1: Teaching and Research Aptitude",
         "UGC NET Preparation", "KVS Madaan", 699, 10,
         "Concepts and practice questions for common Paper 1 topics.",
         "KVS Madaan UGC NET Paper 1 Teaching Research Aptitude", "UGC NET")

add_book("NET03", "UGC NET Commerce Preparation",
         "UGC NET Preparation", "Exam Preparation Reference", 699, 10,
         "A starting point for commerce candidates; verify syllabus coverage.",
         "UGC NET Commerce Paper 2 latest edition", "UGC NET")

# GATE PREPARATION

add_book("GATE01", "GATE Computer Science and IT Preparation",
         "GATE Preparation", "GATE Preparation Reference", 899, 10,
         "Computer science concepts and practice; check the paper-specific syllabus.",
         "GATE Computer Science Information Technology preparation book", "GATE")

add_book("GATE02", "GATE Mathematics Preparation",
         "GATE Preparation", "GATE Preparation Reference", 799, 10,
         "Mathematical concepts and practice for relevant GATE papers.",
         "GATE Engineering Mathematics preparation book", "GATE")

add_book("GATE03", "GATE General Aptitude Preparation",
         "GATE Preparation", "GATE Preparation Reference", 499, 10,
         "Practice verbal, numerical, analytical and spatial aptitude.",
         "GATE General Aptitude preparation book", "GATE")

add_book("GATE04", "GATE Data Science and Artificial Intelligence",
         "GATE Preparation", "GATE Preparation Reference", 899, 10,
         "Preparation for relevant data science and AI topics.",
         "GATE Data Science and Artificial Intelligence preparation book",
         "GATE")


# ------------------------ CURRICULUM ----------------------

CURRICULA = {
    "BBA (Honours)": {
        "description": "A general undergraduate business curriculum. "
                       "Exact courses depend on the university, programme "
                       "structure and year of admission.",
        "semesters": {
            "Semester 1": [
                "Principles of Management",
                "Microeconomics",
                "Business Mathematics",
                "Business Communication",
                "Financial Accounting",
                "Information Technology"
            ],
            "Semester 2": [
                "Macroeconomics",
                "Business Statistics",
                "Marketing Fundamentals",
                "Spreadsheet Applications",
                "Written Communication",
                "Indian Business Environment"
            ],
            "Semester 3": [
                "Organisational Behaviour",
                "Cost Accounting",
                "Business Law",
                "Operations Management",
                "Business Research Methods"
            ],
            "Semester 4": [
                "Financial Management",
                "Human Resource Management",
                "Marketing Management",
                "Management Information Systems",
                "Business Analytics"
            ],
            "Semester 5": [
                "Strategic Management",
                "Entrepreneurship",
                "Taxation Fundamentals",
                "Business Ethics",
                "Major and Minor Electives"
            ],
            "Semester 6": [
                "International Business",
                "Research Project",
                "Internship",
                "Advanced Electives"
            ],
            "Semester 7": [
                "Advanced Management Electives",
                "Research Methods",
                "Industry Project"
            ],
            "Semester 8": [
                "Research Dissertation or Capstone",
                "Specialisation Electives",
                "Internship or Applied Project"
            ]
        }
    },
    "MBA": {
        "description": "A representative two-year MBA curriculum. "
                       "Specialisations and course sequencing vary by institution.",
        "semesters": {
            "Semester 1": [
                "Financial Accounting",
                "Managerial Economics",
                "Business Statistics",
                "Marketing Management",
                "Organisational Behaviour",
                "Quantitative Techniques",
                "Business Communication"
            ],
            "Semester 2": [
                "Corporate Finance",
                "Human Resource Management",
                "Operations Management",
                "Macroeconomics for Managers",
                "Business Research Methods",
                "Management Information Systems",
                "Business Analytics"
            ],
            "Semester 3": [
                "Strategic Management",
                "International Business",
                "Entrepreneurship",
                "Specialisation Electives",
                "Summer Internship Project"
            ],
            "Semester 4": [
                "Business Ethics",
                "Corporate Governance",
                "Advanced Electives",
                "Capstone Project",
                "Comprehensive Viva"
            ]
        }
    }
}

EXAMS = {
    "CAT": {
        "full": "Common Admission Test",
        "areas": ["Quantitative Aptitude", "VARC",
                  "Data Interpretation", "Logical Reasoning"],
        "books": ["CAT01", "CAT02", "CAT03", "CAT04"],
        "note": "For admission to participating management programmes."
    },
    "GMAT": {
        "full": "Graduate Management Admission Test",
        "areas": ["Quantitative Reasoning", "Verbal Reasoning",
                  "Data Insights"],
        "books": ["GMAT01", "GMAT02", "GMAT03"],
        "note": "Check the current GMAT format and official prep materials."
    },
    "GRE": {
        "full": "Graduate Record Examination",
        "areas": ["Verbal Reasoning", "Quantitative Reasoning",
                  "Analytical Writing"],
        "books": ["GRE01", "GRE02", "GRE03"],
        "note": "Used by many graduate programmes; requirements vary."
    },
    "UGC NET": {
        "full": "University Grants Commission National Eligibility Test",
        "areas": ["Paper 1: Teaching and Research Aptitude",
                  "Paper 2: Subject-specific knowledge"],
        "books": ["NET01", "NET02", "NET03"],
        "note": "Choose Paper 2 resources according to your subject."
    },
    "GATE": {
        "full": "Graduate Aptitude Test in Engineering",
        "areas": ["General Aptitude", "Selected technical or subject paper"],
        "books": ["GATE01", "GATE02", "GATE03", "GATE04"],
        "note": "Select books for your exact GATE paper code and syllabus."
    }
}

EXAM_LINKS = {
    "CAT": "https://iimcat.ac.in/",
    "GMAT": "https://www.mba.com/exams/gmat-exam",
    "GRE": "https://www.ets.org/gre.html",
    "UGC NET": "https://ugcnet.nta.nic.in/",
    "GATE": "https://gate2027.iitm.ac.in/exam_papers_and_syllabus"
}

# ------------------------ UTILITIES ----------------------

def get_price(book):
    mrp = book.get("mrp", 0)
    discount = book.get("discount", 0)
    return {
        "mrp": mrp,
        "discount_amount": round(mrp * discount / 100, 2),
        "selling_price": round(mrp * (1 - discount / 100), 2)
    }


@st.cache_data(ttl=3600, show_spinner=False)
def get_cover(search_title):
    """Find a cover through Google Books; use a generic fallback."""
    fallback = (
        "https://images.unsplash.com/"
        "photo-1507842217343-583bb7270b66"
        "?auto=format&fit=crop&w=500&q=80"
    )

    try:
        response = requests.get(
            "https://www.googleapis.com/books/v1/volumes",
            params={"q": search_title, "maxResults": 1},
            timeout=4
        )

        if response.status_code == 200:
            items = response.json().get("items", [])

            if items:
                images = items[0].get("volumeInfo", {}).get("imageLinks", {})
                image_url = images.get("thumbnail", images.get("smallThumbnail", ""))

                if image_url:
                    return image_url.replace("http://", "https://")

    except (requests.RequestException, ValueError, KeyError):
        pass

    return fallback


def calculate_bill(cart, gst_rate=0):
    mrp_total = 0
    discount_total = 0
    subtotal = 0
    item_count = 0

    # FOR LOOP: total every item in the cart.
    for book_id, quantity in cart.items():
        book = BOOKS.get(book_id, {})

        if book:
            price = get_price(book)
            mrp_total += price["mrp"] * quantity
            discount_total += price["discount_amount"] * quantity
            subtotal += price["selling_price"] * quantity
            item_count += quantity

    gst = round(subtotal * gst_rate / 100, 2)

    return {
        "mrp": round(mrp_total, 2),
        "discount": round(discount_total, 2),
        "subtotal": round(subtotal, 2),
        "gst_rate": gst_rate,
        "gst": gst,
        "total": round(subtotal + gst, 2),
        "items": item_count
    }


def rupees(amount):
    return f"₹{amount:,.2f}"


def show_book(book_id):
    book = BOOKS.get(book_id, {})

    if not book:
        return

    price = get_price(book)
    st.image(get_cover(book.get("search_title", book["title"])),
             use_container_width=True)

    st.markdown(
        f"""
        <div class="book-card">
        <div class="book-subject">{book.get("subject", "Books")}</div>
        <div class="book-title">{book.get("title", "Book")}</div>
        <div class="book-author">{book.get("author", "")}</div>
        <p>{book.get("description", "")}</p>
        <div class="book-price">{rupees(price["selling_price"])}</div>
        <div class="muted">MRP: {rupees(price["mrp"])} |
        Save {book.get("discount", 0)}%</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button("🛒 Add to cart", key=f"add_{book_id}",
                 use_container_width=True):
        st.session_state.cart[book_id] = (
            st.session_state.cart.get(book_id, 0) + 1
        )
        st.toast("Added to your cart!")
        st.rerun()


# ------------------------ STATE --------------------------

if "cart" not in st.session_state:
    st.session_state.cart = {}

if "page" not in st.session_state:
    st.session_state.page = "Home"

if "last_order" not in st.session_state:
    st.session_state.last_order = None


# ------------------------ NAVIGATION ---------------------

with st.sidebar:
    st.markdown("## 📚 The Business Bookshop")
    st.caption("Your academic learning companion")
    st.divider()

    st.radio(
        "Navigate",
        ["Home", "Browse Books", "Exam Preparation",
         "Syllabus Guides", "Shopping Cart", "My Bill", "About Us"],
        key="page"
    )

    st.divider()
    st.metric("Books in cart", sum(st.session_state.cart.values()))
    st.caption("Read better. Learn smarter. Grow further.")

# ------------------------ HERO ---------------------------

st.markdown("""
<div class="hero">
    <div class="eyebrow">READ • LEARN • ACHIEVE</div>
    <h1>The Business Bookshop</h1>
    <p>Your one-stop learning destination for university courses
    and competitive examinations.</p>
</div>
""", unsafe_allow_html=True)


# ======================== HOME ===========================

if st.session_state.page == "Home":
    st.markdown("## Welcome to your learning space")
    st.write("Discover textbooks, exam-preparation guides and curriculum resources.")

    a, b, c = st.columns(3)
    a.metric("Books", len(BOOKS))
    b.metric("Exam categories", len(EXAMS))
    c.metric("Curriculum guides", len(CURRICULA))

    st.divider()
    st.markdown("## Explore our collections")

    a, b, c = st.columns(3)
    with a:
        st.markdown("### 📘 Academic Books")
        st.write("Economics, accounting, business, law and Python.")
        st.button("Browse books", key="home_browse",
                  on_click=lambda: st.session_state.update({"page": "Browse Books"}),
                  use_container_width=True)

    with b:
        st.markdown("### 🎯 Exam Preparation")
        st.write("CAT, GMAT, GRE, UGC NET and GATE resources.")
        st.button("Explore exams", key="home_exams",
                  on_click=lambda: st.session_state.update({"page": "Exam Preparation"}),
                  use_container_width=True)

    with c:
        st.markdown("### 🎓 Syllabus Guides")
        st.write("Explore general BBA Honours and MBA curricula.")
        st.button("View syllabuses", key="home_syllabus",
                  on_click=lambda: st.session_state.update({"page": "Syllabus Guides"}),
                  use_container_width=True)

    st.divider()
    st.markdown("## Popular books")

    popular = ["A01", "A06", "CAT01", "GMAT01", "GRE01", "NET01"]
    for start in range(0, len(popular), 3):
        columns = st.columns(3)
        for index, book_id in enumerate(popular[start:start + 3]):
            with columns[index]:
                show_book(book_id)


# ======================== BROWSE BOOKS ===================

elif st.session_state.page == "Browse Books":
    st.markdown("## Browse the bookstore")

    categories = sorted(set(
        book.get("subject", "") for book in BOOKS.values()
    ))
    selected = st.selectbox("Filter by category", ["All Categories"] + categories)
    keyword = st.text_input("🔍 Search title, author or subject")

    results = []

    # FOR LOOP: filter all books.
    for book_id, book in BOOKS.items():
        searchable = (
            book.get("title", "") + " " +
            book.get("author", "") + " " +
            book.get("subject", "")
        ).lower()

        if selected != "All Categories" and book.get("subject") != selected:
            continue

        if keyword.strip() == "":
            results.append(book_id)
        elif keyword.lower().strip() in searchable:
            results.append(book_id)
        else:
            continue

    st.caption(f"{len(results)} books found")

    if not results:
        st.info("No books found. Try a different search.")

    for start in range(0, len(results), 3):
        columns = st.columns(3)
        for index, book_id in enumerate(results[start:start + 3]):
            with columns[index]:
                show_book(book_id)


# ======================== EXAM PREPARATION ===============

elif st.session_state.page == "Exam Preparation":
    st.markdown("## Competitive examination library")
    st.write("Choose an exam to explore its main preparation areas and recommended books.")

    exam = st.selectbox("Select an examination", list(EXAMS.keys()))
    details = EXAMS.get(exam, {})

    st.markdown(f"### {exam} — {details.get('full', '')}")
    st.write(details.get("note", ""))

    st.markdown("#### Main preparation areas")
    for area in details.get("areas", []):
        st.markdown(f"- {area}")

    st.link_button("Open official exam website", EXAM_LINKS[exam])

    st.divider()
    st.markdown(f"## Recommended books for {exam}")

    book_ids = details.get("books", [])
    for start in range(0, len(book_ids), 3):
        columns = st.columns(3)
        for index, book_id in enumerate(book_ids[start:start + 3]):
            with columns[index]:
                show_book(book_id)

    st.divider()
    st.markdown("### More exam resources")

    for exam_name, url in EXAM_LINKS.items():
        st.markdown(f"- [{exam_name} official website]({url})")

    st.caption(
        "Recommendations are a starting point, not official endorsements. "
        "Check the latest exam format, edition and syllabus before purchasing."
    )


# ======================== SYLLABUS GUIDES =================

elif st.session_state.page == "Syllabus Guides":
    st.markdown("## University syllabus and curriculum guides")

    st.info(
        "These are representative learning guides, not an official syllabus "
        "for every university. Your institution's course structure, credits "
        "and admission year may differ."
    )

    programme = st.selectbox("Choose a programme", list(CURRICULA.keys()))
    curriculum = CURRICULA[programme]

    st.markdown(f"### {programme}")
    st.write(curriculum["description"])

    for semester, subjects in curriculum["semesters"].items():
        with st.expander(semester, expanded=False):
            for subject in subjects:
                st.markdown(f"- {subject}")

    st.divider()
    st.markdown("## Published university curriculum sources")

    for title, url in SOURCES.items():
        if "curriculum" in title.lower():
            st.markdown(f"- [{title}]({url})")

    st.divider()
    st.markdown("## Official exam syllabus and information")

    for exam_name in ["CAT", "GMAT", "GRE", "UGC NET", "GATE"]:
        url = EXAM_LINKS.get(exam_name, "")
        st.markdown(f"- [{exam_name} official website]({url})")

    st.markdown("### Additional references")
    st.markdown(f"- [UGC NET syllabus archive]({SOURCES['UGC NET official syllabus']})")
    st.markdown(f"- [GRE test structure]({SOURCES['GRE official test structure']})")
    st.markdown(f"- [GMAT exam content]({SOURCES['GMAT official exam content']})")


# ======================== SHOPPING CART ===================

elif st.session_state.page == "Shopping Cart":
    st.markdown("## Your shopping cart")

    if not st.session_state.cart:
        st.info("Your cart is empty. Browse the catalogue to add books.")
        st.button("Browse books",
                  on_click=lambda: st.session_state.update({"page": "Browse Books"}))
    else:
        # WHILE LOOP: display cart entries.
        ids = list(st.session_state.cart.keys())
        index = 0

        while index < len(ids):
            book_id = ids[index]
            book = BOOKS.get(book_id, {})

            if book:
                price = get_price(book)
                with st.container(border=True):
                    a, b, c = st.columns([3, 2, 1])

                    with a:
                        st.markdown(f"**{book.get('title', 'Book')}**")
                        st.caption(book.get("subject", ""))
                        st.write(rupees(price["selling_price"]) + " each")

                    with b:
                        quantity = st.number_input(
                            "Quantity", min_value=1, max_value=20,
                            value=st.session_state.cart[book_id],
                            key=f"qty_{book_id}"
                        )
                        st.session_state.cart[book_id] = quantity

                    with c:
                        st.markdown("**Line total**")
                        st.write(rupees(price["selling_price"] * quantity))
                        if st.button("Remove", key=f"remove_{book_id}"):
                            del st.session_state.cart[book_id]
                            st.rerun()

            index += 1

        bill = calculate_bill(st.session_state.cart)

        st.divider()
        a, b = st.columns(2)
        a.metric("Total MRP", rupees(bill["mrp"]))
        b.metric("You save", rupees(bill["discount"]))

        st.subheader(f"Subtotal: {rupees(bill['subtotal'])}")

        st.button("Proceed to billing", use_container_width=True,
                  on_click=lambda: st.session_state.update({"page": "My Bill"}))

        if st.button("Clear cart"):
            st.session_state.cart = {}
            st.rerun()


# ======================== BILLING =========================

elif st.session_state.page == "My Bill":
    st.markdown("## Checkout and billing")

    if not st.session_state.cart:
        st.info("Your cart is empty.")
        st.button("Browse books",
                  on_click=lambda: st.session_state.update({"page": "Browse Books"}))
    else:
        name = st.text_input("Customer name")
        email = st.text_input("Email (optional)")

        st.caption(
            "Select GST only after verifying the applicable tax treatment. "
            "The default is 0% for this demonstration."
        )
        gst_rate = st.selectbox("GST rate", [0, 5, 12, 18, 28], index=0)

        bill = calculate_bill(st.session_state.cart, gst_rate)

        st.divider()
        st.markdown("### THE BUSINESS BOOKSHOP")
        st.caption(datetime.now().strftime("Receipt date: %d %B %Y, %I:%M %p"))
        st.write("Customer:", name or "Guest")
        if email:
            st.write("Email:", email)

        # FOR LOOP: itemised receipt.
        lines = [
            "THE BUSINESS BOOKSHOP",
            "DEMONSTRATION RECEIPT",
            f"Date: {datetime.now().strftime('%d-%m-%Y %H:%M')}",
            f"Customer: {name or 'Guest'}",
            f"Email: {email or 'Not provided'}",
            "-" * 35
        ]

        for book_id, quantity in st.session_state.cart.items():
            book = BOOKS.get(book_id, {})
            if book:
                price = get_price(book)
                line_total = price["selling_price"] * quantity
                st.write(f"**{book.get('title', 'Book')} × {quantity}**")
                st.write(rupees(line_total))
                lines.append(f"{book.get('title', 'Book')} x {quantity}: {rupees(line_total)}")

        st.divider()
        st.write("Total MRP:", rupees(bill["mrp"]))
        st.write("Discount:", "-" + rupees(bill["discount"]))
        st.write("Subtotal:", rupees(bill["subtotal"]))
        st.write(f"GST ({gst_rate}%):", rupees(bill["gst"]))
        st.markdown(f"## Total payable: {rupees(bill['total'])}")

        lines.extend([
            "-" * 35,
            f"MRP: {rupees(bill['mrp'])}",
            f"Discount: -{rupees(bill['discount'])}",
            f"Subtotal: {rupees(bill['subtotal'])}",
            f"GST ({gst_rate}%): {rupees(bill['gst'])}",
            f"TOTAL: {rupees(bill['total'])}",
            "Demonstration receipt only; no payment collected."
        ])

        st.download_button(
            "📄 Download bill",
            data="\n".join(lines),
            file_name="business_bookshop_bill.txt",
            mime="text/plain",
            use_container_width=True
        )

        if st.button("Confirm demo order", use_container_width=True):
            if not name.strip():
                st.warning("Please enter your name.")
            else:
                st.session_state.last_order = {
                    "name": name,
                    "total": bill["total"],
                    "date": datetime.now().strftime("%d %b %Y, %I:%M %p")
                }
                st.success("Demo order confirmed. No payment was taken.")

        if st.session_state.last_order:
            order = st.session_state.last_order
            st.info(
                f"Last demo order: {order.get('name', 'Guest')} — "
                f"{rupees(order.get('total', 0))}"
            )

            if st.button("Start new shopping session"):
                st.session_state.cart = {}
                st.session_state.last_order = None
                st.session_state.page = "Home"
                st.rerun()


# ======================== ABOUT US ========================

elif st.session_state.page == "About Us":
    st.markdown("## About The Business Bookshop")

    st.write("""
    The Business Bookshop is a digital bookstore designed for students,
    graduates and aspiring professionals. It combines academic textbooks,
    university curriculum guides and competitive examination resources in
    one convenient platform.

    Discover books for economics, business, finance, accounting, mathematics,
    Python, law and media studies. Explore preparation materials for CAT,
    GMAT, GRE, UGC NET and GATE, and consult links to official syllabuses.

    The website features book-cover images, search and category filters,
    discounted prices, a shopping cart and a downloadable demonstration bill.

    Our mission is to make learning resources easier to discover and support
    lifelong learning through a simple, student-friendly experience.
    """)

    st.markdown("### Our promise")
    a, b, c = st.columns(3)
    a.markdown("### 📚 Learning")
    a.write("Resources for curious minds.")
    b.markdown("### 🎯 Preparation")
    b.write("Organised exam-prep collections.")
    c.markdown("### 🌱 Growth")
    c.write("Keep building your knowledge.")

    st.markdown("### Research and official sources")
    for title, url in SOURCES.items():
        st.markdown(f"- [{title}]({url})")


# ======================== FOOTER =========================

st.divider()
st.markdown("""
<div class="footer">
<strong>The Business Bookshop</strong><br>
Read better. Learn smarter. Achieve more.<br>
<span style="font-size:12px">
Built with Python and Streamlit | Student project
</span>
</div>
""", unsafe_allow_html=True)
