import sendgrid
from decouple import config
from sendgrid.helpers.mail import *

api_key = config('SENDGRID_API_KEY')

class Send:
    def mail_15(self, to, type):
        sg = sendgrid.SendGridAPIClient(api_key)
        from_email = Email("somos@cariz.studio")
        to_email = To(to)
        subject = "Próximo cargo"
        content = Content("text/plain", "Dentro de 15 días caducan los servicios que tienes contratados con nosotros")
        mail = Mail(from_email, to_email, subject, content)
        response = sg.client.mail.send.post(request_body=mail.get())
        return(response.status_code)
        # print(response.body)
        # print(response.headers)