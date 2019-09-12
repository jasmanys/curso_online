const cargando = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>';
const err = 'Guardar SubMódulo';
var _cerrar = true;
$('#frm').on('submit',() =>{
    _cerrar = false;
    $('#guardar').html(cargando);
    $('#guardar').attr("disabled", true);
});
window.onbeforeunload = function() {
    if(_cerrar){
        var confirmar = confirm("¿Seguro que deseas cerrar la ventana?");
        if(confirmar){
            window.onunload = function () {
                return true;
            }
        }else{
            return false;
        }
    }
}