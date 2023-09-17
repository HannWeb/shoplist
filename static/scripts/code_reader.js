//let barcodeButton = document.getElementById("barcodeButton")
//let dismissModal = document.getElementById("barcodeModal")
//
////qr config details
//function startScanning (){
//const config = {
//                fps: 20,    // Frames per seconds for qr code scanning
//                qrbox: { width: 250, height: 150 }  // Bounded box UI
//                }
//// read for cameras
//// todo: list cameras on a select
//    Html5Qrcode.getCameras().then(devices => {
//        if (devices && devices.length) {
//            var cameraId = devices[0].id;
//            const html5QrCode = new Html5Qrcode("reader");
//            html5QrCode.start(cameraId, config, (decodedText, decodedResult) => {
//                console.log("decoded Tex: ", decodedText);
//                $("#myBtn").click(function() {
//                    $("#myModal").modal("hide");
//                });
//                html5QrCode.stop().then((ignore) => {
//                    console.log("camera stopped")
//                }).catch((err) => {
//                    console.log("camera still running")
//                });
//            }).catch(err => {
//                console.log("this is the camera error: ", err)
//            })
//        }
//    }
//)}
//
//
//
//
//barcodeButton.addEventListener("onclick", onclick = startScanning)
//dismissModal.addEvent Listener("onclick", onclick = closeCamera)




function onScanSuccess(decodedText, decodedResult) {
    // Handle on success condition with the decoded text or result.
    console.log(decodedText)
    console.log(html5QrcodeScanner)
    document.getElementById("barcode").value = decodedText;
    document.getElementById("closeModal").click();
    html5QrcodeScanner.clear();
    // ^ this will stop the scanner (video feed) and clear the scan area.
}

function test () {
    console.log(html5QrcodeScanner)
}

var html5QrcodeScanner = new Html5QrcodeScanner( "reader", { fps: 10, qrbox: 250, rememberLastUsedCamera: false });




var barcodeButton = document.getElementById("barcodeButton")
var dismissModal = document.getElementById("closeModal")

dismissModal.addEventListener("onclick", onclick = test);
barcodeButton.addEventListener("onclick", onclick = html5QrcodeScanner.render(onScanSuccess));