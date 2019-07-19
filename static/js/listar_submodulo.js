function eliminar_submodulo(item, name_item) {
    $('#tituloSubModulo').html(name_item);
    $('#idSubModulo').val(item);
    $('#alertaEliminar').modal('show');
}
$(function(){
    $('#tb_submodulos').DataTable();
    $('.dataTables_length').addClass('bs-select');
    $('#aceptarEliminar').click(() => {
        location = '/curso/submodulo/eliminar/' + $('#idSubModulo').val() + '/';
    });
});