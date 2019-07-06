const cargando = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>';
const err = 'Iniciar sesión';
$('#alert-contenido');
$('#btnLogin').on('click', () => {
    $('#btnLogin').html(cargando);
});