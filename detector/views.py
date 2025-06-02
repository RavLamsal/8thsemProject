import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

from django.shortcuts import render
from django.http import JsonResponse
import torch
import numpy as np
import cv2
from PIL import Image
from io import BytesIO
import base64
from django.shortcuts import render

model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

def index(request):
    return render(request, 'detector/index.html')

def about_view(request):
    return render(request, 'about.html')


def detect(request):
    if request.method == 'POST':
        img_data = request.POST.get('image')
        header, base64_data = img_data.split(';base64,')
        image_bytes = base64.b64decode(base64_data)

        image = Image.open(BytesIO(image_bytes)).convert('RGB')
        frame = np.array(image)

        results = model(frame)
        results.render()

        _, img_encoded = cv2.imencode('.jpg', results.ims[0])
        img_base64 = base64.b64encode(img_encoded).decode('utf-8')

        return JsonResponse({'result_image': f'data:image/jpeg;base64,{img_base64}'})
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

from django.shortcuts import render
from django.http import JsonResponse
import torch
import numpy as np
import cv2
from PIL import Image
from io import BytesIO
import base64

# Load YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
model.conf = 0.14  # Set confidence threshold to 14%    

def index(request):
    return render(request, 'detector/index.html')

def about_view(request):
    return render(request, 'about.html')

def detect(request):
    if request.method == 'POST':
        img_data = request.POST.get('image')
        
        if not img_data:
            return JsonResponse({'error': 'No image data provided'}, status=400)

        try:
            # Decode base64 image
            header, base64_data = img_data.split(';base64,')
            image_bytes = base64.b64decode(base64_data)

            # Convert to image
            image = Image.open(BytesIO(image_bytes)).convert('RGB')
            frame = np.array(image)

            # Run detection
            results = model(frame)
            results.render()  # Draw bounding boxes

            # Encode image back to base64
            _, img_encoded = cv2.imencode('.jpg', results.ims[0])
            img_base64 = base64.b64encode(img_encoded).decode('utf-8')

            return JsonResponse({'result_image': f'data:image/jpeg;base64,{img_base64}'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
