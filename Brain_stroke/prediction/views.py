from django.shortcuts import render,redirect
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.hashers import make_password, check_password
import os
import numpy as np
import tensorflow as tf
from .models import User, Image, Prediction, PredictionHistory
from .forms import SignupForm
from PIL import Image as PILImage

# =========================
# LOAD MODEL
# =========================
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

# Model path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "brain_stroke_model.h5")

print("Loading model from:", MODEL_PATH)

try:
    model = load_model(MODEL_PATH)
    print("✅ Model loaded successfully")
except Exception as e:
    print("❌ Model loading failed:", e)
    model = None


# =========================
# PREDICTION FUNCTION
# =========================
def is_ct_scan(img_path):
    try:
        img = PILImage.open(img_path)

        width, height = img.size

        if width < 200 or height < 200:
            return False

        img_rgb = np.array(img)

        if len(img_rgb.shape) == 3:

            r = img_rgb[:, :, 0]
            g = img_rgb[:, :, 1]
            b = img_rgb[:, :, 2]

            color_difference = (
                np.mean(np.abs(r - g)) +
                np.mean(np.abs(r - b)) +
                np.mean(np.abs(g - b))
            )

            if color_difference > 15:
                return False

        return True

    except Exception:
        return False



def predict_image(img_path):
    if model is None:
        return "Model not loaded", 0

    try:
        img = image.load_img(img_path, target_size=(224, 224))
        img_array = image.img_to_array(img)
        img_array = img_array / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        prediction = model.predict(img_array)

        print("=" * 50)
        print("Raw Prediction:", prediction)
        print("Prediction Shape:", prediction.shape)
        print("Score:", prediction[0][0])
        print("=" * 50)

        score = float(prediction[0][0])

        # Assuming:
        # Normal = 0
        # Stroke = 1

        if score >= 0.5:
            predicted_class = "Stroke"
        else:
            predicted_class = "Normal"

        confidence = max(score, 1 - score) * 100

        return predicted_class, confidence

    except Exception as e:
        print("Prediction Error:", str(e))
        return f"Prediction Error: {str(e)}", 0
# =========================
# HOME
# =========================
def home(request):
    return render(request, 'home.html')

# =========================
# SIGNIN
# =========================
def signin(request):

    if request.method=="POST":

        form=SignupForm(request.POST)

        if form.is_valid():

            user = form.save(commit=False)
            user.full_clean()

            user.password = make_password(user.password)

            user.save()

            return redirect('login')

    else:

        form=SignupForm()

    return render(
        request,
        'signinpage.html',
        {'form':form}
    )

# =========================
# LOGIN
# =========================
def login(request):
    if request.method == 'POST':
        Patientname = (request.POST.get('firstname','').strip() +" " +request.POST.get('lastname','').strip())
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = User.objects.filter(email=email).first()

        if user and check_password(password, user.password):
            request.session['user_id'] = user.id
            request.session['username'] = user.firstname
            return redirect('main')

        return render(request, 'loginpage.html', {"error": "Invalid credentials"})

    return render(request, 'loginpage.html')

# =========================
# MAIN (UPLOAD + PREDICTION)
# =========================
def main(request):
    if 'user_id' not in request.session:
        return redirect('login')

    context = {}

    user = User.objects.get(id=request.session['user_id'])

    if request.method == "POST" and request.FILES.get("disease_image"):

        image_file = request.FILES["disease_image"]

        storage = FileSystemStorage()
        filename = storage.save(image_file.name, image_file)

        file_path = storage.path(filename)
        image_url = storage.url(filename)

        image_obj = Image.objects.create(
            user=user,
            image_file=image_file
        )

        if not is_ct_scan(file_path):

            context = {
                "image_url": image_url,
                "prediction": "❌ Please upload a Brain CT Scan image only",
                "confidence": 0,
                "filename": filename
            }

            return render(request, "main.html", context)

        prediction_result, confidence = predict_image(file_path)

        prediction_obj = Prediction.objects.create(
            user=user,
            image=image_obj,
            disease_name=prediction_result,
            confidence_score=confidence
        )

        PredictionHistory.objects.create(
            user=user,
            prediction=prediction_obj
        )

        context = {
            "image_url": image_url,
            "prediction": prediction_result,
            "confidence": round(confidence, 2),
            "filename": filename
        }

    return render(request, "main.html", context)

# =========================
# HISTORY PAGE
# =========================
def history(request):
    if 'user_id' not in request.session:
        return redirect('login')

    user = User.objects.get(id=request.session['user_id'])

    history = PredictionHistory.objects.filter(user=user)

    return render(request, "history.html", {"history": history})

# =========================
# LOGOUT
# =========================
def logout(request):
    request.session.flush()
    return redirect('login')



