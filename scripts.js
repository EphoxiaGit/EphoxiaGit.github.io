$(document).ready(function() {
  $('#stl_file').on('change', function() {
    $.ajax({
      url: "/",
      method: "POST",
      data: new FormData(this),
      enctype: 'multipart/form-data',
      processData: false,
      contentType: false,
      success: function(response) {
        $('#result').html(response);
      }
    });
  });
});
