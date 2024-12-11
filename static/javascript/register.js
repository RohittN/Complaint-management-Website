// Get form elements
const form = document.querySelector('.registration-form');
const firstNameInput = document.getElementById('firstname');
const lastNameInput = document.getElementById('lastname');
const emailInput = document.getElementById('email');
const phoneInput = document.getElementById('phone');
const usernameInput = document.getElementById('username');
const passwordInput = document.getElementById('password');
const confirmPasswordInput = document.getElementById('confpassword');

// Error message styling
const createErrorElement = (message) => {
    const error = document.createElement('div');
    error.className = 'invalid-feedback';
    error.style.display = 'block';
    error.style.color = 'red';
    error.style.fontSize = '14px';
    error.style.marginTop = '5px';
    error.textContent = message;
    return error;
};

// Remove existing error messages
const removeErrors = (input) => {
    const existingError = input.nextElementSibling;
    if (existingError && existingError.className === 'invalid-feedback') {
        existingError.remove();
    }
};

// Validation functions
const validateName = (input, fieldName) => {
    removeErrors(input);
    const name = input.value.trim();
    
    if (name === '') {
        const error = createErrorElement(`${fieldName} is required`);
        input.parentNode.appendChild(error);
        return false;
    }
    
    if (!/^[A-Za-z\s]{2,}$/.test(name)) {
        const error = createErrorElement(`${fieldName} should contain only letters and be at least 2 characters long`);
        input.parentNode.appendChild(error);
        return false;
    }
    
    return true;
};

const validateEmail = (input) => {
    removeErrors(input);
    const email = input.value.trim();
    
    if (email === '') {
        const error = createErrorElement('Email is required');
        input.parentNode.appendChild(error);
        return false;
    }
    
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
        const error = createErrorElement('Please enter a valid email address');
        input.parentNode.appendChild(error);
        return false;
    }
    
    return true;
};

const validatePhone = (input) => {
    removeErrors(input);
    const phone = input.value.trim();
    
    if (phone === '') {
        const error = createErrorElement('Phone number is required');
        input.parentNode.appendChild(error);
        return false;
    }
    
    if (!/^\d{10}$/.test(phone.replace(/\D/g, ''))) {
        const error = createErrorElement('Please enter a valid 10-digit phone number');
        input.parentNode.appendChild(error);
        return false;
    }
    
    return true;
};

const validateUsername = (input) => {
    removeErrors(input);
    const username = input.value.trim();
    
    if (username === '') {
        const error = createErrorElement('Username is required');
        input.parentNode.appendChild(error);
        return false;
    }
    
    if (!/^[A-Za-z0-9_]{3,20}$/.test(username)) {
        const error = createErrorElement('Username must be 3-20 characters long and can only contain letters, numbers, and underscores');
        input.parentNode.appendChild(error);
        return false;
    }
    
    return true;
};

const validatePassword = (input) => {
    removeErrors(input);
    const password = input.value;
    
    if (password === '') {
        const error = createErrorElement('Password is required');
        input.parentNode.appendChild(error);
        return false;
    }
    
    if (password.length < 8) {
        const error = createErrorElement('Password must be at least 8 characters long');
        input.parentNode.appendChild(error);
        return false;
    }
    
    if (!/(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*])/.test(password)) {
        const error = createErrorElement('Password must contain at least one uppercase letter, one lowercase letter, one number, and one special character');
        input.parentNode.appendChild(error);
        return false;
    }
    
    return true;
};

const validateConfirmPassword = (input) => {
    removeErrors(input);
    const confirmPassword = input.value.trim();
    const password = passwordInput.value.trim();
    
    if (confirmPassword === '') {
        const error = createErrorElement('Confirm password is required');
        input.parentNode.appendChild(error);
        return false;
    }
    
    if (confirmPassword !== password) {
        const error = createErrorElement('Passwords do not match');
        input.parentNode.appendChild(error);
        return false;
    }
    
    return true;
};

// Real-time validation
firstNameInput.addEventListener('blur', () => validateName(firstNameInput, 'First name'));
lastNameInput.addEventListener('blur', () => validateName(lastNameInput, 'Last name'));
emailInput.addEventListener('blur', () => validateEmail(emailInput));
phoneInput.addEventListener('blur', () => validatePhone(phoneInput));
usernameInput.addEventListener('blur', () => validateUsername(usernameInput));
passwordInput.addEventListener('blur', () => validatePassword(passwordInput));
confirmPasswordInput.addEventListener('blur', () => validateConfirmPassword(confirmPasswordInput));

// Form submission
form.addEventListener('submit', (e) => {
    e.preventDefault();
    
    const isFirstNameValid = validateName(firstNameInput, 'First name');
    const isLastNameValid = validateName(lastNameInput, 'Last name');
    const isEmailValid = validateEmail(emailInput);
    const isPhoneValid = validatePhone(phoneInput);
    const isUsernameValid = validateUsername(usernameInput);
    const isPasswordValid = validatePassword(passwordInput);
    const isConfirmPasswordValid = validateConfirmPassword(confirmPasswordInput);
    
    if (isFirstNameValid && isLastNameValid && isEmailValid && isPhoneValid && isUsernameValid && isPasswordValid && isConfirmPasswordValid) {
        // If all validations pass, submit the form
        form.submit();
    }
});
