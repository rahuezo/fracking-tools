function submit_form() {
  let comparison_form = $('#comparison-form');

  if(comparison_form.find('input:file').val().length > 0 && comparison_form.find('input:text').val().length > 0) {
    comparison_form.submit();
    comparison_form[0].reset();
    $('#empty-fields-alert').fadeOut();
    $('#networks-built-alert').fadeIn();
  } else {
    $('#empty-fields-alert').fadeIn();
  }
}
