function eliminar_usuario(item, name_item) {
    $('#datosUsuario').html(name_item);
    $('#idUsuario').val(item);
    $('#alertaEliminar').modal('show');
}
$(function(){
    $('#tb_usuarios').DataTable();
    $('.dataTables_length').addClass('bs-select');
    $('#aceptarEliminar').click(() => {
        location = '/autenticacion/usuario/eliminar/' + $('#idUsuario').val() + '/';
    });
});