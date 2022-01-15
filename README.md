# cuentica-web

Aplicación web para enviar facturas y correo electrónico a cliente con [Cuéntica](https://cuentica.com) a través de su [API](https://apidocs.cuentica.com/) de forma recurrente a traves de una tarea cron.

Usa el campo "personal_comment" de customer para indicar el tipo de producto, el precio y la fecha de la recurrencia (dia-mes)

Ejemplo:
hosting+domino;12-1;70

Este ejemplo envia un correo y la factura con el producto hosting+dominio todos los 12 de enero y con un importe de 70€ + IVA

Lo usamos para el envio de las facturas de servicios anuales tales como hosting, dominio, correo...

La única dependencia es requests

En el archivo .env indicar el token de la api de Cuéntica