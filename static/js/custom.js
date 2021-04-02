
$(document).ready(function (){
    var progressDiv = $('.myProgress')
    var progressBar = document.getElementById("myBar");

    $('#download-group').hide();
    $('#user-message').hide();
    progressDiv.hide();

    $('#download').on('click', function () {
        $('#download-group').fadeOut();
    });

    $('#uploadAudio').on('submit', function(event) {
        if($('#file-upload').val()) {
            event.preventDefault();
            if ($('#download-group').is(":visible")) {
                $('#download-group').fadeOut();
            }
            if ($('#user-message').is(":visible")) {
                $('#user-message').fadeOut();
            }
            $(this).ajaxSubmit({
                beforeSend: function () {
                    progressDiv.show()
                    $('#text').text('Uploading file...')
                },
                uploadProgress: function(event, position, total, percentageComplete) {
                    progressBar.style.width = percentageComplete + "%";

                    if (percentageComplete === 100) {
                        $('#text').text('File uploaded succesfully. Processing...')
                        $('#loading-overlay').fadeIn()
                    }
                },
                success: function(response) {
                    if (response['status'] === 200) {
                        $('#text').text("Finished. Click to process another file.");
                        $('#download').attr("href", '/downloadAudio/' + response["filename"]);
                        $('#underDownload').attr("href", '/downloadAudio/' + response["filename"]);
                        $('#loading-overlay').fadeOut()
                        $('#download-group').fadeIn(2000);
                    }
                    else {
                        $('#loading-overlay').fadeOut()
                        $('#text').text('Select an audio file (mp3 or wav)');
                        $('#user-message').fadeIn();
                        $('#user-message').text(response["error"]);
                    }
                },
                error: function (response) {
                    if(response.status === 413) {
                        $('#user-message').fadeIn();
                        $('#user-message').text("File too large");
                        $('#text').text('Select an audio file (mp3 or wav)');
                    }
                }
            })
            progressDiv.hide()
            progressBar.style.width = "0"
            $('#file-upload').val(undefined)
        }
        return false;
    });

    $('#url-submit').on('submit', function(event) {
        if($('#youtube-url-input').val()) {
            event.preventDefault();
            if ($('#download-group').is(":visible")) {
                $('#download-group').fadeOut();
            }
            if ($('#user-message').is(":visible")) {
                $('#user-message').fadeOut();
            }
            $('#loading-overlay').fadeIn()
            $(this).ajaxSubmit({
                success: function(data) {
                    if (data['status'] === 200) {
                        $('#download').attr("href", '/downloadAudio/' + data["filename"]);
                        $('#underDownload').attr("href", '/downloadAudio/' + data["filename"]);
                        $('#loading-overlay').fadeOut()
                        $('#download-group').fadeIn(2000);
                    }
                    else {
                        $('#loading-overlay').fadeOut();
                        $('#user-message').fadeIn();
                        $('#user-message').text(data["error"]);
                    }
                }
            })
        }
        return false;
    });

    $('#uploadAudio').on('change', '#file-upload', function (event) {
        const target = event.target
        if (target.files && target.files[0]) {
          const maxAllowedSize = 50 * 1024 * 1024;
          if (target.files[0].size > maxAllowedSize) {
            $('#user-message').fadeIn();
            $('#user-message').text("File too large");
          }
          else {
            $('#uploadAudio').submit();
          }
        }
    });
});
