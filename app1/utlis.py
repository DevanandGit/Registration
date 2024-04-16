from rest_framework.response import Response
from django.core.mail import EmailMessage
from .models import Events, Delegates, DelegateEvent
import qrcode
from io import BytesIO

def is_delegate_associated_with_event(delegate, event):
    try:
        DelegateEvent.objects.get(delegate=delegate, event=event)
        return True
    except DelegateEvent.DoesNotExist:
        return False

def send_email(data):
        email = EmailMessage(subject=data['email_subject'], body=data['email_body'], to = [data['to_email']])
        email.content_subtype = 'html'
        email.send()
        return Response('Email sent successfully!')

def generate_qr_code(qr_data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_data)
    qr.make(fit=True)

    # Create an image from the QR code
    img = qr.make_image(fill_color="black", back_color="white")
    return img

def checkevent(ktu_id, event_id):
    event = Events.objects.get(id = event_id)
    delegate = Delegates.objects.get(ktu_id = ktu_id)
    print(delegate)
    delegate_events = DelegateEvent.objects.filter(delegate = delegate)
    for events in delegate_events:
        if events.event.event_name == event.event_name:
            return True
    else:
         return False

    
    
     