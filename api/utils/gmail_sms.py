import smtplib
import random
from email.message import EmailMessage
def send_verification_email(to_email, verification_code):
    """Emailga tasdiqlash kodini yuboruvchi funksiya."""
    # Soxta misollar uchun, bu yerga haqiqiy ma'lumotlarni kiriting
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    from_email = 'muhiddinturonov1416@gmail.com'
    from_password = 'Azi14turon@'  # 2 bosqichli tekshiruv bo'lsa, "App Password" ishlating

    subject = 'Tasdiqlash kodi'
    body = f"Sizning tasdiqlash kodingiz: {verification_code}"

    # Email xabarini tayyorlash
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email
    msg.set_content(body)

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(from_email, from_password)
            server.send_message(msg)
        print("Email muvaffaqiyatli yuborildi.")
    except Exception as e:
        print("Email yuborishda xatolik:", e)