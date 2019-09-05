const cargando = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>';
const err = 'Guardar';

$(function () {
   $('#frm').submit(function () {
       $('#guardar').html(cargando);
        $('#guardar').attr("disabled", true);
   }); 
});