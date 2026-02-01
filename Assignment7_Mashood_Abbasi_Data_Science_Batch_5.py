import streamlit as st
import io
import random
from datetime import datetime
#from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Lahore Zoo Ticket System", layout="centered")

COPYRIGHT_TEXT = "© Assignment # 7 | 01-Feb-2026 | Mashood Abbasi | Contact: 03214340555"

# ---------------- HEADER ----------------
st.markdown(
    """
    <div style="background-color:#8B4513;padding:15px;border-radius:10px">
        <h1 style="color:white;text-align:center;">Lahore Zoo</h1>
        <h4 style="color:white;text-align:center;">
            Shahrah Quaid-e-Azam, Lahore<br>
            Phone: 042-31234567
        </h4>
    </div>
    """,
    unsafe_allow_html=True
)

st.divider()

# ---------------- INPUT FORM ----------------
st.subheader("🎟 Ticket Information")

name = st.text_input("Enter Name")
age_input = st.text_input("Enter Age")

nationality = st.radio("Nationality", ["Pakistani", "Foreigner"])
is_student = st.checkbox("Student") if nationality == "Pakistani" else False

# ---------------- VALIDATION & PRICE ----------------
ticket_price = None
error = None

if age_input:
    if not age_input.isdigit():
        error = "Age must be numeric."
    else:
        age = int(age_input)
        if age < 1 or age > 120:
            error = "Age must be between 1 and 120."
        else:
            if nationality == "Foreigner":
                ticket_price = 0 if age < 3 else 50 if age <= 12 else 100
            else:
                if is_student:
                    ticket_price = 100
                else:
                    ticket_price = 0 if age < 3 else 100 if age <= 12 else 300

if error:
    st.error(error)

# ---------------- GENERATE TICKET ----------------
if st.button("Generate Ticket") and not error and name and age_input:

    now = datetime.now()
    ticket_number = f"LZ-{random.randint(100000, 999999)}"

    st.session_state["ticket"] = {
        "ticket_no": ticket_number,
        "name": name,
        "age": age_input,
        "nationality": nationality,
        "student": "Yes" if is_student else "No",
        "price": ticket_price,
        "date": now.strftime("%d-%m-%Y"),
        "time": now.strftime("%I:%M %p")
    }

    st.success("Ticket Generated Successfully!")

# ---------------- PRINTABLE TICKET ----------------
if "ticket" in st.session_state:
    t = st.session_state["ticket"]

    st.divider()
    st.subheader("🖨 Printable Ticket")

    st.markdown(
        f"""
        <div style="border:2px solid #8B4513;padding:15px;border-radius:10px">
        <h3>Lahore Zoo Entry Ticket</h3>
        <b>Ticket No:</b> {t['ticket_no']}<br>
        <b>Date:</b> {t['date']}<br>
        <b>Time:</b> {t['time']}<br>
        <b>Name:</b> {t['name']}<br>
        <b>Age:</b> {t['age']}<br>
        <b>Nationality:</b> {t['nationality']}<br>
        <b>Student:</b> {t['student']}<br>
        
        <b>Price:</b> {"Free" if t['price'] == 0 else t['price']}
        <hr>
        <p style="font-size:12px;text-align:center;">{COPYRIGHT_TEXT}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # ---------------- PDF GENERATION ----------------
    pdf_buffer = io.BytesIO()
    c = canvas.Canvas(pdf_buffer, pagesize=A4)

    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(300, 800, "Lahore Zoo Entry Ticket")

    c.setFont("Helvetica", 12)
    y = 740
    for label, value in [
        ("Ticket No", t['ticket_no']),
        ("Name", t['name']),
        ("Age", t['age']),
        ("Nationality", t['nationality']),
        ("Student", t['student']),
        ("Date", t['date']),
        ("Time", t['time']),
        ("Price", "Free" if t['price'] == 0 else t['price']),
    ]:
        c.drawString(50, y, f"{label}: {value}")
        y -= 20

    # ---- PDF FOOTER COPYRIGHT ----
    c.setFont("Helvetica-Oblique", 9)
    c.drawCentredString(300, 40, COPYRIGHT_TEXT)

    c.showPage()
    c.save()
    pdf_buffer.seek(0)

    st.download_button(
        "📄 Download Ticket as PDF",
        pdf_buffer,
        file_name=f"{t['ticket_no']}.pdf",
        mime="application/pdf"
    )

# ---------------- PAGE FOOTER ----------------
st.markdown(
    f"<hr><p style='text-align:center;font-size:12px;'>{COPYRIGHT_TEXT}</p>",
    unsafe_allow_html=True

)
