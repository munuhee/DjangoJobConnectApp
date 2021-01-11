$(window).load(function() {
  $('.post-card').hover(function() {
    $(this).find('.description').stop().animate({
      height: "toggle",
      opacity: "toggle"
    }, 300);
  });
});