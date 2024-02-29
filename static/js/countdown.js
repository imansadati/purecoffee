var resendOtpTimer;
var resendOtpSeconds = 90; // Set the countdown duration in seconds

function formatTime(seconds) {
    var minutes = Math.floor(seconds / 60);
    var remainingSeconds = seconds % 60;
    return (minutes < 10 ? "0" : "") + minutes + ":" + (remainingSeconds < 10 ? "0" : "") + remainingSeconds;
}

function startResendOtpTimer() {
    var timerDisplay = document.getElementById("resend-otp-timer");
    var resendOtpButton = document.getElementById("resend-otp-button");

    function updateTimerDisplay() {
        if (resendOtpSeconds <= 0) {
            clearInterval(resendOtpTimer);
            timerDisplay.innerHTML = formatTime(0); // Display 00:00 when the timer ends
            resendOtpButton.style.display = "inline"; // Show the "Resend OTP" link
        } else {
            timerDisplay.innerHTML = formatTime(resendOtpSeconds);
            resendOtpSeconds--;
        }
    }

    updateTimerDisplay();
    resendOtpTimer = setInterval(updateTimerDisplay, 1000);
}

// Call the startResendOtpTimer function on both registration and verification pages
startResendOtpTimer();