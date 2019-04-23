$(document).ready(function() {
    $('#password, #password_confirmation').on('keyup', function () {
      if ($('#password').val() == $('#password_confirmation').val()) {
        $('#message').html('Matching').css('color', 'green');
      } else
        $('#message').html('Not matching!').css('color', 'red');
    });
    }