# # elegate Registration API
# class RegisterCustomEvents(APIView):
#     serializer_class = DelegatesSerializer
#     def post(self, request):
#         serializer = DelegatesSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         instance = serializer.save()
#         instance.total_amount = 0.00
#         instance.save()
#         variable_fee = 0
#         events_id_str = request.data.get('events_id', [])
#         events_id_list = ast.literal_eval(events_id_str)
#         for events_id in events_id_list:
#             try:
#                 event = Events.objects.get(id = events_id)
#                 variable_fee += event.fees
#                 instance.total_amount = variable_fee
#                 instance.save()
#             except Events.DoesNotExist:
#                 raise Http404("Event does not exist")
            
#             registered_event = DelegateEvent.objects.create(delegate = instance, event = event, is_active = True)
#         encryption_key = Fernet.generate_key()
#         cipher_suite = Fernet(encryption_key)
#         user_details = {
#             'name': instance.name,
#             'semester': instance.semester,
#             'KTU_id': instance.ktu_id,
#             'events_registered': [event.event.event_name for event in DelegateEvent.objects.filter(delegate=instance)],
#             # Add more details as needed
#         }
#         user_details_str = json.dumps(user_details)
#         encrypted_user_details = cipher_suite.encrypt(user_details_str.encode())
#         qr = qrcode.QRCode(
#             version=1,
#             error_correction=qrcode.constants.ERROR_CORRECT_L,
#             box_size=10,
#             border=4,
#         )

#         qr.add_data(base64.urlsafe_b64encode(encrypted_user_details))
#         qr.make(fit=True)
#         img = qr.make_image(fill_color="black", back_color="white")

#         # Save the QR code image temporarily
#         qr_image_path = "static/qr_codes/user_qr_code.png"
#         img.save(qr_image_path)
#         html_content = render_to_string('post_reg_form.html', {'user_details':user_details, 'qr_image_path':qr_image_path})

#         # Create EmailMultiAlternatives object
#         subject = 'Your Registration Details'
#         text_content = strip_tags(html_content)
#         email = EmailMultiAlternatives(subject, text_content, to=[instance.gmail])

#         # Attach HTML content
#         email.attach_alternative(html_content, "text/html")

#         # Attach QR code image
#         with open(qr_image_path, 'rb') as f:
#             print(qr_image_path)
#             email.attach('user_qr_code.png', f.read(), 'image/png')

#         # Send email
#         email.send()

#         # Clean up temporary QR code image
#         os.remove(qr_image_path)
        
#         response = {'success':True, 'message': 'Registered successfully'}
#         return Response(response, status=status.HTTP_200_OK)