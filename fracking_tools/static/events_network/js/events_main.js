function submit_form() {
  let events_form = $('#events-form');

  if(events_form.find('input:file').val().length > 0 && events_form.find('input:text').val().length > 0) {
    events_form.submit();
    events_form[0].reset();
    $('#empty-fields-alert').fadeOut();
    $('#networks-built-alert').fadeIn();
  } else {
    $('#empty-fields-alert').fadeIn();
  }
}

$(function () {
  $('[data-toggle="popover"]').popover()
})
