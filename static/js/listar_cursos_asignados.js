function eliminar_curso_asignado(item, name_item) {
    $('#datosEst').html(name_item);
    $('#idCursoAsignado').val(item);
    $('#alertaEliminar').modal('show');
}
$(function(){
    $('#tb_estudiantes').DataTable();
    $('.dataTables_length').addClass('bs-select');
    $('#aceptarEliminar').click(() => {
        location = '/estudiante/cursos_asignados/eliminar/' + $('#idCursoAsignado').val() + '/';
    });
});