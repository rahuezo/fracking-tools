$(document).ready(function(){
  $(window).keydown(function(event){
    if(event.keyCode == 13) {
      event.preventDefault();
      return false;
    }
  });
});

function keywordEntryHandler(element) {
  if($(element).text() == 'Input Keywords from File') {
    $(element).text('Manually Input Keywords');
    $(element).removeClass('btn-secondary').addClass('btn-dark');
    $('#manual-keywords').addClass('invisible');
    $('#file-keywords').removeClass('invisible');
    $('#file-keyword-list').val('');
    $('#keywords-type').val('file');

  } else {
    $(element).text('Input Keywords from File');
    $(element).removeClass('btn-dark').addClass('btn-secondary');
    $('#file-keywords').addClass('invisible');
    $('#manual-keywords').removeClass('invisible');
    $('#manual-keyword-list').val('');
    $('#keywords-type').val('manual');
  }
}

function submit_form() {
  let tag_files_form = $('#tag-files-form');
  if($('#analyze-documents')[0].files.length > 0
    && ($('#file-keyword-list')[0].files.length > 0 || $('#manual-keyword-list').val().length > 0)
    && $('#output-csv-name').val().length > 0) {
    $('#number-of-files').text($('#analyze-documents')[0].files.length);
    tag_files_form.submit();
    tag_files_form[0].reset();
    $('#empty-fields-alert').fadeOut();
    $('#networks-built-alert').fadeIn();
  } else {
    $('#empty-fields-alert').fadeIn();
  }
}
