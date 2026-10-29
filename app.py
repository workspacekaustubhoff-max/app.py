
import streamlit as st
import requests
from urllib.parse import quote_plus

# ---------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------
st.set_page_config(
    page_title="Global Library | Bookstore",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

CURRENCY = "₹"
DEMO_PRICE = 399.0

# Prices throughout this demo store are sample selling prices.
# Verify actual selling prices, GST treatment, and stock before launch.

# ---------------------------------------------------------
# SAMPLE STORE CATALOGUE
# ---------------------------------------------------------
BOOKS = [
    {
        "id": "A01",
        "title": "Principles of Microeconomics",
        "author": "N. Gregory Mankiw",
        "category": "Microeconomics",
        "exam": "University",
        "price": 650,
        "image": "https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=500",
        "description": "Core concepts of demand, supply, markets and consumer choice.",
    },
    {
        "id": "A02",
        "title": "Principles of Macroeconomics",
        "author": "N. Gregory Mankiw",
        "category": "Macroeconomics",
        "exam": "University",
        "price": 650,
        "image": "https://images.unsplash.com/photo-1507842217343-583bb7270b66?w=500",
        "description": "National income, inflation, unemployment and economic growth.",
    },
    {
        "id": "A03",
        "title": "Business Statistics",
        "author": "J. K. Sharma",
        "category": "Business Statistics",
        "exam": "University",
        "price": 550,
        "image": "https://images.unsplash.com/photo-1497633762265-9d179a990aa6?w=500",
        "description": "Statistical methods, probability and data analysis.",
    },
    {
        "id": "A04",
        "title": "Financial Accounting",
        "author": "T. S. Grewal",
        "category": "Financial Accounting",
        "exam": "University",
        "price": 600,
        "image": "https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?w=500",
        "description": "Accounting fundamentals, journal entries and financial statements.",
    },
    {
        "id": "A05",
        "title": "Quantitative Aptitude",
        "author": "R. S. Aggarwal",
        "category": "Quantitative Aptitude",
        "exam": "CAT / Banking / SSC",
        "price": 720,
        "image": "https://images.unsplash.com/photo-1509228468518-180dd4864904?w=500",
        "description": "Arithmetic, algebra, geometry and quantitative practice.",
    },
    {
        "id": "A06",
        "title": "How to Prepare for Quantitative Aptitude for CAT",
        "author": "Arun Sharma",
        "category": "CAT Preparation",
        "exam": "CAT / MBA Entrance",
        "price": 850,
        "image": "https://images.unsplash.com/photo-1516979187457-637abb4f9353?w=500",
        "description": "Practice-oriented preparation for management entrance exams.",
    },
    {
        "id": "A07",
        "title": "Word Power Made Easy",
        "author": "Norman Lewis",
        "category": "English Vocabulary",
        "exam": "CAT / GRE / GMAT / IELTS",
        "price": 300,
        "image": "https://images.unsplash.com/photo-1512820790803-83ca734da794?w=500",
        "description": "Vocabulary-building exercises and word roots.",
    },
    {
        "id": "A08",
        "title": "A Modern Approach to Verbal and Non-Verbal Reasoning",
        "author": "R. S. Aggarwal",
        "category": "Logical Reasoning",
        "exam": "CAT / Banking / SSC",
        "price": 650,
        "image": "https://images.unsplash.com/photo-1519682337058-a94d519337bc?w=500",
        "description": "Reasoning concepts and practice questions.",
    },
    {
        "id": "A09",
        "title": "Business Mathematics",
        "author": "Business Mathematics Reference",
        "category": "Business Mathematics",
        "exam": "University",
        "price": 480,
        "image": "https://images.unsplash.com/photo-1497633762265-9d179a990aa6?w=500",
        "description": "Business calculations, equations, matrices and financial mathematics.",
    },
    {
        "id": "A10",
        "title": "Python Crash Course",
        "author": "Eric Matthes",
        "category": "Python / Programming",
        "exam": "Programming / University",
        "price": 900,
        "image": "https://images.unsplash.com/photo-1515879218367-8466d910aaa4?w=500",
        "description": "Practical introduction to Python programming.",
    },
    {
        "id": "A11",
        "title": "Legal Aspects of Business",
        "author": "Business Law Reference",
        "category": "Business Law",
        "exam": "BBA / MBA",
        "price": 500,
        "image": "https://images.unsplash.com/photo-1505664194779-8beaceb93744?w=500",
        "description": "Contracts, company law and business regulations.",
    },
    {
        "id": "A12",
        "title": "Principles of Management",
        "author": "Management Reference",
        "category": "Management",
        "exam": "BBA / MBA / UGC NET",
        "price": 550,
        "image": "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?w=500",
        "description": "Planning, organising, leadership and control.",
    },
    {
        "id": "A13",
        "title": "Business Studies",
        "author": "Business Studies Reference",
        "category": "Business Studies",
        "exam": "School / University",
        "price": 450,
        "image": "https://images.unsplash.com/photo-1455390582262-044cdead277a?w=500",
        "description": "Business organisation, management and commercial activities.",
    },
    {
        "id": "A14",
        "title": "Written and Verbal Communication",
        "author": "Communication Skills Reference",
        "category": "Communication",
        "exam": "CAT / GMAT / University",
        "price": 400,
        "image": "https://images.unsplash.com/photo-1455390582262-044cdead277a?w=500",
        "description": "Writing, comprehension and professional communication.",
    },
    {
        "id": "A15",
        "title": "Media, Society and Government",
        "author": "Media Studies Reference",
        "category": "Media Studies",
        "exam": "University",
        "price": 450,
        "image": "https://images.unsplash.com/photo-1504711434969-e33886168f5c?w=500",
        "description": "Media institutions, society and public communication.",
    },
    {
        "id": "CAT01",
        "title": "How to Prepare for Data Interpretation for CAT",
        "author": "Arun Sharma",
        "category": "Data Interpretation",
        "exam": "CAT / MBA Entrance",
        "price": 750,
        "image": "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=500",
        "description": "Charts, tables, caselets and data interpretation practice.",
    },
    {
        "id": "CAT02",
        "title": "How to Prepare for Verbal Ability and Reading Comprehension for CAT",
        "author": "Arun Sharma",
        "category": "Verbal Ability",
        "exam": "CAT / MBA Entrance",
        "price": 800,
        "image": "https://images.unsplash.com/photo-1507842217343-583bb7270b66?w=500",
        "description": "Reading comprehension and verbal ability preparation.",
    },
    {
        "id": "GMAT01",
        "title": "Official Guide to the GMAT",
        "author": "GMAC",
        "category": "GMAT Preparation",
        "exam": "GMAT",
        "price": 1200,
        "image": "https://images.unsplash.com/photo-1516979187457-637abb4f9353?w=500",
        "description": "Look for the latest edition aligned with the current GMAT exam.",
    },
    {
        "id": "GRE01",
        "title": "Official GRE Super Power Pack",
        "author": "ETS",
        "category": "GRE Preparation",
        "exam": "GRE",
        "price": 1500,
        "image": "https://images.unsplash.com/photo-1512820790803-83ca734da794?w=500",
        "description": "Official GRE practice materials; verify edition and availability.",
    },
    {
        "id": "NET01",
        "title": "UGC NET Paper 1 Teaching and Research Aptitude",
        "author": "Competitive Exam Reference",
        "category": "UGC NET Paper 1",
        "exam": "UGC NET",
        "price": 500,
        "image": "https://images.unsplash.com/photo-1497633762265-9d179a990aa6?w=500",
        "description": "Teaching aptitude, research aptitude and general paper topics.",
    },
    {
        "id": "NET02",
        "title": "UGC NET Commerce",
        "author": "Commerce Exam Reference",
        "category": "UGC NET Commerce",
        "exam": "UGC NET",
        "price": 650,
        "image": "https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?w=500",
        "description": "Commerce subject preparation; check the current official syllabus.",
    },
    {
        "id": "GATE01",
        "title": "GATE Computer Science and Information Technology",
        "author": "Technical Exam Reference",
        "category": "GATE Computer Science",
        "exam": "GATE",
        "price": 950,
        "image": "https://images.unsplash.com/photo-1515879218367-8466d910aaa4?w=500",
        "description": "Computer science concepts and technical practice.",
    },
    {
        "id": "GATE02",
        "title": "GATE Engineering Mathematics",
        "author": "Engineering Exam Reference",
        "category": "GATE Mathematics",
        "exam": "GATE",
        "price": 700,
        "image": "https://images.unsplash.com/photo-1509228468518-180dd4864904?w=500",
        "description": "Mathematics topics used in several GATE papers.",
    },
    {
        "id": "UPSC01",
        "title": "Indian Polity",
        "author": "M. Laxmikanth",
        "category": "Indian Polity",
        "exam": "UPSC / State PSC",
        "price": 850,
        "image": "https://images.unsplash.com/photo-1505664194779-8beaceb93744?w=500",
        "description": "A widely used reference for Indian polity preparation.",
    },
    {
        "id": "UPSC02",
        "title": "A Brief History of Modern India",
        "author": "Spectrum",
        "category": "Modern History",
        "exam": "UPSC / State PSC",
        "price": 600,
        "image": "https://images.unsplash.com/photo-1507842217343-583bb7270b66?w=500",
        "description": "Modern Indian history preparation.",
    },
    {
        "id": "SAT01",
        "title": "The Official Digital SAT Study Guide",
        "author": "College Board",
        "category": "SAT Preparation",
        "exam": "SAT",
        "price": 1100,
        "image": "https://images.unsplash.com/photo-1516979187457-637abb4f9353?w=500",
        "description": "Check the publisher for the current digital SAT materials.",
    },
    {
        "id": "IELTS01",
        "title": "The Official Cambridge Guide to IELTS",
        "author": "Cambridge English",
        "category": "IELTS Preparation",
        "exam": "IELTS",
        "price": 1000,
        "image": "https://images.unsplash.com/photo-1512820790803-83ca734da794?w=500",
        "description": "Preparation for IELTS listening, reading, writing and speaking.",
    },
    {
        "id": "CLAT01",
        "title": "Legal Aptitude and Logical Reasoning",
        "author": "Law Entrance Reference",
        "category": "Law Entrance",
        "exam": "CLAT / Law Entrance",
        "price": 650,
        "image": "https://images.unsplash.com/photo-1505664194779-8beaceb93744?w=500",
        "description": "Law entrance reasoning and legal aptitude practice.",
    },
]

# ---------------------------------------------------------
# EXAM DIRECTORY AND SYLLABUS LINKS
# ---------------------------------------------------------
EXAMS = {
    "CAT": "https://iimcat.ac.in/",
    "GMAT": "https://www.mba.com/exams/gmat-exam",
    "GRE": "https://www.ets.org/gre.html",
    "UGC NET": "https://ugcnet.nta.nic.in/",
    "GATE": "https://gate2027.iitm.ac.in/exam_papers_and_syllabus",
    "UPSC": "https://upsc.gov.in/",
    "SSC": "https://ssc.gov.in/",
    "IBPS": "https://www.ibps.in/",
    "SAT": "https://satsuite.collegeboard.org/sat",
    "IELTS": "https://ielts.org/",
    "TOEFL": "https://www.ets.org/toefl.html",
    "CLAT": "https://consortiumofnlus.ac.in/",
    "CUET": "https://exams.nta.ac.in/CUET-UG/",
    "JEE": "https://jeemain.nta.nic.in/",
    "NEET": "https://neet.nta.nic.in/",
    "CFA": "https://www.cfainstitute.org/",
}

CURRICULA = {
    "BBA / BBA Honours": {
        "Semester 1": [
            "Principles of Management",
            "Microeconomics",
            "Business Mathematics",
            "Business Communication",
        ],
        "Semester 2": [
            "Macroeconomics",
            "Financial Accounting",
            "Business Statistics",
            "Marketing Management",
        ],
        "Semester 3": [
            "Human Resource Management",
            "Business Law",
            "Organisational Behaviour",
            "Spreadsheet Applications",
        ],
        "Semester 4": [
            "Corporate Finance",
            "Operations Management",
            "Research Methods",
            "Business Analytics",
        ],
        "Semester 5": [
            "Strategic Management",
            "Entrepreneurship",
            "Digital Business",
            "Business Ethics",
        ],
        "Semester 6": [
            "International Business",
            "Investment Analysis",
            "Business Research Project",
        ],
    },
    "MBA": {
        "Semester 1": [
            "Management Principles",
            "Managerial Economics",
            "Financial Accounting",
            "Marketing Management",
            "Business Statistics",
        ],
        "Semester 2": [
            "Corporate Finance",
            "Human Resource Management",
            "Operations Management",
            "Business Research Methods",
            "Management Information Systems",
        ],
        "Semester 3": [
            "Strategic Management",
            "Business Analytics",
            "International Business",
            "Electives / Specialisation",
        ],
        "Semester 4": [
            "Leadership",
            "Corporate Strategy",
            "Industry Project",
            "Electives / Specialisation",
        ],
    },
}

# ---------------------------------------------------------
# SESSION STATE
# ---------------------------------------------------------
if "cart" not in st.session_state:
    st.session_state.cart = {}

if "search_query" not in st.session_state:
    st.session_state.search_query = ""

if "global_results" not in st.session_state:
    st.session_state.global_results = []

if "search_done" not in st.session_state:
    st.session_state.search_done = False

if "page" not in st.session_state:
    st.session_state.page = "Global Search"

if "discount_percent" not in st.session_state:
    st.session_state.discount_percent = 0.0

if "gst_percent" not in st.session_state:
    st.session_state.gst_percent = 0.0


# ---------------------------------------------------------
# HELPER FUNCTIONS
# ---------------------------------------------------------
def money(value):
    return f"₹{value:,.2f}"


def normalise_text(value):
    return str(value or "").strip().lower()


def add_to_cart(book):
    """Add a book or increase its quantity."""
    book_id = str(book["id"])

    if book_id in st.session_state.cart:
        st.session_state.cart[book_id]["qty"] += 1
    else:
        st.session_state.cart[book_id] = {
            **book,
            "qty": 1,
        }


def change_quantity(book_id, difference):
    if book_id not in st.session_state.cart:
        return

    new_quantity = st.session_state.cart[book_id]["qty"] + difference

    if new_quantity <= 0:
        del st.session_state.cart[book_id]
    else:
        st.session_state.cart[book_id]["qty"] = new_quantity


def calculate_bill():
    cart = st.session_state.cart

    subtotal = sum(
        float(item["price"]) * int(item["qty"])
        for item in cart.values()
    )

    discount_percent = float(st.session_state.discount_percent)
    gst_percent = float(st.session_state.gst_percent)

    discount_amount = subtotal * discount_percent / 100
    taxable_amount = subtotal - discount_amount
    gst_amount = taxable_amount * gst_percent / 100
    total = taxable_amount + gst_amount

    return {
        "subtotal": subtotal,
        "discount_percent": discount_percent,
        "discount_amount": discount_amount,
        "taxable_amount": taxable_amount,
        "gst_percent": gst_percent,
        "gst_amount": gst_amount,
        "total": total,
        "items": sum(int(item["qty"]) for item in cart.values()),
    }


@st.cache_data(ttl=3600, show_spinner=False)
def search_google_books(query):
    """
    Search the public Google Books index.
    Search results are for discovery; store prices are demo prices.
    """
    url = "https://www.googleapis.com/books/v1/volumes"

    params = {
        "q": query,
        "maxResults": 20,
        "startIndex": 0,
        "orderBy": "relevance",
        "printType": "books",
    }

    response = requests.get(url, params=params, timeout=12)
    response.raise_for_status()
    data = response.json()

    results = []

    for item in data.get("items", []):
        info = item.get("volumeInfo", {})
        sale_info = item.get("saleInfo", {})

        title = info.get("title", "Untitled book")
        authors = info.get("authors", ["Author not listed"])
        author = ", ".join(authors) if authors else "Author not listed"

        image_links = info.get("imageLinks", {})
        image_url = (
            image_links.get("thumbnail")
            or image_links.get("smallThumbnail")
            or ""
        )

        if image_url.startswith("http://"):
            image_url = "https://" + image_url[len("http://"):]

        book_id = "GB-" + str(item.get("id", title + author))

        results.append({
            "id": book_id,
            "title": title,
            "author": author,
            "category": ", ".join(info.get("categories", [])) or "Global Library",
            "exam": "Global Search",
            "price": DEMO_PRICE,
            "image": image_url,
            "description": info.get("description", "No description provided."),
            "publisher": info.get("publisher", "Publisher not listed"),
            "published": info.get("publishedDate", "Date not listed"),
            "preview": info.get("previewLink", ""),
            "info_link": info.get("infoLink", ""),
            "price_is_demo": True,
        })

    return results, data.get("totalItems", 0)


def search_local_books(query, category_filter="All categories"):
    terms = normalise_text(query).split()
    matches = []

    for book in BOOKS:
        searchable = " ".join([
            book.get("title", ""),
            book.get("author", ""),
            book.get("category", ""),
            book.get("exam", ""),
            book.get("description", ""),
        ]).lower()

        if category_filter != "All categories":
            if category_filter.lower() not in searchable:
                continue

        if all(term in searchable for term in terms):
            matches.append(book)

    return matches


def book_card(book, prefix="book"):
    """Render a book card with a working Add to Cart button."""
    with st.container(border=True):
        col_image, col_details = st.columns([1, 2.7])

        with col_image:
            image_url = book.get("image", "")
            if image_url:
                st.image(image_url, use_container_width=True)
            else:
                st.image(
                    "https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=500",
                    use_container_width=True,
                )

        with col_details:
            st.markdown(f"**{book['title']}**")
            st.caption(f"Author: {book.get('author', 'Not listed')}")
            st.caption(f"Category: {book.get('category', 'General')}")

            description = book.get("description", "No description available.")
            st.write(description[:220] + ("…" if len(description) > 220 else ""))

            st.markdown(f"**Demo store price: {money(float(book['price']))}**")

            if book.get("info_link"):
                st.markdown(f"[View book details ↗]({book['info_link']})")
            elif book.get("preview"):
                st.markdown(f"[View preview ↗]({book['preview']})")

            button_key = f"add_{prefix}_{book['id']}"

            if st.button(
                "＋ Add to Cart",
                key=button_key,
                use_container_width=True,
            ):
                add_to_cart(book)
                st.toast(f"Added: {book['title']}")
                st.rerun()


def render_sidebar_cart():
    """Persistent compact cart and bill summary in the sidebar."""
    with st.sidebar:
        st.markdown("---")
        bill = calculate_bill()

        st.subheader("🛒 Your Cart")
        st.metric("Items in cart", bill["items"])
        st.metric("Running total", money(bill["total"]))

        st.caption("Your bill updates as you add, remove or change quantities.")

        if not st.session_state.cart:
            st.info("Your cart is empty.")
        else:
            with st.expander("View / edit cart items", expanded=True):
                for book_id, item in list(st.session_state.cart.items()):
                    st.markdown(f"**{item['title']}**")
                    st.caption(
                        f"{money(float(item['price']))} × {item['qty']}"
                    )

                    c1, c2, c3 = st.columns([1, 1, 1])

                    with c1:
                        if st.button(
                            "−",
                            key=f"side_minus_{book_id}",
                            use_container_width=True,
                        ):
                            change_quantity(book_id, -1)
                            st.rerun()

                    with c2:
                        st.write(f"**{item['qty']}**")

                    with c3:
                        if st.button(
                            "＋",
                            key=f"side_plus_{book_id}",
                            use_container_width=True,
                        ):
                            change_quantity(book_id, 1)
                            st.rerun()

                    if st.button(
                        "Remove",
                        key=f"side_remove_{book_id}",
                    ):
                        del st.session_state.cart[book_id]
                        st.rerun()

                    st.markdown("---")

        st.markdown("**Bill summary**")
        st.write(f"Subtotal: {money(bill['subtotal'])}")
        st.write(f"Discount: −{money(bill['discount_amount'])}")
        st.write(f"GST: {money(bill['gst_amount'])}")
        st.markdown(f"### Total: {money(bill['total'])}")

        st.markdown("**Bill settings**")
        st.session_state.discount_percent = st.number_input(
            "Discount (%)",
            min_value=0.0,
            max_value=100.0,
            value=float(st.session_state.discount_percent),
            step=1.0,
            key="sidebar_discount_input",
        )
        st.session_state.gst_percent = st.number_input(
            "GST (%)",
            min_value=0.0,
            max_value=28.0,
            value=float(st.session_state.gst_percent),
            step=0.5,
            key="sidebar_gst_input",
        )

        if st.button("Open Full Bill", use_container_width=True):
            st.session_state.page = "Full Bill"
            st.rerun()

        if st.button("Clear Cart", use_container_width=True):
            st.session_state.cart = {}
            st.rerun()


# ---------------------------------------------------------
# SIDEBAR NAVIGATION
# ---------------------------------------------------------
with st.sidebar:
    st.title("📚 Global Library")
    st.caption("Your learning and exam-preparation bookstore")

    pages = [
        "Global Search",
        "Browse Store",
        "Competitive Exams",
        "Syllabus Guides",
        "Full Bill",
        "About",
    ]

    current_page = st.radio(
        "Navigate",
        pages,
        key="page",
    )

    st.markdown("---")
    st.caption("Search books by title, author, subject or exam.")


# Draw the cart in the sidebar on every page.
render_sidebar_cart()


# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------
st.title("📚 Global Library")
st.markdown(
    "### One search bar for academic books and competitive exam preparation"
)
st.write(
    "Discover books for Indian entrance examinations, international tests, "
    "university courses, professional qualifications and general learning."
)

st.info(
    "Store prices are demo prices. Online search results come from the public "
    "Google Books index and do not confirm local stock, edition, or selling price."
)


# ---------------------------------------------------------
# PAGE: GLOBAL SEARCH
# ---------------------------------------------------------
if current_page == "Global Search":
    st.subheader("🔎 Search the Global Book Library")

    with st.form("global_search_form"):
        query = st.text_input(
            "Search all books",
            value=st.session_state.search_query,
            placeholder=(
                "Try CAT, UPSC, GRE, GMAT, GATE, UGC NET, Python, "
                "economics, accounting or an author name..."
            ),
        )

        col1, col2 = st.columns([1, 1])
        with col1:
            search_submitted = st.form_submit_button(
                "🔍 Search Global Library",
                use_container_width=True,
            )
        with col2:
            clear_search = st.form_submit_button(
                "Clear Search",
                use_container_width=True,
            )

    if clear_search:
        st.session_state.search_query = ""
        st.session_state.global_results = []
        st.session_state.search_done = False
        st.rerun()

    if search_submitted:
        st.session_state.search_query = query.strip()
        st.session_state.global_results = []
        st.session_state.search_done = True

        if query.strip():
            with st.spinner("Searching the store and global book index..."):
                try:
                    global_results, total_found = search_google_books(
                        query.strip()
                    )
                    st.session_state.global_results = global_results
                    st.session_state.global_total_found = total_found
                    st.session_state.global_error = ""
                except requests.RequestException:
                    st.session_state.global_error = (
                        "The online book search is temporarily unavailable. "
                        "You can still search the store catalogue below."
                    )
                except (ValueError, KeyError):
                    st.session_state.global_error = (
                        "The online book service returned an unexpected response."
                    )
        else:
            st.warning("Enter a book, subject, author or exam to search.")

    query = st.session_state.search_query

    if st.session_state.get("global_error"):
        st.warning(st.session_state.global_error)

    if st.session_state.search_done and query:
        st.markdown(f"#### Results for: **{query}**")

        local_results = search_local_books(query)

        if local_results:
            st.markdown("### From our store catalogue")
            st.caption(f"{len(local_results)} matching store book(s).")

            for index, book in enumerate(local_results):
                book_card(book, prefix=f"local_{index}")

        else:
            st.caption("No exact match in the store catalogue.")

        global_results = st.session_state.global_results

        if global_results:
            st.markdown("### 🌍 More books from the global index")
            st.caption(
                f"Showing {len(global_results)} online discovery result(s). "
                "The total matching index count may be much larger."
            )

            for index, book in enumerate(global_results):
                # Avoid repeating the same title/author from the store list.
                already_in_store = any(
                    normalise_text(existing["title"]) == normalise_text(book["title"])
                    and normalise_text(existing["author"]) == normalise_text(book["author"])
                    for existing in local_results
                )

                if already_in_store:
                    continue

                book_card(book, prefix=f"global_{index}")

            st.caption(
                "Global results use a temporary demo store price of "
                f"{money(DEMO_PRICE)} when added to the cart. "
                "Edit prices for your real inventory before accepting orders."
            )

        elif not local_results:
            st.warning(
                "No results were found. Try a shorter keyword, exam name, "
                "subject, title or author."
            )

    else:
        st.markdown("### Explore popular searches")

        popular_searches = [
            "CAT preparation",
            "UPSC books",
            "UGC NET Commerce",
            "GATE Computer Science",
            "GMAT",
            "GRE",
            "SAT",
            "IELTS",
            "CLAT",
            "CUET",
            "Python programming",
            "Business Mathematics",
        ]

        columns = st.columns(3)

        for index, search_term in enumerate(popular_searches):
            with columns[index % 3]:
                if st.button(
                    f"🔎 {search_term}",
                    key=f"popular_{index}",
                    use_container_width=True,
                ):
                    st.session_state.search_query = search_term
                    st.session_state.search_done = True

                    try:
                        results, total_found = search_google_books(search_term)
                        st.session_state.global_results = results
                        st.session_state.global_total_found = total_found
                        st.session_state.global_error = ""
                    except requests.RequestException:
                        st.session_state.global_results = []
                        st.session_state.global_error = (
                            "Online search is unavailable right now."
                        )

                    st.rerun()

        st.markdown("---")
        st.markdown("### Store highlights")

        featured = BOOKS[:6]
        featured_columns = st.columns(3)

        for index, book in enumerate(featured):
            with featured_columns[index % 3]:
                st.image(book["image"], use_container_width=True)
                st.markdown(f"**{book['title']}**")
                st.caption(book["category"])
                st.write(money(book["price"]))

                if st.button(
                    "Add to Cart",
                    key=f"featured_{book['id']}",
                    use_container_width=True,
                ):
                    add_to_cart(book)
                    st.rerun()


# ---------------------------------------------------------
# PAGE: BROWSE STORE
# ---------------------------------------------------------
elif current_page == "Browse Store":
    st.subheader("📖 Browse Store Catalogue")

    all_categories = sorted({book["category"] for book in BOOKS})
    all_exams = sorted({book["exam"] for book in BOOKS})

    col1, col2, col3 = st.columns(3)

    with col1:
        category_choice = st.selectbox(
            "Subject / category",
            ["All categories"] + all_categories,
        )

    with col2:
        exam_choice = st.selectbox(
            "Exam / purpose",
            ["All exams"] + all_exams,
        )

    with col3:
        sort_choice = st.selectbox(
            "Sort by",
            ["Recommended", "Price: low to high", "Price: high to low", "Title A–Z"],
        )

    filtered_books = BOOKS[:]

    if category_choice != "All categories":
        filtered_books = [
            book for book in filtered_books
            if book["category"] == category_choice
        ]

    if exam_choice != "All exams":
        filtered_books = [
            book for book in filtered_books
            if book["exam"] == exam_choice
        ]

    if sort_choice == "Price: low to high":
        filtered_books.sort(key=lambda book: book["price"])
    elif sort_choice == "Price: high to low":
        filtered_books.sort(key=lambda book: book["price"], reverse=True)
    elif sort_choice == "Title A–Z":
        filtered_books.sort(key=lambda book: book["title"].lower())

    st.caption(f"{len(filtered_books)} book(s) in this view.")

    for index in range(0, len(filtered_books), 2):
        columns = st.columns(2)

        for offset, column in enumerate(columns):
            book_index = index + offset
            if book_index < len(filtered_books):
                with column:
                    book_card(
                        filtered_books[book_index],
                        prefix=f"browse_{book_index}",
                    )


# ---------------------------------------------------------
# PAGE: COMPETITIVE EXAMS
# ---------------------------------------------------------
elif current_page == "Competitive Exams":
    st.subheader("🎯 Competitive Exam Directory")

    st.write(
        "Choose an examination to open its official website. "
        "Use the global search to discover related preparation books."
    )

    exam_names = list(EXAMS.keys())
    columns = st.columns(3)

    for index, exam_name in enumerate(exam_names):
        with columns[index % 3]:
            with st.container(border=True):
                st.markdown(f"**{exam_name}**")
                st.markdown(f"[Official website ↗]({EXAMS[exam_name]})")

                if st.button(
                    f"Find {exam_name} books",
                    key=f"exam_search_{exam_name}",
                    use_container_width=True,
                ):
                    st.session_state.search_query = exam_name
                    st.session_state.search_done = True

                    try:
                        results, total_found = search_google_books(exam_name)
                        st.session_state.global_results = results
                        st.session_state.global_total_found = total_found
                        st.session_state.global_error = ""
                    except requests.RequestException:
                        st.session_state.global_results = []
                        st.session_state.global_error = (
                            "Online search is unavailable right now."
                        )

                    st.session_state.page = "Global Search"
                    st.rerun()


# ---------------------------------------------------------
# PAGE: SYLLABUS GUIDES
# ---------------------------------------------------------
elif current_page == "Syllabus Guides":
    st.subheader("🎓 BBA Honours and MBA Syllabus Guides")

    st.warning(
        "These are illustrative subject structures, not an official syllabus "
        "for every university. Courses and semester order vary by institution. "
        "Check your university's current curriculum before purchasing books."
    )

    selected_program = st.selectbox(
        "Select programme",
        list(CURRICULA.keys()),
    )

    semester_data = CURRICULA[selected_program]

    for semester, subjects in semester_data.items():
        with st.expander(semester, expanded=False):
            for subject in subjects:
                st.write(f"• {subject}")

                if st.button(
                    f"Search books: {subject}",
                    key=f"syllabus_{selected_program}_{semester}_{subject}",
                ):
                    st.session_state.search_query = subject
                    st.session_state.search_done = True

                    try:
                        results, total_found = search_google_books(subject)
                        st.session_state.global_results = results
                        st.session_state.global_total_found = total_found
                        st.session_state.global_error = ""
                    except requests.RequestException:
                        st.session_state.global_results = []
                        st.session_state.global_error = (
                            "Online search is unavailable right now."
                        )

                    st.session_state.page = "Global Search"
                    st.rerun()

    st.markdown("---")
    st.markdown("### Official exam syllabus links")

    for exam_name, url in EXAMS.items():
        st.markdown(f"- [{exam_name} official website ↗]({url})")


# ---------------------------------------------------------
# PAGE: FULL BILL
# ---------------------------------------------------------
elif current_page == "Full Bill":
    st.subheader("🧾 Your Detailed Bill")

    bill = calculate_bill()

    st.write("Review your selected books, quantities and estimated charges.")

    if not st.session_state.cart:
        st.info("Your cart is empty. Add books from Global Search or Browse Store.")
    else:
        rows = []

        for item in st.session_state.cart.values():
            price = float(item["price"])
            quantity = int(item["qty"])

            rows.append({
                "Book": item["title"],
                "Author": item.get("author", "Not listed"),
                "Unit price": money(price),
                "Quantity": quantity,
                "Line total": money(price * quantity),
            })

        st.dataframe(
            rows,
            use_container_width=True,
            hide_index=True,
        )

        st.markdown("---")
        left, right = st.columns([1.2, 1])

        with right:
            st.markdown("### Bill breakdown")
            st.write(f"Items: {bill['items']}")
            st.write(f"Subtotal: {money(bill['subtotal'])}")
            st.write(
                f"Discount ({bill['discount_percent']:.1f}%): "
                f"−{money(bill['discount_amount'])}"
            )
            st.write(f"Taxable amount: {money(bill['taxable_amount'])}")
            st.write(
                f"GST ({bill['gst_percent']:.1f}%): "
                f"{money(bill['gst_amount'])}"
            )
            st.markdown(f"## Total payable: {money(bill['total'])}")

        with left:
            st.markdown("### Before checkout")
            st.write("- Confirm book editions and availability.")
            st.write("- Confirm actual selling prices.")
            st.write("- Verify applicable GST and invoicing requirements.")
            st.write("- This demo does not process payments.")

        st.markdown("---")

        if st.button("Prepare Printable Bill", type="primary"):
            bill_text = [
                "GLOBAL LIBRARY — ESTIMATED BILL",
                "=" * 38,
                "",
            ]

            for item in st.session_state.cart.values():
                bill_text.append(
                    f"{item['title']} | Qty: {item['qty']} | "
                    f"{money(float(item['price']) * int(item['qty']))}"
                )

            bill_text.extend([
                "",
                f"Subtotal: {money(bill['subtotal'])}",
                f"Discount: -{money(bill['discount_amount'])}",
                f"Taxable amount: {money(bill['taxable_amount'])}",
                f"GST: {money(bill['gst_amount'])}",
                f"TOTAL: {money(bill['total'])}",
                "",
                "Estimated bill only. Not a tax invoice or payment receipt.",
            ])

            st.download_button(
                "⬇️ Download Bill as Text",
                data="\n".join(bill_text),
                file_name="global_library_bill.txt",
                mime="text/plain",
                use_container_width=True,
            )


# ---------------------------------------------------------
# PAGE: ABOUT
# ---------------------------------------------------------
elif current_page == "About":
    st.subheader("About Global Library")

    st.write(
        "Global Library is a bookstore prototype for academic learning, "
        "competitive exam preparation and professional development."
    )

    st.markdown("### Features")
    st.write("- Search the store catalogue and discover additional books online.")
    st.write("- Explore preparation books for Indian and international exams.")
    st.write("- Add books to a cart and update quantities.")
    st.write("- View a running bill in the sidebar.")
    st.write("- Calculate sample discounts, GST and the estimated total.")
    st.write("- Download a text version of the bill.")

    st.markdown("### Important information")
    st.write(
        "Online book discovery uses the public Google Books API. "
        "It does not search every publisher, retailer, library or book ever "
        "published. Availability and cover images depend on the data returned "
        "by the service."
    )
    st.write(
        "This is a prototype, not a live ecommerce checkout. Sample prices, "
        "tax settings, inventory, payment processing and tax-compliant invoices "
        "must be configured before using it for real sales."
    )

st.markdown("---")
st.caption(
    "Global Library • Search, discover and learn. "
    "All sample store prices are illustrative."
)
