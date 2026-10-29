import streamlit as st
import urllib.parse
import urllib.request
import json
import re
import io
import uuid
from difflib import SequenceMatcher
from datetime import date, timedelta

st.set_page_config(page_title="PageNest | Books & Learning", page_icon="📚", layout="wide")

# ----------------------- STYLE -----------------------
st.markdown("""
<style>
.stApp,[data-testid="stAppViewContainer"],[data-testid="stMain"],[data-testid="stHeader"]{
 background:#F5F7FB!important;color:#172033!important}
.block-container{max-width:1450px;padding-top:1.4rem;padding-bottom:3rem}
h1,h2,h3,h4,p,label,li,[data-testid="stMarkdownContainer"],
[data-testid="stWidgetLabel"],[data-testid="stCaptionContainer"]{color:#26344B!important}
[data-testid="stSidebar"]{background:#E8EEF7!important;border-right:1px solid #D6DFEC}
[data-testid="stSidebar"] *{color:#24334B!important}
.stTextInput input,.stTextArea textarea,.stNumberInput input{
 background:#fff!important;color:#172033!important;-webkit-text-fill-color:#172033!important;
 border:1px solid #C8D3E2!important;border-radius:8px!important;caret-color:#2458A6!important}
.stTextInput input::placeholder,.stTextArea textarea::placeholder{color:#758198!important;-webkit-text-fill-color:#758198!important;opacity:1!important}
[data-baseweb="select"]>div{background:#fff!important;color:#172033!important;border-color:#C8D3E2!important}
[data-baseweb="select"] input{color:#172033!important;-webkit-text-fill-color:#172033!important}
[data-baseweb="popover"],[data-baseweb="menu"],[role="listbox"],[role="option"]{background:#fff!important;color:#172033!important}
[data-testid="stForm"]{background:#fff!important;border:1px solid #DDE5EF!important;border-radius:14px!important;padding:22px!important}
[data-testid="stForm"] label,[data-testid="stForm"] [data-testid="stWidgetLabel"],
[data-testid="stForm"] [data-testid="stMarkdownContainer"]{color:#26344B!important}
.stButton>button,.stFormSubmitButton>button,.stDownloadButton>button{
 background:#2458A6!important;color:#fff!important;border:1px solid #2458A6!important;
 border-radius:9px!important;font-weight:600!important;min-height:2.45rem}
.stButton>button *, .stFormSubmitButton>button *, .stDownloadButton>button *{color:#fff!important}
.stButton>button:hover,.stFormSubmitButton>button:hover{background:#183F7C!important}
[data-testid="stVerticalBlockBorderWrapper"]{background:#fff!important;border-color:#DDE5EF!important;border-radius:14px!important}
[data-testid="stMetric"]{background:#fff!important;padding:15px;border:1px solid #DDE5EF;border-radius:12px}
[data-testid="stMetricLabel"],[data-testid="stMetricValue"]{color:#172033!important}
.hero{background:linear-gradient(120deg,#17345E,#3268A8);border-radius:18px;padding:30px;margin-bottom:24px}
.hero h1{color:#fff!important;font-size:clamp(30px,4vw,42px);margin-bottom:8px}
.hero p{color:#EDF4FF!important}
.pill{display:inline-block;background:#EAF1FF;color:#214E91!important;border-radius:20px;padding:5px 9px;font-size:11px;font-weight:700}
.book-title{color:#172033!important;font-size:16px;font-weight:700;min-height:42px}
.book-author{color:#64718A!important;font-size:13px;min-height:35px}
.book-price{color:#173F7A!important;font-size:21px;font-weight:700;margin:8px 0}
hr{border-color:#DDE5EF!important}
.footer{margin-top:35px;padding:22px;text-align:center;border-radius:14px;background:#17345E;color:#fff!important}
.footer *{color:#fff!important}
[data-testid="stChatMessage"]{background:#fff!important;border:1px solid #DDE5EF;border-radius:12px}
</style>
""", unsafe_allow_html=True)

# ----------------------- CATALOGUE -----------------------
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
BOOKS = [{"id":i+1,"title":r[0],"author":r[1],"category":r[2],"price":r[3],"stock":r[4]} for i,r in enumerate(RAW_BOOKS)]
PAGES = ["Catalogue","Book Bundles","Shopping Cart","Checkout","Find a Book"]

# ----------------------- SESSION / NAV FIX -----------------------
if "page" not in st.session_state or st.session_state.page not in PAGES:
    st.session_state.page = "Catalogue"
if "navigation_radio" not in st.session_state:
    st.session_state.navigation_radio = st.session_state.page
if "cart" not in st.session_state: st.session_state.cart = {}
if "last_order" not in st.session_state: st.session_state.last_order = None
if "invoice_id" not in st.session_state: st.session_state.invoice_id = None
if "find_book_title" not in st.session_state: st.session_state.find_book_title = ""
if "bundle_discount" not in st.session_state: st.session_state.bundle_discount = 0.0
if "support_messages" not in st.session_state:
    st.session_state.support_messages = [{"role":"assistant","content":"Hi! I'm PageNest Help. Ask me about books, bundles, discounts, checkout, or unavailable titles. This demo doesn't process payments."}]

def go(page):
    if page in PAGES:
        st.session_state.page = page
    st.rerun()

def get_book(book_id):
    return next(b for b in BOOKS if b["id"] == book_id)

def cart_count():
    return sum(st.session_state.cart.values())

def subtotal():
    return sum(get_book(i)["price"] * q for i,q in st.session_state.cart.items())

def norm(value):
    return " ".join(re.sub(r"[^a-zA-Z0-9 ]"," ",str(value).lower()).split())

def similarity(a,b):
    return SequenceMatcher(None,norm(a),norm(b)).ratio()

def add_to_cart(book_id, quantity=1):
    book=get_book(book_id)
    current=st.session_state.cart.get(book_id,0)
    if current+quantity>book["stock"]:
        st.warning("Sorry, that is more than the available demo stock.")
    else:
        st.session_state.cart[book_id]=current+quantity
        st.toast("Added to your cart!")

@st.cache_data(ttl=86400,show_spinner=False)
def book_cover(title,author):
    def get_json(url):
        req=urllib.request.Request(url,headers={"User-Agent":"PageNestBookstore/1.0"})
        with urllib.request.urlopen(req,timeout=4) as response:
            return json.loads(response.read().decode("utf-8"))
    try:
        url="https://www.googleapis.com/books/v1/volumes?"+urllib.parse.urlencode({
            "q":f'intitle:"{title}" inauthor:"{author}"',"maxResults":8,"printType":"books"})
        for item in get_json(url).get("items",[]):
            info=item.get("volumeInfo",{})
            if similarity(title,info.get("title",""))<0.58: continue
            authors=info.get("authors",[])
            if authors and not any(similarity(author,n)>0.45 for n in authors): continue
            links=info.get("imageLinks",{})
            image=links.get("large") or links.get("medium") or links.get("thumbnail") or links.get("smallThumbnail")
            if image: return image.replace("http://","https://")
    except Exception: pass
    try:
        url="https://openlibrary.org/search.json?"+urllib.parse.urlencode({
            "title":title,"author":author,"limit":10,"fields":"title,author_name,cover_i"})
        for item in get_json(url).get("docs",[]):
            if similarity(title,item.get("title",""))<0.58: continue
            authors=item.get("author_name",[])
            if authors and not any(similarity(author,n)>0.45 for n in authors): continue
            cover_id=item.get("cover_i")
            if cover_id: return f"https://covers.openlibrary.org/b/id/{cover_id}-L.jpg?default=false"
    except Exception: pass
    return None

def render_book_card(book,prefix="book"):
    with st.container(border=True):
        cover=book_cover(book["title"],book["author"])
        if cover:
            st.image(cover,use_container_width=True)
        else:
            st.markdown('<div style="height:180px;display:flex;align-items:center;justify-content:center;background:#EAF1FB;border-radius:10px;font-size:48px">📚</div>',unsafe_allow_html=True)
            q=urllib.parse.quote(f'{book["title"]} {book["author"]} book cover')
            st.markdown(f"[Search for cover image](https://www.google.com/search?tbm=isch&q={q})")
        st.markdown(f'<div class="book-title">{book["title"]}</div>',unsafe_allow_html=True)
        st.markdown(f'<div class="book-author">{book["author"]}</div>',unsafe_allow_html=True)
        st.caption(book["category"])
        st.markdown(f'<div class="book-price">₹{book["price"]:,.2f}</div>',unsafe_allow_html=True)
        if book["stock"] > 0:
            st.markdown(f'<span class="pill">In stock: {book["stock"]}</span>',unsafe_allow_html=True)
        else:
            st.warning("Currently unavailable")
            st.caption("Estimated restock: 7 days (illustrative estimate)")
        if st.button("Add to Cart",key=f"{prefix}_{book['id']}",use_container_width=True):
            add_to_cart(book["id"])
            st.rerun()
        if book["stock"] == 0:
            q=urllib.parse.quote(book["title"]+" bookstore near me")
            st.markdown(f"[Find nearby stores](https://www.google.com/maps/search/?api=1&query={q})")

def create_invoice_pdf(order,items):
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib.units import mm

    buffer=io.BytesIO()
    doc=SimpleDocTemplate(buffer,pagesize=A4,rightMargin=18*mm,leftMargin=18*mm,topMargin=15*mm,bottomMargin=15*mm)
    styles=getSampleStyleSheet()
    styles.add(ParagraphStyle(name="Brand",parent=styles["Title"],fontName="Helvetica-Bold",fontSize=25,textColor=colors.HexColor("#17345E"),alignment=TA_LEFT,spaceAfter=5))
    styles.add(ParagraphStyle(name="Sub",parent=styles["Normal"],fontSize=9,textColor=colors.HexColor("#64718A"),leading=13))
    styles.add(ParagraphStyle(name="Section",parent=styles["Heading2"],fontSize=12,textColor=colors.HexColor("#17345E"),spaceBefore=12,spaceAfter=6))
    styles.add(ParagraphStyle(name="Right",parent=styles["Normal"],alignment=TA_RIGHT,fontSize=9))
    story=[]
    story.append(Paragraph("PageNest",styles["Brand"]))
    story.append(Paragraph("BOOKS &amp; LEARNING · DIGITAL INVOICE",styles["Sub"]))
    story.append(Spacer(1,10*mm))
    details=[
        [Paragraph("<b>INVOICE NUMBER</b>",styles["Normal"]),order["invoice_id"],
         Paragraph("<b>DATE</b>",styles["Normal"]),order["order_date"]],
        [Paragraph("<b>BILLED TO</b>",styles["Normal"]),Paragraph(order["name"],styles["Normal"]),
         Paragraph("<b>EMAIL</b>",styles["Normal"]),Paragraph(order["email"],styles["Normal"])],
        [Paragraph("<b>PHONE</b>",styles["Normal"]),order["phone"],
         Paragraph("<b>GSTIN</b>",styles["Normal"]),order["gstin"] or "Not provided"],
        [Paragraph("<b>DELIVERY ADDRESS</b>",styles["Normal"]),
         Paragraph(f'{order["address"]}, {order["city"]}, {order["state"]} {order["pincode"]}',styles["Normal"]),
         "", ""],
    ]
    info_table=Table(details,colWidths=[30*mm,55*mm,25*mm,48*mm])
    info_table.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1),colors.HexColor("#F2F5FA")),
        ("BOX",(0,0),(-1,-1),0.6,colors.HexColor("#D5DFEC")),
        ("INNERGRID",(0,0),(-1,-1),0.3,colors.HexColor("#D5DFEC")),
        ("VALIGN",(0,0),(-1,-1),"TOP"),
        ("LEFTPADDING",(0,0),(-1,-1),7),("RIGHTPADDING",(0,0),(-1,-1),7),
        ("TOPPADDING",(0,0),(-1,-1),7),("BOTTOMPADDING",(0,0),(-1,-1),7),
    ]))
    story.append(info_table)
    story.append(Paragraph("Order Details",styles["Section"]))
    rows=[["S.No.","Book / Product","Qty","Rate (INR)","Amount (INR)"]]
    for idx,item in enumerate(items,1):
        rows.append([str(idx),Paragraph(item["title"],styles["Normal"]),str(item["quantity"]),
                     f'₹{item["price"]:,.2f}',f'₹{item["price"]*item["quantity"]:,.2f}'])
    product_table=Table(rows,colWidths=[13*mm,82*mm,15*mm,28*mm,30*mm],repeatRows=1)
    product_table.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,0),colors.HexColor("#17345E")),
        ("TEXTCOLOR",(0,0),(-1,0),colors.white),
        ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),
        ("FONTSIZE",(0,0),(-1,-1),8),
        ("GRID",(0,0),(-1,-1),0.4,colors.HexColor("#D5DFEC")),
        ("VALIGN",(0,0),(-1,-1),"TOP"),
        ("ALIGN",(2,1),(-1,-1),"RIGHT"),
        ("LEFTPADDING",(0,0),(-1,-1),6),("RIGHTPADDING",(0,0),(-1,-1),6),
        ("TOPPADDING",(0,0),(-1,-1),7),("BOTTOMPADDING",(0,0),(-1,-1),7),
    ]))
    story.append(product_table)
    story.append(Spacer(1,8*mm))
    summary=[
        ["Subtotal",f'₹{order["subtotal"]:,.2f}'],
        ["Bundle savings",f'- ₹{order["bundle_discount"]:,.2f}'],
        ["Discount code savings",f'- ₹{order["code_discount"]:,.2f}'],
        ["Total discount",f'- ₹{order["discount"]:,.2f}'],
        ["AMOUNT DUE",f'₹{order["total"]:,.2f}'],
    ]
    summary_table=Table(summary,colWidths=[115*mm,53*mm],hAlign="RIGHT")
    summary_table.setStyle(TableStyle([
        ("ALIGN",(1,0),(1,-1),"RIGHT"),
        ("FONTNAME",(0,-1),(-1,-1),"Helvetica-Bold"),
        ("FONTSIZE",(0,0),(-1,-1),10),
        ("TEXTCOLOR",(0,-1),(-1,-1),colors.HexColor("#17345E")),
        ("BACKGROUND",(0,-1),(-1,-1),colors.HexColor("#EAF1FB")),
        ("LINEABOVE",(0,-1),(-1,-1),1,colors.HexColor("#2458A6")),
        ("TOPPADDING",(0,0),(-1,-1),6),("BOTTOMPADDING",(0,0),(-1,-1),6),
    ]))
    story.append(summary_table)
    story.append(Spacer(1,12*mm))
    story.append(Paragraph("Thank you for choosing PageNest.",ParagraphStyle(name="Thanks",parent=styles["Normal"],fontSize=12,textColor=colors.HexColor("#17345E"),alignment=TA_CENTER)))
    story.append(Spacer(1,3*mm))
    story.append(Paragraph("Demo invoice only. No payment has been processed. Sample prices and stock are illustrative.",ParagraphStyle(name="Note",parent=styles["Normal"],fontSize=8,textColor=colors.HexColor("#64718A"),alignment=TA_CENTER)))
    doc.build(story)
    return buffer.getvalue()

# ----------------------- SIDEBAR -----------------------
with st.sidebar:
    st.markdown("## 📚 PageNest")
    st.caption("Your personal bookstore")
    st.markdown("### Navigate")
    # Give each page's radio a distinct key. Buttons update only st.session_state.page.
    # This avoids modifying the value of an already-instantiated widget.
    nav_key = f"navigation_radio_{st.session_state.page}"
    selected_nav = st.radio("Navigate", PAGES, index=PAGES.index(st.session_state.page), key=nav_key)
    if selected_nav != st.session_state.page:
        st.session_state.page = selected_nav
        st.rerun()

    st.divider()
    st.markdown("### 🔎 Find your next book")
    search=st.text_input("Search title or author",placeholder="e.g. Microeconomics",key="sidebar_search")
    categories=["All Subjects"]+sorted(set(b["category"] for b in BOOKS))
    category=st.selectbox("Subject",categories,key="sidebar_category")
    max_price=st.slider("Maximum price (₹)",min_value=100,max_value=1500,value=1500,step=50)
    availability=st.selectbox("Availability",["All Books","In stock","Out of stock"])
    st.divider()
    st.markdown("### 🛒 Your Cart")
    st.metric("Items",cart_count())
    st.metric("Subtotal",f"₹{subtotal():,.2f}")
    if st.button("Open Shopping Cart",use_container_width=True):
        go("Shopping Cart")

# ----------------------- TOP / PAGE CONTENT -----------------------
if st.session_state.page=="Catalogue":
    st.markdown("""
    <div class="hero">
      <h1>📚 PageNest</h1>
      <p>Books, ideas and possibilities — all in one place.</p>
      <p>Discover textbooks, business classics, competitive exam guides and research resources.</p>
    </div>
    """,unsafe_allow_html=True)
    m1,m2,m3=st.columns(3)
    m1.metric("Books in Catalogue",len(BOOKS))
    m2.metric("Subject Categories",len(set(b["category"] for b in BOOKS)))
    m3.metric("Items in Your Cart",cart_count())
    st.markdown("## Explore the Catalogue")

    filtered=[]
    for book in BOOKS:
        matches_search=not search or search.lower() in (book["title"]+" "+book["author"]).lower()
        matches_category=category=="All Subjects" or book["category"]==category
        matches_price=book["price"]<=max_price
        matches_stock=(availability=="All Books" or (availability=="In stock" and book["stock"]>0) or (availability=="Out of stock" and book["stock"]==0))
        if matches_search and matches_category and matches_price and matches_stock:
            filtered.append(book)
    st.caption(f"Showing {len(filtered)} books.")
    sort_by=st.selectbox("Sort by",["Recommended","Price: Low to High","Price: High to Low","Title A–Z"])
    if sort_by=="Price: Low to High": filtered.sort(key=lambda b:b["price"])
    elif sort_by=="Price: High to Low": filtered.sort(key=lambda b:b["price"],reverse=True)
    elif sort_by=="Title A–Z": filtered.sort(key=lambda b:b["title"].lower())

    if not filtered:
        st.info("No books match those filters. Try changing the search or price.")
    else:
        columns=st.columns(3)
        for idx,book in enumerate(filtered):
            with columns[idx%3]:
                render_book_card(book,"catalogue")

    st.markdown("## Need a book that is not listed?")
    st.write("Use Find a Book to search online sellers and nearby bookstores. Restock dates are estimates, not live supplier promises.")
    if st.button("Find an unavailable book"):
        go("Find a Book")
    if st.button(f"View Cart ({cart_count()})"):
        go("Shopping Cart")

# ----------------------- BOOK BUNDLES -----------------------
elif st.session_state.page=="Book Bundles":
    st.markdown("## 🎁 Book Bundles")
    st.write("Choose a curated bundle and save 10% compared with buying the books individually.")
    bundles=[
        ("Commerce & Business Foundations","For undergraduate commerce and business students",["Principles of Microeconomics","Principles of Macroeconomics","Principles of Management","Financial Accounting"]),
        ("CAT & MBA Starter Bundle","Quantitative aptitude, verbal ability and data interpretation",["How to Prepare for Quantitative Aptitude for CAT","How to Prepare for Data Interpretation for CAT","How to Prepare for Verbal Ability and Reading Comprehension for CAT"]),
        ("JEE Physics & Chemistry Bundle","A starter set for JEE preparation",["Concepts of Physics Volume 1","Physical Chemistry","Concise Inorganic Chemistry"]),
        ("NEET Biology & Science Bundle","Core biology and science preparation",["Objective Biology","Trueman's Elementary Biology","Objective Physics for NEET"]),
        ("UPSC Foundation Bundle","Core polity, economy and modern history books",["Indian Polity","Indian Economy","A Brief History of Modern India"]),
        ("Python & Research Bundle","Programming and academic research foundations",["Python Crash Course","Think Python","Research Methodology"]),
    ]
    cols=st.columns(2)
    for idx,(title,desc,titles) in enumerate(bundles):
        books=[next((b for b in BOOKS if b["title"]==t),None) for t in titles]
        books=[b for b in books if b]
        total=sum(b["price"] for b in books)
        discounted=round(total*.9,2)
        with cols[idx%2]:
            with st.container(border=True):
                st.markdown(f"### {title}")
                st.write(desc)
                for b in books: st.write(f"• {b['title']} — ₹{b['price']:,}")
                st.write(f"Individual total: ₹{total:,.2f}")
                st.markdown(f'<div class="book-price">Bundle price: ₹{discounted:,.2f}</div>',unsafe_allow_html=True)
                if st.button("Add bundle to cart",key="bundle_"+norm(title).replace(" ","_"),use_container_width=True):
                    if all(st.session_state.cart.get(b["id"],0)+1<=b["stock"] for b in books):
                        for b in books: st.session_state.cart[b["id"]]=st.session_state.cart.get(b["id"],0)+1
                        st.session_state.bundle_discount += round(total-discounted,2)
                        st.toast("Bundle added with 10% bundle savings.")
                        st.rerun()
                    else: st.error("A title in this bundle does not have enough demo stock.")

# ----------------------- CART -----------------------
elif st.session_state.page=="Shopping Cart":
    st.markdown("## 🛒 Your Shopping Cart")
    if not st.session_state.cart:
        st.info("Your cart is empty.")
        if st.button("Continue Shopping",use_container_width=True): go("Catalogue")
    else:
        for book_id in list(st.session_state.cart):
            book=get_book(book_id); qty=st.session_state.cart[book_id]
            with st.container(border=True):
                c1,c2,c3,c4=st.columns([4,1,2,1])
                c1.markdown(f"**{book['title']}**"); c1.caption(f"{book['author']} · {book['category']}")
                c2.write(f"Qty: {qty}"); c3.write(f"₹{book['price']*qty:,.2f}")
                if c4.button("Remove",key=f"remove_{book_id}"):
                    del st.session_state.cart[book_id]
                    st.rerun()
                q1,q2,_=st.columns([1,1,4])
                if q1.button("−",key=f"minus_{book_id}"):
                    if qty<=1: del st.session_state.cart[book_id]
                    else: st.session_state.cart[book_id]=qty-1
                    st.rerun()
                if q2.button("+",key=f"plus_{book_id}"):
                    if qty<book["stock"]: st.session_state.cart[book_id]=qty+1; st.rerun()
                    else: st.warning("Maximum demo stock reached.")
        st.divider()
        amount=subtotal()
        bundle_discount=min(st.session_state.bundle_discount,amount)
        st.markdown(f"### Subtotal: ₹{amount:,.2f}")
        if bundle_discount: st.write(f"Bundle discount: −₹{bundle_discount:,.2f}")
        c1,c2=st.columns(2)
        if c1.button("Continue Shopping",use_container_width=True): go("Catalogue")
        if c2.button("Proceed to Checkout",use_container_width=True): go("Checkout")

# ----------------------- CHECKOUT -----------------------
elif st.session_state.page=="Checkout":
    st.markdown("## Checkout & Digital Invoice")
    if not st.session_state.cart:
        st.info("Your cart is empty.")
        if st.button("Browse Books",use_container_width=True): go("Catalogue")
    else:
        amount=subtotal()
        bundle_discount=min(st.session_state.bundle_discount,amount)
        with st.form("checkout_form"):
            st.markdown("### Delivery Details")
            full_name=st.text_input("Full Name *")
            email=st.text_input("Email Address *")
            phone=st.text_input("Phone Number *")
            address=st.text_area("Delivery Address *")
            city=st.text_input("City *")
            state=st.text_input("State *")
            pincode=st.text_input("PIN Code *")
            st.markdown("### Invoice Details")
            gstin=st.text_input("Customer GSTIN (optional)",placeholder="Enter GSTIN if applicable")
            discount_code=st.text_input("Discount Code",placeholder="Try PAGENEST10")
            st.caption("PAGENEST10 gives 10% off after bundle savings. Taxes are not calculated in this demo invoice.")
            submitted=st.form_submit_button("Calculate Total",use_container_width=True)
        if submitted:
            required=[full_name,email,phone,address,city,state,pincode]
            if not all(x.strip() for x in required): st.error("Please complete all required delivery fields.")
            elif not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+",email.strip()): st.error("Please enter a valid email address.")
            elif not re.fullmatch(r"[0-9+\-\s()]{7,20}",phone.strip()): st.error("Please enter a valid phone number.")
            elif not re.fullmatch(r"[0-9A-Za-z -]{4,10}",pincode.strip()): st.error("Please enter a valid PIN code.")
            elif gstin.strip() and not re.fullmatch(r"[0-9A-Z]{15}",gstin.strip().upper()): st.error("GSTIN should contain 15 alphanumeric characters.")
            else:
                after_bundle=max(0,amount-bundle_discount)
                code_discount=round(after_bundle*.10,2) if discount_code.strip().upper()=="PAGENEST10" else 0
                if discount_code.strip() and discount_code.strip().upper()!="PAGENEST10":
                    st.warning("Discount code not recognised. Bundle savings remain applied.")
                cart_snapshot=[{"title":get_book(i)["title"],"quantity":q,"price":get_book(i)["price"]} for i,q in st.session_state.cart.items()]
                st.session_state.last_order={
                    "name":full_name.strip(),"email":email.strip(),"phone":phone.strip(),
                    "address":address.strip(),"city":city.strip(),"state":state.strip(),"pincode":pincode.strip(),
                    "gstin":gstin.strip().upper(),"subtotal":amount,"bundle_discount":bundle_discount,
                    "code_discount":code_discount,"discount":bundle_discount+code_discount,
                    "total":max(0,amount-bundle_discount-code_discount),
                    "order_date":date.today().strftime("%d %B %Y"),
                    "invoice_id":"PN-"+date.today().strftime("%Y%m%d")+"-"+uuid.uuid4().hex[:6].upper(),
                    "cart_snapshot":cart_snapshot
                }
                st.success("Order summary calculated. Download the professional PDF invoice below.")
        order=st.session_state.last_order
        if order:
            st.markdown("### Digital Bill Preview")
            st.write(f"**Invoice:** {order['invoice_id']}  ·  **Date:** {order['order_date']}")
            st.write(f"**Billed to:** {order['name']} · {order['email']}")
            lines=[]
            for item in order["cart_snapshot"]:
                lines.append({"Book":item["title"],"Qty":item["quantity"],"Rate":f"₹{item['price']:,.2f}","Amount":f"₹{item['price']*item['quantity']:,.2f}"})
            st.dataframe(lines,use_container_width=True,hide_index=True)
            a,b,c=st.columns(3)
            a.metric("Subtotal",f"₹{order['subtotal']:,.2f}")
            b.metric("Discount",f"−₹{order['discount']:,.2f}")
            c.metric("Amount Due",f"₹{order['total']:,.2f}")
            try:
                pdf=create_invoice_pdf(order,order["cart_snapshot"])
                st.download_button("⬇ Download Professional PDF Invoice",data=pdf,file_name=f"{order['invoice_id']}.pdf",mime="application/pdf",use_container_width=True)
            except Exception:
                st.error("Could not create PDF invoice. Check that reportlab is installed in requirements.txt.")
            if st.button("Confirm Demo Order",use_container_width=True):
                st.session_state.completed_order=order
                st.session_state.cart={}
                st.session_state.bundle_discount=0.0
                st.session_state.last_order=None
                st.success("Demo order confirmed. No payment was processed.")
                st.rerun()

# ----------------------- FIND BOOK -----------------------
elif st.session_state.page=="Find a Book":
    st.markdown("## 🔎 Find a Book")
    st.write("Search online sellers or locate nearby bookstores.")
    find_title=st.text_input("Book title",value=st.session_state.find_book_title,key="find_title_input")
    find_author=st.text_input("Author (optional)",key="find_author_input")
    search_city=st.text_input("City or area",placeholder="e.g. Sonipat, Haryana",key="find_city_input")
    if st.button("Find Book & Stores",use_container_width=True):
        if not find_title.strip(): st.error("Enter the book title first.")
        else:
            term=" ".join(x for x in [find_title.strip(),find_author.strip()] if x)
            online=urllib.parse.quote(term+" buy book India")
            cover=urllib.parse.quote(term+" book cover")
            place=urllib.parse.quote("bookstores near "+search_city.strip() if search_city.strip() else "bookstores near me")
            st.markdown("### Where to look")
            st.markdown(f"[Search online sellers](https://www.google.com/search?q={online})")
            st.markdown(f"[Search book cover images](https://www.google.com/search?tbm=isch&q={cover})")
            st.markdown(f"[Find bookstores on Google Maps](https://www.google.com/maps/search/?api=1&query={place})")
            eta=date.today()+timedelta(days=7)
            st.markdown("### Estimated restock")
            st.write(f"Illustrative 7-day estimate: **{eta.strftime('%d %B %Y')}**.")
            st.caption("This is not live supplier inventory or a confirmed delivery date. Contact the seller to verify.")

# ----------------------- FOOTER -----------------------
st.markdown("""<div class="footer"><strong>PageNest | Books &amp; Learning</strong><br>
Find your next idea. Discover your next chapter.<br>
<span style="font-size:12px;">Demo bookstore · Sample prices and inventory · No real payments processed</span></div>""",unsafe_allow_html=True)
