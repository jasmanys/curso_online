const cargando = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>';
const err = 'Iniciar sesión';
var cls = $('#btnLogin').attr('class');
$('#alert-contenido');
$('#frm').on('submit', () => {
    $('#btnLogin').html(cargando);
    $('#btnLogin').attr("disabled", true);
});