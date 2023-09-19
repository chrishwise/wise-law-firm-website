/*
    This file listens for the change of the file input with id: "picture", and uploads it to S3 cloud storage.

    Needs the following elements:

    <input id="picture">
    <input type="hidden" name="image-url" id="image-url">
    <progress id="progressBar" value="0" max="100"></progress>
    <p id="uploadStatus"></p>
    <div id="preview-container"></div>
 */

(function(){
    document.getElementById("picture").onchange = function () {
        var files = document.getElementById("picture").files;
        console.log(files)
        var file = files[0];
        if (!file) {
            return alert("No picture selected.");
        }
        Array.from(files).forEach(file => {
            getSignedRequest(file);
        });
    };
})();

function appendStatus(message) {
    document.getElementById('uploadStatus').innerText += message + "\n";
}

function getSignedRequest(file) {
    var xhr = new XMLHttpRequest();
    xhr.open("GET", "/sign_s3?file_name=" + file.name + "&file_type=" + file.type);
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                var response = JSON.parse(xhr.responseText);
                appendStatus(file.name + ": Successfully got signed request")
                uploadFile(file, response.data, response.url);
            } else {
                appendStatus("Error. The GET signed request returned the following response message: " + xhr.statusText);
            }
        }
    };
    xhr.send();
}

function progressHandler(event) {
    var percent = (event.loaded / event.total) * 100;
    document.getElementById("progressBar").value = Math.round(percent);
}

function uploadFile(file, s3Data, url) {
    var xhr = new XMLHttpRequest();
    xhr.upload.addEventListener('progress', progressHandler, false)
    xhr.open("POST", s3Data.url);
    var postData = new FormData();
    for (key in s3Data.fields) {
        postData.append(key, s3Data.fields[key]);
    }
    postData.append('file', file);
    // Attach event handler
    xhr.onreadystatechange = function () {
        // If the request is complete
        if (xhr.readyState === 4) {
            // If the request was successful
            if (xhr.status === 200 || xhr.status === 204) {
                appendStatus(file.name + ': Upload Complete')
                // Set the value of the form's hidden input with the newly uploaded picture url
                document.getElementById('image-url').value = url;
                document.getElementById('picturePreview').src = url;
            } else {
                appendStatus(file.name + ': Upload Failed - status text: ' + xhr.statusText)
            }
        }
        ;
    }
    xhr.send(postData);
};