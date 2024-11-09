import yagmail
def enviar_correo(producto,cantidad,ciudad,nombre,correo,telefono,empresa,mensaje):
    # Datos de autenticación
    email_usuario = 'eusacrafter@gmail.com'  # Tu dirección de correo
    password = 'hdhjjorqyyqkaoyk'  # Tu contraseña
    # Configuración del mensaje
    destinatario = 'grupodeomega@gmail.com'  # Correo del destinatario
    asunto = f'Nueva Solicitud de Cotización de {producto}'
    cuerpo = f"""Estimado equipo de ventas, \nSe ha recibido una nueva solicitud de cotización de la empresa { empresa }.
            detallan los datos proporcionados por el cliente:\n
            * Producto solicitado: {producto} \n
            * Cantidad requerida: {cantidad} \n
            * Ciudad de entrega: {ciudad} \n
            Información de contacto: \n
            * Nombre del cliente: { nombre } \n
            * Correo electrónico: { correo } \n
            * Teléfono: { telefono } \n
            Observaciones adicionales: { mensaje } \n
            Les solicitamos revisar esta solicitud y enviar la cotización correspondiente a la mayor brevedad posible.  \n
            Para cualquier información adicional o ajuste en la solicitud, pueden contactar directamente al cliente usando los datos de contacto proporcionados. \n
            Gracias por su atención y pronta respuesta. \n
            Saludos cordiales, \n
            {nombre}
            {telefono}
            {correo}"""
    #Iniciar sesión con yagmail
    yag = yagmail.SMTP(email_usuario, password)

    # Enviar el correo
    yag.send(to=destinatario, subject=asunto, contents=cuerpo)

    # Cerrar la sesión de yagmail
    yag.close() 
    
    
    
    
    
def aviso_cotizacion(producto,cantidad,ciudad,nombre,correo,telefono,empresa,mensaje):
    # Datos de autenticación
    email_usuario = 'eusacrafter@gmail.com'  # Tu dirección de correo
    password = 'hdhjjorqyyqkaoyk'  # Tu contraseña
    
    # Configuración del mensaje
    destinatario = correo  # Correo del destinatario
    asunto = f'Solicitud de Cotización para {producto}'
    cuerpo = f"""Estimado/a, \nRecibimos su solicitud de cotización. A continuación, le presentamos los detalles proporcionados:\n
            * Producto solicitado: {producto} \n
            * Cantidad requerida: {cantidad} \n
            * Ciudad de entrega: {ciudad} \n
            Información de contacto: \n
            * Nombre: { nombre } \n
            * Correo electrónico: { correo } \n
            * Teléfono: { telefono } \n
            * Empresa: { empresa } \n
            Observaciones adicionales: { mensaje } \n
            Nos pondremos en contacto con usted lo antes posible para brindarle la cotización solicitada. 
            Si necesita información adicional o desea modificar algún dato, no dude en responder a este correo. \n
            Gracias por su interés en nuestros productos. \n
            Saludos cordiales, \n
            Grupo Omega
            5556566789
            grupodeomega@gmail.com""" 
            
    #Iniciar sesión con yagmail
    yag = yagmail.SMTP(email_usuario, password)

    # Enviar el correo
    yag.send(to=destinatario, subject=asunto, contents=cuerpo)

    # Cerrar la sesión de yagmail
    yag.close()