import requests
import json
from datetime import datetime, timedelta
import Notice as notice
from decouple import config

#Variables
url = 'https://api.cuentica.com'
token = config('TOKEN')
payload={}
notice_days = 15
account = 47393

class MainWeb:
    def __init__(self) -> None:
        data = self.get_customer()
        customers = json.loads(data)
        for customer in customers:
           if customer['personal_comment']: self.test_invoice(customer)
    
    #Acciones
    def test_invoice(self, customer):
        dato = customer['personal_comment'].split(';')
        if len(customer) > 2:
            currentDay = datetime.now().day
            currentMonth = datetime.now().month
            currentYear = datetime.now().year

            now = str(currentDay) + '-' + str(currentMonth)
            fecha_tmp = datetime.strptime(dato[1]+'-'+str(currentYear), '%d-%m-%Y')
            aviso_tmp = fecha_tmp - timedelta(days=notice_days)
            aviso = str(aviso_tmp.day)+'-'+str(aviso_tmp.month)

            if now == aviso:
                self.send_notice(customer['email'], dato[0], customer['contact_person'], dato[2], customer['tradename'])

            if now == dato[1]:
                fecha = str(currentYear)+'-'+str(currentMonth)+'-'+str(currentDay)
                factura = False
                if 3 < len(dato): factura = dato[3]
                self.send_invoice(customer['id'], fecha, customer['email'], dato[0], dato[2], factura, customer['contact_person'], customer['tradename'])

    def send_invoice(self, id, fecha, correo, tipo, precio, factura, name, empresa):
        false = False
        true = True
        facturacion = False
        if factura == 'factura': facturacion = True
        lastinvoice = self.get_last_invoice(id, fecha)
        sin_iva = float(precio)
        tax = float('21.0')
        total = (sin_iva * tax / 100) + sin_iva
        bodyData = {
            'description':'Factura WEB',
            'annotations':'Factura enviada automáticamente',
            'date': fecha,
            'issued': facturacion,
            'customer':id,
            'invoice_lines':[
                {'quantity':1,'concept':'Renovación anual de ' + tipo,'amount':sin_iva,'discount':0,'tax':tax,'surcharge':0,'retention':0}],
            'charges':[{'date':fecha,'amount':total,'method':'cash','destination_account':account,'origin_account':'CUENTA','charged':false}]
        }

        bodyCorreo = {
            'body': 'Hola '+name+'.\n\nAquí te hacemos llegar la factura de renovación anual de '+tipo+' para '+empresa+'.\n\nMuchas gracias por seguir confiando en nosotros y saludos.\n\ncariz.studio',
            'subject': 'Factura de servicios',
            'reply_to': 'somos@cariz.studio',
            'to':[correo, 'somos@cariz.studio'],
            'include_pdf': true,
            'show_card_payment': false
        }

        if len(lastinvoice) == 2:
            print('FACTURA Y CORREO')
            invoice = self.post_invoice(bodyData)
            datos_invoice = json.loads(invoice)
            if facturacion: mail = self.post_email(datos_invoice['id'], bodyCorreo)
            print(mail)
        else:
            print('NADA')

    def send_notice(self, correo, tipo, nombre, precio, empresa):
        notice.Send.mail_15(self, correo, tipo, nombre, precio, empresa)
 

    #API
    def get_customer(self):
        payload={}
        headers = {'X-AUTH-TOKEN': token}
        response = requests.request("GET", url+'/customer', headers=headers, data=payload)
        return response.text

    def get_last_invoice(self, id, fecha):
        headers = {'X-AUTH-TOKEN': token}
        response = requests.request("GET", url+'/invoice?customer='+str(id)+'&initial_date='+fecha, headers=headers, data=payload)
        return response.text

    def post_invoice(self, bodyData):
        payload = json.dumps(bodyData)
        headers = {'X-AUTH-TOKEN': token, 'Content-Type': 'application/json'}
        response = requests.request("POST", url+'/invoice', headers=headers, data=payload)
        return response.text

    def post_email(self, id, bodyData):
        payload = json.dumps(bodyData)
        headers = {'X-AUTH-TOKEN': token, 'Content-Type': 'application/json'}
        response = requests.request("POST", url+'/invoice/'+str(id)+'/email', headers=headers, data=payload)
        return response


if __name__ == '__main__':
    MainWeb()