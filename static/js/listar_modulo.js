function eliminar_modulo(item, name_item) {
    $('#tituloModulo').html(name_item);
    $('#idModulo').val(item);
    $('#alertaEliminar').modal('show');
}
$(function(){
    $('#tb_modulos').DataTable();
    $('.dataTables_length').addClass('bs-select');
    $('#aceptarEliminar').click(() => {
        location = '/curso/modulo/eliminar/' + $('#idModulo').val() + '/';
    });
});