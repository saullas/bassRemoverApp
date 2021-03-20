
$(document).ready(function (){
    $('#download-group').hide();
    $('#user-message').hide();

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
            $('#response').show();
            $('#text').text('Uploading file');
            $(this).ajaxSubmit({
                target: '#file-progress',
                uploadProgress: function(event, position, total, percentageComplete) {
                    $('.progress').animate({
                        value: percentageComplete
                    }, {
                        duration: 5000
                    });

                    if (percentageComplete === 100) {
                        $('#text').text('Uploaded succesfully. Processing...')
                        $('#response').hide()
                        $('#loading-overlay').fadeIn()
                    }
                },
                success: function(data) {
                    if (data['status'] === 200) {
                        $('#text').text("Finished. Click to process another file.");
                        $('#download').attr("href", '/downloadAudio/' + data["filename"]);
                        $('#underDownload').attr("href", '/downloadAudio/' + data["filename"]);
                        $('#loading-overlay').fadeOut()
                        $('#download-group').fadeIn(2000);
                    }
                    else {
                        $('#loading-overlay').fadeOut()
                        $('#user-message').fadeIn();
                        $('#user-message').text(data["error"]);
                    }
                }
            })
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

    $('#uploadAudio').on('change', '#file-upload', function () {
        $('#uploadAudio').submit();
    });
});
