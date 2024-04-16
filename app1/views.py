from rest_framework import viewsets
from .models import Events, Delegates, DelegateEvent
from .serializers import EventsSerializer, DelegatesSerializer
from rest_framework.generics import (CreateAPIView, ListCreateAPIView, 
                            RetrieveUpdateDestroyAPIView, GenericAPIView, 
                            RetrieveAPIView, ListAPIView)
from rest_framework.views import APIView
from django.http import Http404
from rest_framework.response import Response
from rest_framework import status
import ast
from rest_framework.filters import SearchFilter
from django.db.models import Q
from .utlis import is_delegate_associated_with_event
import qrcode
import json
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .utlis import send_email, checkevent
from django.core.mail import EmailMultiAlternatives


class EventsViewSet(viewsets.ModelViewSet):
    queryset = Events.objects.all()
    serializer_class = EventsSerializer

    
class RegisterCustomEvents(APIView):
    serializer_class = DelegatesSerializer

    def post(self, request):
        serializer = DelegatesSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()

        instance.total_amount = 0.00
        instance.save()
        variable_fee = 0

        events_id_str = request.data.get('events_id', [])
        events_id_list = ast.literal_eval(events_id_str)

        for events_id in events_id_list:
            try:
                event = Events.objects.get(id=events_id)
                variable_fee += event.fees
                instance.total_amount = variable_fee
                instance.save()
            except Events.DoesNotExist:
                raise Http404("Event does not exist")
            
            registered_event = DelegateEvent.objects.create(delegate=instance, event=event, is_active=True)
            
        user_details = {
            'name': instance.name,
            'semester': instance.semester,
            'ktu_id': instance.ktu_id,
            'events_registered': [event.event.event_name for event in DelegateEvent.objects.filter(delegate=instance)],
            # Add more details as needed
        }
        qr_data = {'ktu_id': instance.ktu_id}
        user_details_str = json.dumps(user_details)
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )

        qr.add_data(qr_data['ktu_id'])
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        # Save the QR code image temporarily
        qr_image_path = f"media/qr_codes/{instance.ktu_id}.png"
        img.save(qr_image_path)
        html_content = render_to_string('post_reg_form.html', {'user_details':user_details, 'qr_image_path':qr_image_path})

        # Create EmailMultiAlternatives object
        subject = 'Your Registration Details'
        text_content = strip_tags(html_content)
        email = EmailMultiAlternatives(subject, text_content, to=[instance.gmail])
        email.attach_alternative(html_content, "text/html")

        # Attach QR code image
        with open(qr_image_path, 'rb') as f:
            email.attach('user_qr_code.png', f.read(), 'image/png')
        email.send()

        response = {'success':True, 'message': 'Registered successfully'}
        return Response(response, status=status.HTTP_200_OK)


class EditRegisterEvents(APIView):
    def post(self, request):
        search_query = self.request.query_params.get('ktu_id')
        events_id_str = request.data.get('events_id', [])
        events_id_list = ast.literal_eval(events_id_str)
        try:
            delegate = Delegates.objects.get(ktu_id = search_query)
        except Delegates.DoesNotExist:
            raise Http404("Delegate Data Notfound. Please Register!")
        for events_id in events_id_list:
            try:
                event = Events.objects.get(id = events_id)
                is_associated = is_delegate_associated_with_event(delegate=delegate, event=event)
                if is_associated:
                    continue
                else:
                    delegate.total_amount += event.fees
                    delegate.save()
                    registered_event = DelegateEvent.objects.create(delegate = delegate, event = event, is_active = True)
            except Events.DoesNotExist:
                raise Http404("Event does not exist")
        response = {'success':True, 'message': 'Events Added successfully'}
        return Response(response, status=status.HTTP_200_OK)
        

#Delegate list
class ListDelegatesAPIView(ListAPIView):
    queryset = Delegates.objects.all()
    serializer_class = DelegatesSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name', 'ktu_id', 'gmail']
    #need to add search functionality.
    def get_queryset(self):
        queryset = super().get_queryset()

        # Apply search filtering
        search_query = self.request.query_params.get('search')
        if search_query:
            # Split the search query into individual words and create a Q object for each word
            search_words = search_query.split()
            search_filter = Q()
            for word in search_words:
                search_filter |= (
                    Q(name__icontains=word) |
                    Q(ktu_id__icontains=word)|
                    Q(gmail__icontains=word)
                )
            queryset = queryset.filter(search_filter)
        return queryset


#individual Delegate
class RetrieveUpdateDestroyDelegateAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Delegates.objects.all()
    serializer_class = DelegatesSerializer
    lookup_field = 'id'


class CheckForEvents(APIView):
    def post(self, request):
        ktu_id = self.request.query_params.get('ktu_id')
        event_id = self.request.query_params.get('event_id')

        is_registered = checkevent(ktu_id=ktu_id, event_id=event_id)

        if is_registered == True:
            try:
                event = Events.objects.get(id = event_id)
            except Events.DoesNotExist:
                raise Http404("Delegate Data Notfound. Please Register!")
            try:
                delegate = Delegates.objects.get(ktu_id = ktu_id)
                delegate_event = DelegateEvent.objects.get(event = event)
                delegate_event.is_active = False
                delegate_event.save()
            except Delegates.DoesNotExist:
                raise Http404("Delegate Data Notfound. Please Register!")
            
            response = {'success':True, 'message': 'Delegate verified succesfully'}
            return Response(response, status=status.HTTP_200_OK)
        else:
            response = {'success':False, 'message': 'Delegate verification unsuccessfull'}
            return Response(response, status=status.HTTP_404_NOT_FOUND)

            

                



