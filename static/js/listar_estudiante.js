function eliminar_estudiante(item, name_item) {
    var arr = name_item.split(';');
    $('#datosEst').html('Usuario: ' + arr[0] + ' - Cédula: ' + arr[1] + ' - Nombres: ' + arr[2]);
    $('#idEstudiante').val(item);
    $('#alertaEliminar').modal('show');
}
$(function(){
    $('#tb_estudiantes').DataTable();
    $('.dataTables_length').addClass('bs-select');
    $('#aceptarEliminar').click(() => {
        location = '/estudiante/eliminar/' + $('#idEstudiante').val() + '/';
    });
});