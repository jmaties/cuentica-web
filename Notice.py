import sendgrid
from decouple import config
from sendgrid.helpers.mail import *

api_key = config('SENDGRID_API_KEY')

class Send:
    def mail_15(self, to, type, nombre, precio):
        sg = sendgrid.SendGridAPIClient(api_key)
        from_email = Email("somos@cariz.studio")
        to_email = To(to)
        subject = "Renovación de servicios"
        content = Content("text/html", "<p>Hola "+nombre+"</p><p>Te escribimos porque dentro de quince días caducará el servicio anual de "+type+" que tienes contratado con nosotros con coste total de "+precio+"€+IVA</p><p>Cuando llegue el día, recibirás una factura con el número de cuenta para su abono.<br/>Si decides no seguir con nosotros, por favor contáctanos a la mayor brevedad para que podamos facilitarte la migración de los servicios.<br/><br/>Saludos.</p><p>cariz.studio</p>")
        mail = Mail(from_email, to_email, subject, content)
        response = sg.client.mail.send.post(request_body=mail.get())
        return(response.status_code)
        # print(response.body)
        # print(response.headers)