document.addEventListener("DOMContentLoaded", function() {
    const html5QrCode = new Html5Qrcode("reader");
    const scanForm = document.getElementById("scanForm");
    const scanDataInput = document.getElementById("scan_data");

    html5QrCode.start(
        { facingMode: "environment" }, // Use back camera if available
        {
            fps: 10, // Frames per second for scanning
            qrbox: 250, // Define scan area size
        },
        qrCodeMessage => {
            scanDataInput.value = qrCodeMessage;
            scanForm.submit();
        },
        errorMessage => {
            // Handle errors here (optional)
            console.log(`QR code parse error, error = ${errorMessage}`);
        }
    ).catch(err => {
        console.log("Error in starting the QR code scanner:", err);
    });
});
