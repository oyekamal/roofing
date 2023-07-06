from django.apps import AppConfig


class ServiceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'service'
    def ready(self):
        import service.signals
        from paypal.standard.ipn.signals import valid_ipn_received
        from service.signals import paypal_payment_received

        valid_ipn_received.connect(paypal_payment_received)
        