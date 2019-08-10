const cargando = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>';
const err = 'Siguiente';
$(function () {
    $('#frm').on('submit',(e) =>{
        if($('#id_check_contrasena').is(':checked')){
            if($('#id_contrasena').val() != $('#id_confirmar_contrasena').val()){
                e.preventDefault();
                $('#no_coincide').removeAttr('style');
                return;
            }else{
                $('#no_coincide').attr('style', 'display:none;');
            }
        }
        $('#guardar').html(cargando);
        $('#guardar').attr("disabled", true);
    });
    $('#id_check_contrasena').change(function () {
        if($(this).is(':checked')){
            $('#p_id_contrasena, #p_id_confirmar_contrasena').removeAttr('style');
            $('#id_contrasena, #id_confirmar_contrasena').attr('required','required');
        }else{
            $('#p_id_contrasena, #p_id_confirmar_contrasena').attr('style','display: none;');
            $('#id_contrasena, #id_confirmar_contrasena').removeAttr('required');
        }
    });
    var helpText = $('.helptext');
    var text = '';
    for(var i = 0; i < helpText.length; i++)
    {
        text = $(helpText[i]).html();
        $(helpText[i]).replaceWith('<small class="form-text text-info">' + text + '</small>');
    }
});