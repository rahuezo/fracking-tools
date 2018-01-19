$(document).ready(function(){
  $(window).keydown(function(event){
    if(event.keyCode == 13) {
      event.preventDefault();
      return false;
    }
  });
});

function submit_form() {
  let events_form = $('#events-form');
  if(events_form.find('input:file')[0].files.length > 1 && events_form.find('input:text').val().length > 0) {
    $('#number-of-files').text(events_form.find('input:file')[0].files.length);
    events_form.submit();
    events_form[0].reset();
    $('#empty-fields-alert').fadeOut();
    $('#networks-built-alert').fadeIn();
  } else {
    $('#empty-fields-alert').fadeIn();
  }
}
