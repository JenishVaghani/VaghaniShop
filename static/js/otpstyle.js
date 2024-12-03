// Auto-focus logic
const otpInputs = document.querySelectorAll('.otp-input');
otpInputs.forEach((input, index) => {
    input.addEventListener('input', () => {
        if (input.value.length === 1 && index < otpInputs.length - 1) {
            otpInputs[index + 1].focus();
        }
    });
});

// Resend OTP click event
const resendLink = document.getElementById('resend-link');
resendLink.addEventListener('click', (e) => {
    e.preventDefault();
    alert('A new OTP has been sent!');
    // Logic for resending OTP goes here
});