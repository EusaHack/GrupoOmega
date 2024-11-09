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