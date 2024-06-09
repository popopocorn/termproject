# -*- coding: cp949 -*-
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
import os


def send_email(send_to, title, main_text):
    host = "smtp.gmail.com"  # Gmail STMP 서버 주소.
    port = 587

    from_addr = "ahw8670@tukorea.ac.kr"
    to_addr = str(send_to)
    subject = '제목: ' + str(title)
    body = """
    <html>
      <body>
        <p>"""+str(main_text)+"""</p>
        <img src="cid:image1">
      </body>
    </html>
    """

    msg = MIMEMultipart()
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'html'))

    filename = 'graph.png'
    filepath = os.path.join('', filename)

    msg.attach(MIMEText('test', 'plain'))

    with open(filepath, 'rb') as img:
        mime_image = MIMEImage(img.read())
        mime_image.add_header('Content-ID', '<image1>')
        mime_image.add_header('Content-Disposition', 'inline', filename=filename)
        msg.attach(mime_image)

    val = bool()

    try:
        server = smtplib.SMTP(host, port)
        server.starttls()
        server.login("ahw8670@tukorea.ac.kr", "rxye pkmp sjpp iqsn")
        server.sendmail(from_addr, to_addr, msg.as_string())
        val = True
    except Exception as e:
        print(f'이메일 전송 중 오류 발생: {e}')
        val = False
    finally:
        server.quit()
        return val
