from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from .models import Shipment
from .notifications import send_shipment_status_email


@receiver(pre_save, sender=Shipment)
def capture_previous_status(sender, instance, **kwargs):
    print(" Guarda el status anterior en el objeto antes de guardar")
    """Guarda el status anterior en el objeto antes de guardar."""
    
    if instance.pk:
        try:
            instance._previous_status = Shipment.objects.get(pk=instance.pk).status
        except Shipment.DoesNotExist:
            instance._previous_status = None
    else:
        instance._previous_status = None


@receiver(post_save, sender=Shipment)
def notify_on_status_change(sender, instance, created, **kwargs):
    print(" Envía email al usuario cuando el status cambia")
    """
    Envía email al usuario cuando el status cambia
    a 'shipped' o 'delivered'.
    """
    previous = getattr(instance, '_previous_status', None)
    print("previous:", previous)

    # No notificar en la creación (status inicial = pending)
    if created:
        return

    # Solo notificar si el status realmente cambió
    if previous == instance.status:
        return

    send_shipment_status_email(instance)
