from django.shortcuts import render, HttpResponse
import random
import yagmail

def generador_numero():
    codigo_user = random.randint(1000, 9999)
    return codigo_user

def envio_correo(numero_clave,correo):
    # Datos de autenticación
    email_usuario = 'eusacrafter@gmail.com'  # Tu dirección de correo
    password = 'hdhjjorqyyqkaoyk'  # Tu contraseña

    # Configuración del mensaje
    destinatario = correo  # Correo del destinatario
    asunto = 'Codigo de Restablecimiento'
    cuerpo = f'Este es el código para restablecer su contraseña. Si no solicitó el cambio de contraseña, puede ignorar este correo.\n\n codigo : {numero_clave}'

    #Iniciar sesión con yagmail
    yag = yagmail.SMTP(email_usuario, password)

    # Enviar el correo
    yag.send(to=destinatario, subject=asunto, contents=cuerpo)

    # Cerrar la sesión de yagmail
    yag.close()

def envio_code_auth(numero_clave,bussines_name,email):
    # Datos de autenticación
    email_usuario = 'eusacrafter@gmail.com'  # Tu dirección de correo
    password = 'hdhjjorqyyqkaoyk'  # Tu contraseña

    # Configuración del mensaje
    destinatario = 'eusacrafter@gmail.com'  # Correo del destinatario
    asunto = 'Codigo de Autorizacion'
    cuerpo = f'La empresa : {bussines_name} quiere el acceso con el correo : {email} \n su codigo de registro es codigo activacion : {numero_clave}'

    #Iniciar sesión con yagmail
    yag = yagmail.SMTP(email_usuario, password)

    # Enviar el correo
    yag.send(to=destinatario, subject=asunto, contents=cuerpo)

    # Cerrar la sesión de yagmail
    yag.close()
    

def envio_correo_estatus_pedido(correo,estatus_pedido,numero_pedido,detalle_correo,fecha,producto):
    # Datos de autenticación
    email_usuario = 'eusacrafter@gmail.com'  # Tu dirección de correo
    password = 'hdhjjorqyyqkaoyk'  # Tu contraseña

    # Configuración del mensaje
    destinatario = correo  # Correo del destinatario
    asunto = f'Pedido {estatus_pedido}'
    cuerpo = f"""Estimado/a \n
    Nos complace informarle que su pedido con el número {numero_pedido} se encuentra en progreso. 
    Nuestro equipo está trabajando para procesarlo y garantizar que reciba sus productos en el menor tiempo posible. \n
    Le notificaremos tan pronto como su pedido esté listo para ser enviado. \n
    Si tiene alguna pregunta o necesita realizar alguna modificación en su pedido, no dude en contactarnos a través de nuestro servicio de atención al cliente en 5555555555. \n
    Agradecemos su preferencia y confianza en Grupo Omega. Estamos a su disposición para cualquier consulta."""
    if estatus_pedido == "cancelado":
        cuerpo = f"""Estimado/a \n
        Esperamos que este mensaje lo/la encuentre bien. Nos comunicamos para confirmar 
        la cancelación de su pedido con el número {numero_pedido}, realizada el día {fecha}. \n
        Razón de la Cancelación : {detalle_correo} \n
        Lamentamos los inconvenientes que esto pueda haber causado y agradecemos que nos haya informado. Si corresponde, 
        el reembolso se procesará a través del mismo método de pago utilizado en un plazo de  2 días hábiles. Recibirá una notificación cuando el reembolso se haya completado.
        Si tiene alguna duda o necesita asistencia adicional, no dude en responder a este correo o contactarnos a través de nuestro servicio de atención al cliente en 5555555555.
        Agradecemos su comprensión y quedamos a su disposición para cualquier consulta."""
    elif estatus_pedido == "entregado":
        cuerpo = f"""Estimado/a \n
        Nos complace informarle que su pedido con el número {numero_pedido} ha sido entregado con éxito el día {fecha} \n.
        Esperamos que los productos hayan cumplido con sus expectativas. A continuación, encontrará un resumen de su pedido:\n
        Detalles del Pedido:\n
        * Producto: {producto} \n
        * Fecha de Entrega: {fecha} \n
        Detalle de Entrega:\n
        {detalle_correo}\n
        En caso de que necesite asistencia, realizar una devolución o tenga comentarios sobre su experiencia, no dude en contactarnos a través de 5555555555. 
        Nos encantaría saber cómo fue su experiencia y estamos aquí para ayudarle en lo que necesite. \n
        Gracias por confiar en Grupo Omega. Esperamos servirle nuevamente en el futuro."""
    #Iniciar sesión con yagmail
    yag = yagmail.SMTP(email_usuario, password)

    # Enviar el correo
    yag.send(to=destinatario, subject=asunto, contents=cuerpo)

    # Cerrar la sesión de yagmail
    yag.close()