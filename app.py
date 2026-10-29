
import streamlit as st
import requests

# --------------------------------------------------
# PAGE SETUP
# --------------------------------------------------
st.set_page_config(
    page_title="PageNest | The Global Bookstore",
    page_icon="📚",
    layout="wide",
)

st.markdown("""
<style>
    .stApp {
        background-color: #faf8f4;
        color: #252c28;
    }
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
        max-width: 1500px;
    }
    h1, h2, h3 {
        color: #243c35;
    }
    .brand {
        font-size: 42px;
        font-weight: 800;
        letter-spacing: -1.5px;
        color: #244c3e;
        margin-bottom: 0;
    }
    .tagline {
        color: #6c756e;
        font-size: 16px;
        margin-top: -5px;
        margin-bottom: 18px;
    }
    .book-title {
        font-size: 17px;
        font-weight: 700;
        min-height: 48px;
        color: #243c35;
    }
    .price {
        font-size: 19px;
        font-weight: 700;
        color: #244c3e;
    }
    div[data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 14px;
        border-color: #e5e2d9;
        background-color: #fffefa;
    }
    div.stButton > button {
        border-radius: 9px;
        border: 1px solid #d9e1d9;
    }
    div.stButton > button[kind="primary"] {
        background-color: #244c3e;
        color: white;
    }
    div[data-testid="stMetric"] {
        background: #f0f3ec;
        border-radius: 10px;
        padding: 10px;
    }
    [data-testid="stImage"] img {
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# BOOK CATALOGUE
# --------------------------------------------------
BOOKS = [
    {
        "id": "B01", "title": "Principles of Microeconomics",
        "author": "N. Gregory Mankiw", "category": "Economics",
        "exam": "University", "price": 650,
        "image": "https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=500",
        "description": "Demand, supply, markets and consumer choice."
    },
    {
        "id": "B02", "title": "Principles of Macroeconomics",
        "author": "N. Gregory Mankiw", "category": "Economics",
        "exam": "University", "price": 650,
        "image": "https://images.unsplash.com/photo-1507842217343-583bb7270b66?w=500",
        "description": "Inflation, GDP, unemployment and economic growth."
    },
    {
        "id": "B03", "title": "Quantitative Aptitude",
        "author": "R. S. Aggarwal", "category": "Quantitative Aptitude",
        "exam": "CAT / SSC / Banking", "price": 720,
        "image": "https://images.unsplash.com/photo-1509228468518-180dd4864904?w=500",
        "description": "Arithmetic, algebra and quantitative practice."
    },
    {
        "id": "B04", "title": "How to Prepare for CAT Quantitative Aptitude",
        "author": "Arun Sharma", "category": "CAT Preparation",
        "exam": "CAT / MBA", "price": 850,
        "image": "https://images.unsplash.com/photo-1516979187457-637abb4f9353?w=500",
        "description": "Quantitative aptitude practice for MBA entrance exams."
    },
    {
        "id": "B05", "title": "Word Power Made Easy",
        "author": "Norman Lewis", "category": "English",
        "exam": "CAT / GRE / GMAT", "price": 300,
        "image": "https://images.unsplash.com/photo-1512820790803-83ca734da794?w=500",
        "description": "Build vocabulary through structured exercises."
    },
    {
        "id": "B06", "title": "Official Guide to the GMAT",
        "author": "GMAC", "category": "GMAT Preparation",
        "exam": "GMAT", "price": 1200,
        "image": "https://images.unsplash.com/photo-1519682337058-a94d519337bc?w=500",
        "description": "Official preparation material. Check the current edition."
    },
    {
        "id": "B07", "title": "Official GRE Preparation",
        "author": "ETS", "category": "GRE Preparation",
        "exam": "GRE", "price": 1500,
        "image": "https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?w=500",
        "description": "GRE practice and preparation resources."
    },
    {
        "id": "B08", "title": "UGC NET Teaching and Research Aptitude",
        "author": "Exam Preparation Reference", "category": "UGC NET",
        "exam": "UGC NET", "price": 500,
        "image": "https://images.unsplash.com/photo-1497633762265-9d179a990aa6?w=500",
        "description": "Teaching aptitude, research aptitude and general paper."
    },
    {
        "id": "B09", "title": "GATE Computer Science",
        "author": "Technical Exam Reference", "category": "GATE",
        "exam": "GATE", "price": 950,
        "image": "https://images.unsplash.com/photo-1515879218367-8466d910aaa4?w=500",
        "description": "Computer science concepts and practice."
    },
    {
        "id": "B10", "title": "Indian Polity",
        "author": "M. Laxmikanth", "category": "General Studies",
        "exam": "UPSC / State PSC", "price": 850,
        "image": "https://images.unsplash.com/photo-1505664194779-8beaceb93744?w=500",
        "description": "A popular reference for Indian polity preparation."
    },
    {
        "id": "B11", "title": "Financial Accounting",
        "author": "Accounting Reference", "category": "Accounting",
        "exam": "BBA / MBA", "price": 600,
        "image": "https://images.unsplash.com/photo-1455390582262-044cdead277a?w=500",
        "description": "Journal entries, ledgers and financial statements."
    },
    {
        "id": "B12", "title": "Business Statistics",
        "author": "Statistics Reference", "category": "Statistics",
        "exam": "BBA / MBA", "price": 550,
        "image": "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=500",
        "description": "Probability, statistical methods and data analysis."
    },
    {
        "id": "B13", "title": "Business Mathematics",
        "author": "Mathematics Reference", "category": "Mathematics",
        "exam": "BBA / MBA", "price": 480,
        "image": "https://images.unsplash.com/photo-1497633762265-9d179a990aa6?w=500",
        "description": "Equations, matrices and financial mathematics."
    },
    {
        "id": "B14", "title": "Principles of Management",
        "author": "Management Reference", "category": "Management",
        "exam": "BBA / MBA / UGC NET", "price": 550,
        "image": "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?w=500",
        "description": "Planning, leadership, organisation and control."
    },
    {
        "id": "B15", "title": "Business Studies",
        "author": "Business Studies Reference", "category": "Business",
        "exam": "School / University", "price": 450,
        "image": "https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?w=500",
        "description": "Business organisations and commercial activities."
    },
    {
        "id": "B16", "title": "Legal Aspects of Business",
        "author": "Business Law Reference", "category": "Law",
        "exam": "BBA / MBA", "price": 500,
        "image": "https://images.unsplash.com/photo-1505664194779-8beaceb93744?w=500",
        "description": "Contracts, company law and business regulations."
    },
    {
        "id": "B17", "title": "Python Crash Course",
        "author": "Eric Matthes", "category": "Programming",
        "exam": "University / Programming", "price": 900,
        "image": "https://images.unsplash.com/photo-1515879218367-8466d910aaa4?w=500",
        "description": "A practical introduction to Python programming."
    },
    {
        "id": "B18", "title": "A Modern Approach to Reasoning",
        "author": "R. S. Aggarwal", "category": "Reasoning",
        "exam": "CAT / SSC / Banking", "price": 650,
        "image": "https://images.unsplash.com/photo-1519682337058-a94d519337bc?w=500",
        "description": "Logical reasoning concepts and practice questions."
    },
    {
        "id": "B19", "title": "The Official Cambridge Guide to IELTS",
        "author": "Cambridge English", "category": "English",
        "exam": "IELTS", "price": 1000,
        "image": "https://images.unsplash.com/photo-1512820790803-83ca734da794?w=500",
        "description": "Practice for IELTS listening, reading, writing and speaking."
    },
    {
        "id": "B20", "title": "The Official Digital SAT Study Guide",
        "author": "College Board", "category": "SAT Preparation",
        "exam": "SAT", "price": 1100,
        "image": "https://images.unsplash.com/photo-1516979187457-637abb4f9353?w=500",
        "description": "Check the publisher for current digital SAT resources."
    },
    {
        "id": "B21", "title": "A Brief History of Modern India",
        "author": "Spectrum", "category": "General Studies",
        "exam": "UPSC / State PSC", "price": 600,
        "image": "https://images.unsplash.com/photo-1507842217343-583bb7270b66?w=500",
        "description": "Modern Indian history for competitive exam preparation."
    },
    {
        "id": "B22", "title": "Business Communication",
        "author": "Communication Reference", "category": "Communication",
        "exam": "BBA / MBA", "price": 400,
        "image": "https://images.unsplash.com/photo-1455390582262-044cdead277a?w=500",
        "description": "Writing, speaking, comprehension and workplace communication."
    },
    {
        "id": "B23", "title": "Media, Society and Government",
        "author": "Media Studies Reference", "category": "Media Studies",
        "exam": "University", "price": 450,
        "image": "https://images.unsplash.com/photo-1504711434969-e33886168f5c?w=500",
        "description": "Media, society, institutions and public communication."
    },
]

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------
if "cart" not in st.session_state:
    st.session_state.cart = {}

if "search_results" not in st.session_state:
    st.session_state.search_results = []

if "search_message" not in st.session_state:
    st.session_state.search_message = ""

if "discount" not in st.session_state:
    st.session_state.discount = 0

if "gst" not in st.session_state:
    st.session_state.gst = 0


# --------------------------------------------------
# FUNCTIONS
# --------------------------------------------------
def money(amount):
    return f"₹{amount:,.2f}"


def add_book(book):
    book_id = book["id"]

    if book_id in st.session_state.cart:
        st.session_state.cart[book_id]["qty"] += 1
    else:
        st.session_state.cart[book_id] = {**book, "qty": 1}


def get_bill():
    subtotal = sum(
        item["price"] * item["qty"]
        for item in st.session_state.cart.values()
    )

    discount = subtotal * st.session_state.discount / 100
    taxable = subtotal - discount
    gst_amount = taxable * st.session_state.gst / 100
    total = taxable + gst_amount

    return {
        "subtotal": subtotal,
        "discount": discount,
        "taxable": taxable,
        "gst": gst_amount,
        "total": total,
        "count": sum(
            item["qty"] for item in st.session_state.cart.values()
        ),
    }


@st.cache_data(ttl=1800, show_spinner=False)
def online_search(query):
    url = "https://www.googleapis.com/books/v1/volumes"
    response = requests.get(
        url,
        params={
            "q": query,
            "maxResults": 20,
            "orderBy": "relevance",
            "printType": "books",
        },
        timeout=10,
    )
    response.raise_for_status()
    data = response.json()

    books = []

    for item in data.get("items", []):
        info = item.get("volumeInfo", {})
        images = info.get("imageLinks", {})

        books.append({
            "id": "ONLINE-" + item.get("id", ""),
            "title": info.get("title", "Untitled book"),
            "author": ", ".join(info.get("authors", ["Author not listed"])),
            "category": ", ".join(info.get("categories", ["Global Library"])),
            "exam": "Online discovery",
            "price": 399,
            "image": images.get("thumbnail", ""),
            "description": info.get(
                "description", "Discover this title in the global book index."
            ),
            "link": info.get("infoLink", ""),
        })

    return books


def book_card(book, key_prefix):
    with st.container(border=True):
        image_url = book.get("image", "")

        if image_url:
            st.image(image_url, use_container_width=True)
        else:
            st.markdown("### 📚")

        st.markdown(
            f'<div class="book-title">{book["title"]}</div>',
            unsafe_allow_html=True,
        )
        st.caption(book["author"])
        st.caption(book.get("category", "Books"))
        st.markdown(
            f'<div class="price">{money(book["price"])}</div>',
            unsafe_allow_html=True,
        )

        if book.get("link"):
            st.markdown(f"[Book details ↗]({book['link']})")

        with st.expander("About this book"):
            st.write(book.get("description", "No description available."))

        if st.button(
            "＋ Add to Bill",
            key=f"{key_prefix}_{book['id']}",
            type="primary",
            use_container_width=True,
        ):
            add_book(book)
            st.rerun()


def render_bill():
    bill = get_bill()

    st.markdown("## 🧾 Your Bill")
    st.caption("Updates automatically as you add books.")

    st.metric("Books selected", bill["count"])
    st.markdown("### Selected items")

    if not st.session_state.cart:
        st.info("Your bill will appear here when you add a book.")
    else:
        for book_id in list(st.session_state.cart.keys()):
            item = st.session_state.cart[book_id]

            with st.container(border=True):
                st.markdown(f"**{item['title']}**")
                st.caption(f"{money(item['price'])} each")

                c1, c2, c3 = st.columns([1, 1, 1])

                with c1:
                    if st.button("−", key=f"minus_{book_id}"):
                        item["qty"] -= 1
                        if item["qty"] <= 0:
                            del st.session_state.cart[book_id]
                        st.rerun()

                with c2:
                    st.markdown(f"**{item['qty']}**")

                with c3:
                    if st.button("＋", key=f"plus_{book_id}"):
                        item["qty"] += 1
                        st.rerun()

                st.write(
                    f"Line total: **{money(item['price'] * item['qty'])}**"
                )

                if st.button("Remove", key=f"remove_{book_id}"):
                    del st.session_state.cart[book_id]
                    st.rerun()

    st.markdown("---")

    st.markdown("### Bill summary")

    st.session_state.discount = st.number_input(
        "Discount (%)",
        min_value=0,
        max_value=100,
        value=int(st.session_state.discount),
        step=1,
        key="discount_widget",
    )

    st.session_state.gst = st.number_input(
        "GST (%)",
        min_value=0,
        max_value=28,
        value=int(st.session_state.gst),
        step=1,
        key="gst_widget",
    )

    # Recalculate after the user changes discount or GST.
    bill = get_bill()

    st.write(f"Subtotal: {money(bill['subtotal'])}")
    st.write(f"Discount: −{money(bill['discount'])}")
    st.write(f"Taxable amount: {money(bill['taxable'])}")
    st.write(f"GST: {money(bill['gst'])}")

    st.markdown(f"## Total: {money(bill['total'])}")

    if st.session_state.cart:
        lines = [
            "PAGENEST — ESTIMATED BILL",
            "=" * 32,
            "",
        ]

        for item in st.session_state.cart.values():
            lines.append(
                f"{item['title']} | Qty {item['qty']} | "
                f"{money(item['price'] * item['qty'])}"
            )

        lines += [
            "",
            f"Subtotal: {money(bill['subtotal'])}",
            f"Discount: -{money(bill['discount'])}",
            f"GST: {money(bill['gst'])}",
            f"TOTAL: {money(bill['total'])}",
            "",
            "Demo bill only. Not a tax invoice or payment receipt.",
        ]

        st.download_button(
            "⬇ Download Bill",
            data="\n".join(lines),
            file_name="pagenest_bill.txt",
            mime="text/plain",
            use_container_width=True,
        )

        if st.button("Clear Bill", use_container_width=True):
            st.session_state.cart = {}
            st.rerun()

    st.caption(
        "Prices are illustrative. Confirm real prices, stock and applicable "
        "taxes before accepting orders."
    )


# --------------------------------------------------
# HOMEPAGE HEADER
# --------------------------------------------------
st.markdown('<div class="brand">PageNest 📚</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="tagline">The Global Bookstore · Find your next chapter.</div>',
    unsafe_allow_html=True,
)

st.markdown(
    "Academic essentials, competitive exam preparation and books "
    "for curious minds — all in one place."
)

# --------------------------------------------------
# SEARCH AND FILTERS
# --------------------------------------------------
with st.form("search_form"):
    search_text = st.text_input(
        "Search",
        placeholder=(
            "Search any book, author, subject or exam — CAT, UPSC, GRE, "
            "GMAT, GATE, UGC NET, Python..."
        ),
    )

    col_a, col_b = st.columns([1, 1])

    with col_a:
        search_button = st.form_submit_button(
            "🔍 Search Books",
            type="primary",
            use_container_width=True,
        )

    with col_b:
        clear_button = st.form_submit_button(
            "Show All Books",
            use_container_width=True,
        )

if clear_button:
    st.session_state.search_results = []
    st.session_state.search_message = ""
    st.rerun()

if search_button:
    if search_text.strip():
        local_matches = [
            book for book in BOOKS
            if all(
                word in " ".join([
                    book["title"],
                    book["author"],
                    book["category"],
                    book["exam"],
                    book["description"],
                ]).lower()
                for word in search_text.lower().split()
            )
        ]

        st.session_state.search_results = local_matches
        st.session_state.search_message = search_text.strip()

        try:
            with st.spinner("Finding more books online..."):
                online_books = online_search(search_text.strip())

            existing = {
                (book["title"].lower(), book["author"].lower())
                for book in local_matches
            }

            for book in online_books:
                identity = (book["title"].lower(), book["author"].lower())
                if identity not in existing:
                    st.session_state.search_results.append(book)
                    existing.add(identity)

        except (requests.RequestException, ValueError):
            st.warning(
                "The online book index is temporarily unavailable. "
                "Showing matching books from the store."
            )
    else:
        st.session_state.search_results = []
        st.session_state.search_message = ""

# --------------------------------------------------
# MAIN PAGE + ALWAYS-VISIBLE BILL
# --------------------------------------------------
st.markdown("---")

catalogue_column, bill_column = st.columns(
    [2.15, 1],
    gap="large",
)

with catalogue_column:
    if st.session_state.search_message:
        st.markdown(f"## Results for “{st.session_state.search_message}”")
        books_to_show = st.session_state.search_results
    else:
        st.markdown("## Discover Your Next Book")
        books_to_show = BOOKS

    category_options = ["All subjects"] + sorted({
        book["category"] for book in books_to_show
    })

    chosen_category = st.selectbox(
        "Browse by subject",
        category_options,
    )

    if chosen_category != "All subjects":
        books_to_show = [
            book for book in books_to_show
            if book["category"] == chosen_category
        ]

    if not books_to_show:
        st.info(
            "No matching books found. Try a shorter search or a different keyword."
        )
    else:
        st.caption(f"{len(books_to_show)} books in this view.")

        # Three neat book cards per row.
        for start in range(0, len(books_to_show), 3):
            row = st.columns(3, gap="medium")

            for offset, col in enumerate(row):
                index = start + offset

                if index < len(books_to_show):
                    with col:
                        book_card(
                            books_to_show[index],
                            key_prefix=f"catalog_{index}",
                        )

with bill_column:
    # This bill stays beside the catalogue on the homepage.
    with st.container(border=True):
        render_bill()

# --------------------------------------------------
# FOOTER
# --------------------------------------------------
st.markdown("---")

footer_left, footer_right = st.columns(2)

with footer_left:
    st.markdown("**PageNest 📚**")
    st.caption("A little corner for every big idea.")

with footer_right:
    st.caption(
        "Online results are for book discovery. Prices shown for online "
        "results are demo prices, not verified retailer prices."
    )
