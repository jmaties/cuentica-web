import requests
import json
from datetime import datetime
import os

#Variables
url = 'https://api.cuentica.com'
token = os.environ.get("token")
payload={}

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

            if now == dato[1]:
                fecha = str(currentYear)+'-'+str(currentMonth)+'-'+str(currentDay)
                factura = False
                if 3 < len(dato): factura = dato[3]
                self.send_invoice(customer['id'], fecha, customer['email'], dato[0], dato[2], factura)

    def send_invoice(self, id, fecha, correo, tipo, precio, factura):
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
            'charges':[{'date':fecha,'amount':total,'method':'cash','destination_account':47393,'origin_account':'CUENTA','charged':false}]
        }

        bodyCorreo = {
            'body': 'Aqui llevas tu factura por todo lo que hemos hecho',
            'subject': 'La factura!!!',
            'reply_to': 'somos@cariz.studio',
            'to':[correo, 'somos@cariz.studio'],
            'include_pdf': true,
            'show_card_payment': true
        }

        if len(lastinvoice) == 2:
            print('FACTURA Y CORREO')
            invoice = self.post_invoice(bodyData)
            if (facturacion): mail = self.post_email(id, bodyCorreo)
        else:
            print('NADA')
 

    #API
    def get_customer(self):
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
        return response

    def post_email(self, id, bodyData):
        payload = json.dumps(bodyData)
        headers = {'X-AUTH-TOKEN': token, 'Content-Type': 'application/json'}
        response = requests.request("POST", url+'/invoice/'+str(id)+'/email', headers=headers, data=payload)
        return response


if __name__ == '__main__':
    MainWeb()