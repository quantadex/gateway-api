import hmac
import os
import hashlib
import smtplib
from email.message import EmailMessage
from jinja2 import Template
from bitshares.exceptions import (
    InvalidMessageSignature
)
import base64
import base58

from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText

import qrcode
from PIL import Image, ImageDraw
import io
import json
from binascii import hexlify, unhexlify

verifyTemplate = open('verify_email.template', 'r').read()
walletInfoTemplate = open('walletinfo_email.template', 'r').read()

smtp_options = {'host':os.environ.get("SMTP_HOST"), 'port': 587, 'ssl': False, 'user': os.environ.get("SMTP_USER"), 'password': os.environ.get("SMTP_PASS")}
email_from = "QUANTA<no-reply@quantadex.com>"

def get_code(email):
    sig = hmac.new(bytes(os.environ.get("HMAC_SECRET"),'UTF-8'), bytes(email, "UTF-8"), hashlib.sha256)
    verifyCode = int.from_bytes(sig.digest(),"little") % 100000
    print(verifyCode)
    return verifyCode

# sends a confirmation email to the user
def verify_email(email):
    verifyCode = get_code(email)

    msg = EmailMessage()
    template = Template(verifyTemplate)
    rendered = template.render(code=verifyCode)
    msg.set_content(rendered)
    msg["Subject"] = str(verifyCode) + " is your QUANTA verification code"
    msg["From"] = email_from
    msg["To"] = email
    with smtplib.SMTP(smtp_options['host'], smtp_options['port']) as s:
        s.starttls()
        s.login(smtp_options['user'],smtp_options['password'])
        s.send_message(msg)


def check_code(email,code):
    return get_code(email) == code

def make_qr(json):
    qr = qrcode.QRCode(
        version=16,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=4,
    )
    qr.add_data(json)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    logo = Image.open('logo.png')
    img = img.convert("RGBA")
    img.paste(logo, (int((img.width-logo.width)/2),int((img.height-logo.height)/2)),logo)
    #img.save("img1.png")
    return img

def send_walletinfo(email, confirm, public_key, account, json_str):
    if check_code(email, confirm):
        rawJson = base64.decodebytes(bytes(json_str,"UTF-8"))
        filename = "quanta_wallet.json"
        part = MIMEApplication(
            rawJson,
            Name=filename
        )
        part['Content-Disposition'] = 'attachment; filename="%s"' % filename

        jsonObj = json.loads(rawJson)
        base58_key = base58.b58encode(unhexlify(jsonObj["encryption_key"]) + unhexlify(jsonObj["wallet_encryption_key"]))

        qr_image = make_qr(json)
        imgBytes = io.BytesIO()
        qr_image.save(imgBytes, format='PNG')

        qrPart = MIMEApplication(
            imgBytes.getvalue(),
            Name=filename
        )
        qrPart['Content-Disposition'] = 'attachment; filename="%s"' % "quanta_wallet.png"

        msg = MIMEMultipart()

        template = Template(walletInfoTemplate)
        rendered = template.render(base58_key=base58_key, public_key=public_key, account=account)
        print(rendered)

        msg.attach(MIMEText(rendered, 'plain'))
        msg.attach(part)
        msg.attach(qrPart)

        msg["Subject"] = "Your QUANTA Wallet"
        msg["From"] = email_from
        msg["To"] = email
        with smtplib.SMTP(smtp_options['host'], smtp_options['port']) as s:
            s.starttls()
            s.login(smtp_options['user'], smtp_options['password'])
            #s.send_message(msg)
    else:
        raise InvalidMessageSignature("Confirm code is not correct")


# try {
#   val client = new OkHttpClient()
#   val body = new FormEncodingBuilder()
#     .add("name", user.first_name.getOrElse(""))
#     .add("email", user.email)
#     .add("list", config.get[String]("sendy.subscribe.list"))
#     .add("Created", user.created_at.toDate.toString)
#     .add("ReferralToken", user.referral_code.getOrElse(""))
#     .add("ActivateToken", user.token)
#     .add("Activated", user.activated.toString)
#     .build()
#
#   val request = new Request.Builder().url("http://sendy.env.quantadex.com/subscribe").post(body).build()
#   val response = client.newCall(request).execute()
#   if (response.isSuccessful) {
#     println(response.body().string())
#     false
#   } else {
#     true
#   }
# } catch {
#   case ex: Exception =>
#     Logger.error("Sendy error", ex)
#     false
# }
#
#verify_email("quocble@gmail.com")

# send_walletinfo("quocble@gmail.com",79365,"public", "account", "eyJlbmNyeXB0aW9uX2tleSI6IjAzMjIzODQ4NzJiMmZlZGVlOTJjMjU5Njk4Mjc3ZTZhYzUzYjA4NTdjMGQ1MGJjN2M1ODhiMjY1MmNiZjFlMGQ3YTZhZjQ4ODg2YTIyMTZkZTBjMmYxZGQ0ZjI3NjNmNyIsIndhbGxldF9lbmNyeXB0aW9uX2tleSI6ImUzMmM5ZTczMzAxMjQ2ZjA0MjMwMmE0MzViZGE4MjVhYWE4MTM1ZTEyYWRlMWY4YjA0Mzg3Mjg3YTgyZTE3Y2EyOWZlZjRiMmRjMDMwM2UxMDNkZTk1YWUzNTIwMmE2NiIsInBhc3N3b3JkX3B1YmtleSI6IlFBOFNVZzd0MlNaZm14a3ZRZ0JncjlKSkxRcHRRbU1pVmhiOVpYZ3l0ZXByOGQxNzFyUGsifQ==")

#make_qr("eyJlbmNyeXB0aW9uX2tleSI6IjAzMjIzODQ4NzJiMmZlZGVlOTJjMjU5Njk4Mjc3ZTZhYzUzYjA4NTdjMGQ1MGJjN2M1ODhiMjY1MmNiZjFlMGQ3YTZhZjQ4ODg2YTIyMTZkZTBjMmYxZGQ0ZjI3NjNmNyIsIndhbGxldF9lbmNyeXB0aW9uX2tleSI6ImUzMmM5ZTczMzAxMjQ2ZjA0MjMwMmE0MzViZGE4MjVhYWE4MTM1ZTEyYWRlMWY4YjA0Mzg3Mjg3YTgyZTE3Y2EyOWZlZjRiMmRjMDMwM2UxMDNkZTk1YWUzNTIwMmE2NiIsInBhc3N3b3JkX3B1YmtleSI6IlFBOFNVZzd0MlNaZm14a3ZRZ0JncjlKSkxRcHRRbU1pVmhiOVpYZ3l0ZXByOGQxNzFyUGsifQ==")