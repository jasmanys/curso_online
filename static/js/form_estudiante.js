const cargando = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>';
const err = 'Siguiente';
$(function () {
    if(typeof editar !== 'undefined'){
        var f = __id12458ase2.split('value')[1].split('"')[1].split('/');
        $('#id_fecha_nacimiento').val(f[2]+'-'+f[1]+'-'+f[0]);
    }
    $('label').each(function () {
            $(this).attr('class', 'text-muted');
        }
    );
    $('#frm').submit(function (e) {
        if(typeof __id12458ase25 == 'undefined'){
            if($('#id_password').val()!=$('#id_password2').val()){
                e.preventDefault();
                $('#confirmar_pass').attr('class','form-text text-danger font-weight-bold');
                return;
            }else{
                $('#confirmar_pass').attr('class','form-text text-info');
            }
        }
        $('#guardar').html(cargando);
        $('#guardar').attr("disabled", true);
    });
});