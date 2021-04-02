
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
            // $('#response').show();

            var numberOfDots = 0
            var uploadingText = setInterval(function () {
                numberOfDots = numberOfDots % 3 + 1
                console.log(numberOfDots)
                $('#text').text(`Uploading file${'.'.repeat(numberOfDots)}`);
            }, 350);


            $(this).ajaxSubmit({
                uploadProgress: function(event, position, total, percentageComplete) {
                    if (percentageComplete === 100) {
                        clearInterval(uploadingText)
                        $('#text').text('File uploaded succesfully. Processing...')
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
                        $('#text').text('Select an audio file (mp3 or wav)');
                        $('#user-message').fadeIn();
                        $('#user-message').text(data["error"]);
                    }
                }
            })
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

    $('#uploadAudio').on('change', '#file-upload', function () {
        $('#uploadAudio').submit();
    });
});
