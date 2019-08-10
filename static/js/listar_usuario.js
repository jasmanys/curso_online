/*function eliminar_modulo(item, name_item) {
    $('#tituloModulo').html(name_item);
    $('#idModulo').val(item);
    $('#alertaEliminar').modal('show');
}*/
$(function(){
    $('#tb_usuarios').DataTable();
    $('.dataTables_length').addClass('bs-select');
    /*$('#aceptarEliminar').click(() => {
        location = '/curso/modulo/eliminar/' + $('#idModulo').val() + '/';
    });*/
});