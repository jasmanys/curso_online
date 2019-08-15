function eliminar_enunciado(item, name_item) {
    $('#tituloEnunciado').html(name_item);
    $('#idEnunciado').val(item);
    $('#alertaEliminar').modal('show');
}
$(function(){
    $('#tb_submodulos').DataTable();
    $('.dataTables_length').addClass('bs-select');
    $('#aceptarEliminar').click(() => {
        location = '/evaluacion/eliminar/enunciado/' + $('#idEnunciado').val() + '/';
    });
});