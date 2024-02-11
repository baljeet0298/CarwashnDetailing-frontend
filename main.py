# The first step is always the same: import all necessary components:

import smtplib, ssl
import pdfkit
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import Flask, render_template, request, current_app

app = Flask(__name__)

# adding new comment
@app.route('/')
def home():
    return render_template('./index.html')


@app.route('/send', methods=['POST', 'GET'])
def send_mail():
    to = "carwashndetailingjbp@gmail.com"
    subject = "Customer Query"
    message = MIMEMultipart("alternative")
    message["From"] = to
    message["To"] = to
    message["Subject"] = subject
    if request.method == 'POST':
        name_from = request.form["Name"]
        email_from = request.form["Email"]
        query_from = request.form["Query"]
        text = """\
            Hi,
            Sender Name : {name_from}
            Email_Id : {email_from}
            Query : {query_from}
            """
        html = f"""\
            <html>
              <body>
                <p>Hi,<br>
                   Sender Name : <b>{name_from}</b><br>
                   Email_Id : {email_from}<br>
                   Query : <b>{query_from}</b><br> 
                </p>
              </body>
            </html>
            """
        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")
        message.attach(part1)
        message.attach(part2)
        uname = "carwashndetailingjbp@gmail.com"
        upass = "Sirat@2017"
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(uname, upass)
            server.sendmail(
                uname, uname, message.as_string()
            )
    return render_template("result.html")


@app.route('/loginpage.html')
def success():
    return render_template("loginpage.html")


@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == 'POST':
        uid = request.form["userid"]
        pswrd = request.form["pswrd"]
    if uid == "admin" and pswrd == "admin":
        return render_template('./create_invoice.html')


@app.route('/createinvoice', methods=["POST", "GET"])
def create_invoice():
    if request.method == 'POST':
        data = {"GST Number": "ABCDE12334",
                "Name": request.form["firstname"],
                "Vehicle Type": request.form["vehicletype"],
                "Email id": request.form["email"],
                "Mobile No": request.form["phone"],
                "City": request.form["city"],
                "Car Model": request.form["carmodel"],
                "Registration Number": request.form["registrationnumber"],
                "Date": request.form["date"],
                "Delivery Date": request.form["deliverydate"],
                "Mudflap": request.form["mudflap"],
                "Mats": request.form["mats"],
                "Service Taken": request.form.getlist("servicetaken"),
                "Accessories": request.form["accessories"],
                "Total": 0}
        price = {"Shampoo": 100, "Quick Wash": 500, "Detailing": 5000}
        pricelist = []
        total=0
        for i in request.form.getlist("servicetaken"):
            an_item = dict(name=i, price=price[i])
            pricelist.append(an_item)
            total=total+price[i]
        data["Service Taken"] = pricelist
        data["Total"] = total
        o = {
            "enable-local-file-access": ""
        }
        x = render_template("index2.html", data=data)
        print(x)
        pdfkit.from_string(x, request.form["registrationnumber"] + ".pdf", options=o)

        # -------------------------main------------------------------------------------
        subject = "Car Wash N Detailing : Invoice"
        body = "<h3>Thanks for your visit.</h3>" \
               "---------------------------" \
               "---------------------------" \
               "<h3>PFA.</h3>" \
               "<h3>Car Wash N Detailing</h3>" \
               "<h3>Jabalpur,M.P</h3>" \
               "<h3>For any Query: Revert back to carwashndetailingjbp@gmail.com</h3>"
        sender_email = "carwashndetailingjbp@gmail.com"
        receiver_email = request.form["email"]
        password = "Sirat@2017"

        # Create a multipart message and set headers
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = subject
        message["Bcc"] = receiver_email  # Recommended for mass emails

        # Add body to email
        message.attach(MIMEText(body, "html"))

        filename = request.form["registrationnumber"] + ".pdf"  # In same directory as script

        # Open PDF file in binary mode
        with open(filename, "rb") as attachment:
            # Add file as application/octet-stream
            # Email client can usually download this automatically as attachment
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())

        # Encode file in ASCII characters to send by email
        encoders.encode_base64(part)

        # Add header as key/value pair to attachment part
        part.add_header(
            "Content-Disposition",
            f"attachment; filename= {filename}",
        )

        # Add attachment to message and convert message to string
        message.attach(part)
        text = message.as_string()

        # Log in to server using secure context and send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, text)
    return render_template("./result.html")


if __name__ == '__main__':
    app.run(debug=True)
