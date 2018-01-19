function submit_form() {
  let pairs_form = $('#pairs-form');
  if(pairs_form.find('input:file').val().length > 0 && pairs_form.find('input:text').val().length > 0) {
    pairs_form.submit();
    pairs_form[0].reset();
    $('#empty-fields-alert').fadeOut();
    $('#networks-built-alert').fadeIn();
  } else {
    $('#empty-fields-alert').fadeIn();
  }
}
