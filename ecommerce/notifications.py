from django.core.mail import send_mail
from django.conf import settings


SUBJECT_MAP = {
    'shipped': 'Tu pedido ha sido enviado 🚚',
    'delivered': '¡Tu pedido ha llegado! ✅',
}

BODY_MAP = {
    'shipped': (
        'Hola {name},\n\n'
        'Tu pedido de "{product}" ha sido enviado.\n\n'
        'Courier: {courier}\n'
        'N° de seguimiento: {tracking}\n'
        'Entrega estimada: {estimated}\n\n'
        '{notes}'
        'Gracias por tu compra.'
    ),
    'delivered': (
        'Hola {name},\n\n'
        '¡Tu pedido de "{product}" ha sido entregado exitosamente!\n\n'
        'Courier: {courier}\n'
        'N° de seguimiento: {tracking}\n\n'
        '{notes}'
        'Gracias por confiar en nosotros.'
    ),
}


def send_shipment_status_email(shipment):
    print(shipment)
    """
    Envía un email al usuario cuando el estado del envío cambia
    a 'shipped' o 'delivered'.
    """
    status = shipment.status
    if status not in SUBJECT_MAP:
        return

    user = shipment.user
    recipient_email = user.email
    if not recipient_email:
        return

    estimated = (
        shipment.estimated_delivery.strftime('%d/%m/%Y')
        if shipment.estimated_delivery
        else 'Por confirmar'
    )
    notes_line = f'Nota: {shipment.notes}\n\n' if shipment.notes else ''

    body = BODY_MAP[status].format(
        name=user.get_full_name() or user.username,
        product=shipment.product.name,
        courier=shipment.courier_company,
        tracking=shipment.tracking_number,
        estimated=estimated,
        notes=notes_line,
    )

    send_mail(
        subject=SUBJECT_MAP[status],
        message=body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[recipient_email],
        fail_silently=False,
    )
