const cargando = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>';
const err = 'Iniciar sesión';
$('#alert-contenido');
$('#frm').on('submit', () => {
    $('#btnLogin').html(cargando);
});