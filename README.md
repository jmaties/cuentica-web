# cuentica-web

Aplicación web para enviar facturas y correo electrónico a cliente con [Cuéntica](https://cuentica.com) a través de su [API](https://apidocs.cuentica.com/) de forma recurrente mediante una tarea cron.

Usa el campo "personal_comment" de customer para indicar: 
tipo de producto;precio (sin iva);fecha de la recurrencia (dia-mes);factura o presupuesto

Ejemplo:
hosting+domino;12-1;70;factura

Este ejemplo envia un correo y la factura con el producto hosting+dominio todos los 12 de enero y con un importe de 70€ + IVA
Además, envia un correo 15 días antes avisando al cliente de la próxima renovación de su servicio

Lo usamos para el envio de las facturas de servicios anuales tales como hosting, dominio, correo...
Campo issued para generación de factura(true) o presupuesto(false)

Dependencias: requests, sendgrid, python-decouple

En el archivo .env indicar el token de la api de Cuéntica
