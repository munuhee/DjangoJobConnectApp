$(document).ready(function() {
  $(window).scroll(function() {
    if ($(this).scrollTop() > 100) {
      $('#back-to-top-btn').removeClass('d-none');
    } else {
      $('#back-to-top-btn').addClass('d-none');
    }
  });

  $('#back-to-top-btn').click(function() {
    $('html, body').animate({scrollTop : 0},800);
    return false;
  });
});