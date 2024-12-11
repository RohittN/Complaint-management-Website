document.getElementById('complaintForm').addEventListener('submit', function(e) {
    // Validate title
    const title = document.getElementById('title').value.trim();
    if (!title) {
        alert("Title is required.");
        e.preventDefault();
        return;
    }

    // Validate genre (category)
    const genre = document.getElementById('genre').value;
    if (!genre) {
        alert("Please select a complaint category.");
        e.preventDefault();
        return;
    }

    // Validate image upload
    const image = document.getElementById('image').files[0];
    if (!image) {
        alert("Please upload an image.");
        e.preventDefault();
        return;
    }

    // Validate location
    const latitude = document.getElementById('latitude').value;
    const longitude = document.getElementById('longitude').value;
    if (!latitude || !longitude) {
        alert("Please get the location before submitting the complaint.");
        e.preventDefault();
        return;
    }

    // Validate phone number
    const phone = document.getElementById('phone').value.trim();
    const phonePattern = /^[0-9]{10}$/;  // Regular expression for 10-digit phone number
    if (!phone || !phonePattern.test(phone)) {
        alert("Please enter a valid 10-digit phone number.");
        e.preventDefault();
        return;
    }

    // Validate address
    const address = document.getElementById('address').value.trim();
    if (!address) {
        alert("Address is required.");
        e.preventDefault();
        return;
    }
});

// Display image preview on file selection
document.getElementById('image').addEventListener('change', function(event) {
    const preview = document.getElementById('preview');
    const imagePreview = document.getElementById('imagePreview');
    const file = event.target.files[0];

    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            preview.src = e.target.result;
            imagePreview.style.display = 'block';
        };
        reader.readAsDataURL(file);
    } else {
        imagePreview.style.display = 'none';
    }
});

// Get user location when the button is clicked
document.getElementById('getLocationBtn').addEventListener('click', function() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(position) {
            const latitude = position.coords.latitude;
            const longitude = position.coords.longitude;

            document.getElementById('latitude').value = latitude;
            document.getElementById('longitude').value = longitude;

            document.getElementById('locationMessage').style.display = 'none';
        }, function() {
            alert("Unable to retrieve location.");
        });
    } else {
        alert("Geolocation is not supported by this browser.");
    }
});
