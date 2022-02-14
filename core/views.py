import json
from django.db import reset_queries
from django.shortcuts import redirect, render, resolve_url
from .serializers import DeviceSerializer
from django.contrib import messages
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import TOTP, Device, Authenticate
from django.conf import settings

# for the qr code
from django.core.files import File
import urllib
from django.core.files.base import ContentFile
import os
import io
import base64
import qrcode
from PIL import Image
import cv2
import pyotp
import numpy as np

# Create your views here.

################################ this is the device api  ##############################


@api_view(["GET", "POST"])
def device(request):
    device = Device.objects.all()
    serializers = DeviceSerializer(device, many=True)

    return Response(serializers.data, status=200)

################################## authenticaton api ############################


@api_view(["POST"])
def authenticate(request):
    if request.method == 'POST':
        image = request.FILES
        d1 = json.dumps(image)
        # print(json.loads(image))
        # image = cv2.imread(image)
        print(d1)
        return Response({'status': 'working'})

    return Response({'status': 'something'})


import datetime
################################## home view and logic ##############################
def home(request, locationID):

    device = Device.objects.get(location_ID=locationID)

    totp = pyotp.TOTP(device.seed)


    if device.otp != totp.now():
        device.seed = pyotp.random_base32()
        totp = pyotp.TOTP(device.seed)
        device.otp = totp.now()
        device.save()

        # save the seed and otp for 24 hours period
        TOTP.objects.create(totp=device.otp,seed=device.seed)



    q = qrcode.make(device.seed)

    image = io.BytesIO()
    q.save(stream=image)
    base64_image = base64.b64encode(image.getvalue()).decode()

    main_code = 'data:image/png;utf8;base64,' + base64_image

    context = {
        'qr_name': main_code,
        'otp': totp.now()
    }
    return render(request, 'device.html', context)



# import RPi.GPIO as GPIO
# from time import sleep


######################## authentication logic ####################################
def auth(request):
    if request.method == 'POST':

        device = None
        try:
            image = request.FILES.get('image')
            pic = cv2.imdecode(np.fromstring(image.read(), np.uint8), cv2.IMREAD_UNCHANGED)
            detector = cv2.QRCodeDetector()
            data, vertices_array, binary_qrcode = detector.detectAndDecode(pic)
            if vertices_array is not None:
                device = Device.objects.get(seed=data)
        except:
            pass
        try:
            code = request.POST.get("totp")
            device = Device.objects.get(otp=code)
        except:
            pass


        if device is not None:
            auth, created = Authenticate.objects.get_or_create(totp=device.otp)
            auth.save()
            ########## SOLENOI.PY HERE #######################




            ################ SOLENOI.PY HERE ###################

            messages.success(request, f'Authentication Successfully done | code - {device.otp}')

            device.otp = None
            device.save()
            return render(request, 'auth.html')

        if not device:
            messages.error(request, 'Authentication does not accepted')
            return render(request, 'auth.html')

    return render(request, 'auth.html')
