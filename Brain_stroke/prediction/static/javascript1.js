// ===============================
// SIGNUP VALIDATION
// ===============================

function validateSignup() {

    const firstname = document.querySelector('input[name="firstname"]').value.trim();
    const lastname = document.querySelector('input[name="lastname"]').value.trim();
    const phone = document.querySelector('input[name="phone"]').value.trim();
    const email = document.querySelector('input[name="email"]').value.trim();
    const password = document.querySelector('input[name="password"]').value;
    const confirmPassword = document.querySelector('input[name="confirm_password"]').value;
    const dob = document.querySelector('input[name="dob"]').value;

    // First name validation
    if (firstname.length < 3) {
        alert("First name must contain at least 3 characters");
        return false;
    }
    // First name validation
  const namePattern = /^[A-Za-z]+$/;
    if (!namePattern.test(firstname))
         {
        alert("First name should contain only alphabets without spaces");

    return false;
    }
    // Last name validation
    if (lastname.length < 1) {
        alert("Enter valid last name");
        return false;
    }
    
    const namePattern = /^[A-Za-z]+$/;
    if (!namePattern.test(lastname))
         {
        alert("Last name should contain only alphabets without spaces");
            return false;
         }
    // Phone validation
    const phonePattern = /^[0-9]{10}$/;

    if (!phonePattern.test(phone)) {
        alert("Phone number must contain exactly 10 digits");
        return false;
    }

    // Email validation
    const emailPattern = /^[^ ]+@[^ ]+\.[a-z]{2,3}$/;

    if (!emailPattern.test(email)) {
        alert("Enter valid email address");
        return false;
    }

    // Password validation
    if (password.length < 6) {
        alert("Password must contain minimum 6 characters");
        return false;
    }

    // Confirm password validation
    if (password !== confirmPassword) {
        alert("Password and Confirm Password do not match");
        return false;
    }

    // DOB validation
    if (!dob) {
        alert("Please select Date of Birth");
        return false;
    }

    const dobDate = new Date(dob);
    const today = new Date();

    if (dobDate > today) {
        alert("Date of Birth cannot be future date");
        return false;
    }

    return true;
}


// ===============================
// LOGIN VALIDATION
// ===============================

const loginForm = document.querySelector('.login-container form');

if (loginForm) {

    loginForm.addEventListener("submit", function(event){

        const email = document.querySelector('input[name="email"]').value.trim();
        const password = document.querySelector('input[name="password"]').value;

        const emailPattern = /^[^ ]+@[^ ]+\.[a-z]{2,3}$/;

        if (!emailPattern.test(email)) {
            alert("Enter valid email");
            event.preventDefault();
            return;
        }

        if (password.length < 6) {
            alert("Password must contain minimum 6 characters");
            event.preventDefault();
            return;
        }

    });

}
//image validation
function isLikelyCT(imageElement) {
    const canvas = document.createElement("canvas");
    const ctx = canvas.getContext("2d");

    canvas.width = imageElement.width;
    canvas.height = imageElement.height;

    ctx.drawImage(imageElement, 0, 0);

    const data = ctx.getImageData(
        0,
        0,
        canvas.width,
        canvas.height
    ).data;

    let colorPixels = 0;

    for (let i = 0; i < data.length; i += 4) {

        const r = data[i];
        const g = data[i + 1];
        const b = data[i + 2];

        if (
            Math.abs(r - g) > 15 ||
            Math.abs(r - b) > 15 ||
            Math.abs(g - b) > 15
        ) {
            colorPixels++;
        }
    }

    const percentage =
        (colorPixels / (data.length / 4)) * 100;

    console.log("Color Percentage:", percentage);

    return percentage < 5;
}
// ===============================
// CT IMAGE VALIDATION
// ===============================

const imageInput = document.getElementById("disease_image");

if (imageInput) {

    imageInput.addEventListener("change", function(event){

        const file = event.target.files[0];

        if (!file) {
            return;
        }

        // Allowed image types
        const allowedTypes = [
            "image/jpeg",
            "image/jpg",
            "image/png"
        ];

        // Check image type
        if (!allowedTypes.includes(file.type)) {

            alert("Please upload valid Brain CT image only");

            event.target.value = "";

            return;
        }

        // Check file size
        const maxSize = 10 * 1024 * 1024;

        if (file.size > maxSize) {

            alert("Image size must be less than 10MB");

            event.target.value = "";

            return;
        }

        // Validate image dimensions
        const img = new Image();

        img.onload = function(){

            if (img.width < 50 || img.height < 50) {

                alert("Please upload clear CT scan image");

                imageInput.value = "";

                return;
            }

            // Success
            alert("Valid image selected");

        };

        img.onerror = function(){

            alert("Invalid image file");

            imageInput.value = "";

        };

        img.src = URL.createObjectURL(file);

    });

}
// ===============================
// DOB FORMAT VALIDATION
// ===============================

const dobInput = document.querySelector('input[name="dob"]');

if (dobInput) {

    dobInput.addEventListener("change", function(){

        const dobValue = dobInput.value;

        if (!dobValue) {

            alert("Please enter DOB in correct format");

            dobInput.focus();
        }

    });

}

// ===============================
// IMAGE PREVIEW
// ===============================

document.addEventListener("DOMContentLoaded", function () {

    const imageInput =
        document.getElementById("disease_image");

    const previewContainer =
        document.getElementById("preview-container");

    const previewImage =
        document.getElementById("preview-image");

    if (!imageInput) return;

    imageInput.addEventListener("change", function () {

        const file = this.files[0];

        if (!file) {
            previewContainer.style.display = "none";
            return;
        }

        const reader = new FileReader();

        reader.onload = function (e) {

            previewImage.src = e.target.result;

            previewContainer.style.display = "block";
        };

        reader.readAsDataURL(file);

    });

});