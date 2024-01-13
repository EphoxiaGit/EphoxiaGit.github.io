$(document).ready(function() {
    const uploadForm = $("#upload-form");
    const submitButton = $("#submit-button");
    const resultDiv = $("#result");

    uploadForm.on("submit", function(event) {
        event.preventDefault();

        const stlFile = $("#stl-file")[0].files[0];

        if (!stlFile) {
            alert("Please select an STL file");
            return;
        }

        $.ajax({
            url: "/",
            method: "POST",
            data: new FormData(this),
            enctype: "multipart/form-data",
            processData: false,
            contentType: false,
            success: function(response) {
                // Parse JSON response
                const parsedResponse = JSON.parse(response);

                // Extract volume and surface area values
                const volume = parsedResponse.volume;
                const surfaceArea = parsedResponse.surfaceArea;

                // Extract filename
                const filename = encodeURIComponent(stlFile.name);

                // Construct URL for result page with query parameters
                const url = "result.html?stl_file=" + filename;

                // Redirect to result page with calculated values
                window.location = url;
            }
        });
    });
});
