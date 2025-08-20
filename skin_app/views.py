import os
import uuid
import numpy as np
from PIL import Image

from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from .forms import UploadImageForm
from .models import Product

import tensorflow as tf

# Try importing tensorflow keras load_model with error handling
try:
    from tensorflow.keras.models import load_model

    # ✔ Update folder name here
    MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'models', 'skin_disease_model.h5')
    model = load_model(MODEL_PATH)

except ImportError as e:
    model = None
    print("TensorFlow import error:", e)
except Exception as e:
    model = None
    print("Model loading error:", e)

# ✔ Class names
CLASS_NAMES = ['acne', 'eczema', 'pigmentation', 'rosacea']

def prepare_image(img_path):
    img = Image.open(img_path).convert("RGB")
    img = img.resize((64, 64))
    img_array = np.array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array.astype('float32') / 255.0
    return img_array

def index(request):
    prediction = None
    products = None
    img_url = None

    if request.method == 'POST':
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_img = form.cleaned_data['image']

            media_dir = 'media'
            if not os.path.exists(media_dir):
                os.makedirs(media_dir)

            fs = FileSystemStorage()
            unique_filename = f"{uuid.uuid4().hex}_{uploaded_img.name}"
            filename = fs.save(unique_filename, uploaded_img)
            img_path = fs.path(filename)
            img_url = fs.url(filename)

            if model is not None:
                try:
                    img_prepared = prepare_image(img_path)
                    preds = model.predict(img_prepared)
                    predicted_class_index = np.argmax(preds)
                    prediction = CLASS_NAMES[predicted_class_index]
                    products = Product.objects.filter(disease_name__iexact=prediction)
                except Exception as e:
                    prediction = "Error processing image"
                    products = None
                    print("Prediction Error:", e)
            else:
                prediction = "Model not loaded"
                products = None

    else:
        form = UploadImageForm()

    return render(request, 'index.html', {
        'form': form,
        'prediction': prediction,
        'products': products,
        'img_url': img_url,
    })
