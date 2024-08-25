const html5QrCode = new Html5Qrcode("reader");

function onScanSuccess(decodedText, decodedResult) {
    document.getElementById("result").innerHTML = decodedText;
}

function onScanFailure(error) {
    console.log("Error: ", error);
}

html5QrCode.start(
    { facingMode: "environment" },
    {
        fps: 10,
        qrbox: 250
    },
    onScanSuccess,
    onScanFailure
);