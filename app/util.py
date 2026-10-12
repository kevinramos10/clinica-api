from math import ceil

from smtplib import SMTP
from email.message import EmailMessage
from os import getenv
import requests

def paginationInfo(total, pagina, porPagina):

    itemsPorPagina = porPagina if total >= porPagina else total

    totalPaginas = ceil(total / itemsPorPagina) if itemsPorPagina > 0 else 0

    paginaPrevia = pagina - 1 if pagina > 1 and pagina <= totalPaginas else None

    paginaSiguiente = pagina + 1 if totalPaginas > 1 and pagina < totalPaginas else None

    return{
        'porPagina': itemsPorPagina,
        'total': total,
        'pagina': pagina,
        'paginaPrevia': paginaPrevia,
        'paginaSiguiente': paginaSiguiente,
        'totalPaginas': totalPaginas
    }

# def enviar_correo(destinatarios, asunto, cuerpo):
#     mensaje = EmailMessage()

#     #Correo del emisor
#     mensaje["From"] = getenv("EMAIL")

#     #Correo Destino
#     mensaje["To"] = destinatarios

#     #Asunto del cuerpo
#     mensaje["Subject"] = asunto

#     #Contenido del mensaje
#     mensaje.set_content("Abre este correo en un cliente compatible con HTML.")
#     mensaje.add_alternative(cuerpo, subtype="html")

#     #Conexion con el servidor de correo
#     servidor = SMTP(
#         host=getenv("SMTP_HOST"),
#         port=int(getenv("SMTP_PUERTO"))
#     )

#     servidor.starttls()

#     #Autenticacion
#     servidor.login(
#         user=getenv("EMAIL"),
#         password=getenv("EMAIL_PASSWORD")
#     )

#     #Enviar correo
#     servidor.send_message(mensaje)

#     #Cerrar sesion
#     servidor.quit()

def enviar_correo(destinatario, asunto, cuerpo):
    respuesta = requests.post(
        "https://api.resend.com/emails",
        headers={
            "Authorization": f"Bearer {getenv('RESEND_API_KEY')}",
            "Content-Type": "application/json"            
        },
        json={
            "from": getenv("EMAIL"),
            "to": [destinatario],
            "subject": asunto,
            "html": cuerpo
        },
        timeout=20
    )

    respuesta.raise_for_status()






