import sendgrid
import os
from sendgrid.helpers.mail import *
from utils import invert_date, get_gmt_date, split_into_sections, split_str

def send_mail(images):
    todays_date = invert_date(get_gmt_date(int(os.getenv('GMT', '5'))), join_delimiter='-')

    html_body = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <style>
        h1,
        h2 {{
            text-align: center;
        }}
        img {{
            max-width: 100%;
            height: auto;
            display: block;
            margin: 0 auto;
        }}
        </style>
    </head>
    <body>
        <h1>DAWN Newspaper {todays_date}</h1>
        """

    for section, images in split_into_sections(images).items():
        html_body += f"""
            <hr />
            <h2>{section}</h2>
        """
        for image in images:
            html_body += f"""
                <hr />
                <img src="{image['url']}" />
            """

    html_body += """
    </body>
    </html>
    """

    sg = sendgrid.SendGridAPIClient(api_key=os.getenv('MAIL_API_KEY'))
    from_email = Email(os.getenv("MAIL_SENDER"))
    for mail_recipient in split_str(os.getenv("MAIL_RECIPIENTS")):
        print('Sending mail to', mail_recipient)
        to_email = To(mail_recipient)
        subject = f"{images[0]['newspaper_name']} Newspaper {todays_date}"
        mail = Mail(from_email, to_email, subject, html_content=html_body)
        response = sg.client.mail.send.post(request_body=mail.get())
        print(response.status_code)
        print(response.body)
        print(response.headers)