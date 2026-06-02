from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from datetime import date
import re 
import os

# ---------------------- 
#   USER 
# ---------------------- 

# FIRST NAME VALIDATION
def firstname_validator(value):
    if " " in value:
        raise ValidationError("First name should not contain spaces")

    if not value.isalpha():
        raise ValidationError("First name should contain only letters")

# LAST NAME VALIDATION
def lastname_validator(value):
    if not value.isalpha():
        raise ValidationError("Last name should contain only letters")

# EMAIL VALIDATION
def email_validator(value):
    try:
        validate_email(value)
    except:
        raise ValidationError("Enter valid email address")

# # PASSWORD VALIDATOR 
def validate_password(value):    
  if len(value) < 6: 
        raise ValidationError("Password must be at least 6 characters")     
  if not re.search(r'[A-Z]', value): 
        raise ValidationError("Password must contain uppercase letter")  
  if not re.search(r'[0-9]', value): 
        raise ValidationError("Password must contain number") 
     
# PHONE VALIDATOR 
def phone_validator(value):     
  if len(value) != 10: 
        raise ValidationError("Phone number must be 10 digits") 
  if not value.isdigit(): 
         raise ValidationError("Phone number must contain only numbers") 

  
# DATE OF BIRTH VALIDATION
def dob_validator(value):
    today = date.today()
    if value >= today:
        raise ValidationError("DOB cannot be today or future date") 
                  
#USER MODEL 
class User(models.Model): 
    firstname = models.TextField(max_length=100,validators=[firstname_validator])   
    lastname = models.TextField(max_length=100,validators=[lastname_validator]) 
    phone = models.CharField(max_length=10,validators=[phone_validator])  
    email = models.EmailField(unique=True,validators=[email_validator])   
    password = models.CharField(max_length=100,validators=[validate_password])   
    gender = models.CharField(max_length=10)  
    dob= models.DateField(validators=[dob_validator]) 
    created_at = models.DateTimeField(auto_now_add=True) 
     
    def __str__(self): 
     return f"{self.firstname} {self.lastname}" 
 
 
# ---------------------- 
#   IMAGE 
# ---------------------- 
def validate_ct_image(value):
    valid_extensions = ['.jpg', '.jpeg', '.png']

    ext = os.path.splitext(value.name)[1].lower()

    if ext not in valid_extensions:
        raise ValidationError(
            "Only JPG, JPEG and PNG images are allowed."
        )

    if value.size > 10 * 1024 * 1024:
        raise ValidationError(
            "Image size must be less than 10 MB."
        )

#MODEL FOR IMAGE UPLOAD
class Image(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    image_file = models.ImageField(
        upload_to='Brain_Stroke_CT-SCAN_image/',
        validators=[validate_ct_image]
    )

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image {self.id}"
    

# ---------------------- 
#   PREDICTION 
# ---------------------- 
class Prediction(models.Model): 
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    image = models.ForeignKey(Image, on_delete=models.CASCADE)   
    disease_name = models.CharField(max_length=100)   
    confidence_score = models.FloatField() 
    created_at = models.DateTimeField(auto_now_add=True) 
    def __str__(self): 
        return self.disease_name 
 
 
# ---------------------- 
#   PREDICTION HISTORY 
# ---------------------- 
class PredictionHistory(models.Model): 
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    prediction = models.ForeignKey(Prediction, on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now_add=True) 
    
    def __str__(self): 
        return f"{self.user.firstname} - {self.prediction.disease_name}" 


