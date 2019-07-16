function quitar(id){
    $('#containerModulos>#m'+id).remove();
}
function concatenar(i, valor){
    var html = ''
    html += '<div id="m' + i +'"  class="card">';
    html += '<input class="titulo_modulo" type="hidden" name="titulo_modulo['+ i +']" value="'+
    valor + '"/>';
    html += '<div class="card-header" id="h-'+ i +'">';
    html += '<h2 class="mb-0">';
    html += '<button class="btn btn-link" type="button" data-toggle="collapse"';
    html += 'data-target="#collapse-'+ i + '" aria-expanded="true" aria-controls="collapse-'+ i + '">';
    html += valor;
    html += '</button>';
    html += '<button onclick="quitar(&#39;'+ i +'&#39;)" title="Eliminar modulo" class="btn btn-outline-danger btn-sm" type="button">';
    html += '<i class="fas fa-times"></i>';
    html += '</button>';
    html += '</h2>';
    html += '</div>';
    html += '<div id="collapse-'+ i + '" class="collapse" aria-labelledby="h-'+ i +'" data-parent="#containerModulos">';
    html += '<div class="card-body text-justify text-break">';
    html += '<div class="input-group mb-3">';
    html += '<div class="input-group-prepend">';
    html += '<span class="input-group-text" id="basic-addon1">Título del AnteMódulo</span>';
    html += '</div>';
    html += '<input type="text" class="form-control tituloAnteModulo" placeholder="Ej: Introducción; Voltaje, corriente, potencia, sobrecarga, cortocircuito, circuito abierto. "aria-label="AnteModulo" aria-describedby="basic-addon1">';
    html += '<div class="input-group-append">';
    html += '<button title="Agregar un AnteMódulo para este módulo" class="btn btn-outline-success addTituloAnteModulo" type="button">';
    html += '<i class="fas fa-folder-plus"></i>';
    html += '</button>';
    html += '</div>';
    html += '</div>';
    html += '<div id="containerAnteModulos" class="accordion">';
    html += '';
    html += '';
    html += '';
    html += '';
    html += '';
    html += '';
    html += '';
    html += '</div>';
    html += '</div>';
    html += '</div>';
    html += '</div>';
    return html;
}
$(function(){
const cargando = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>';
        const err = 'Siguiente';
        $('#frm').on('submit',(e) =>{
            if($('#containerModulos>div').length > 0){
                $('#next').html(cargando);
            }else{
                e.preventDefault();
            }
        });
        $('#addModulo').on('click', function () {
            if($('#modTitulo').val() != ''){
                var c = $('#containerModulos>div').length + 1;
                var contenido = $('#containerModulos>div').toArray();
                var inputs = $('#containerModulos>div .titulo_modulo').toArray();
                var html = '';
                for(var i = 0; i < contenido.length; i++){
                    html += concatenar((i+1), $(inputs[i]).val());
                }
                html += concatenar(c, $('#modTitulo').val());
                //alert($(contenido[0]).html());
                $('#containerModulos').html(html);
                $('#modTitulo').val('');
            }else{
                $('#exampleModalCenter').modal('show');
            }
        });
        $('#exampleModalCenter').on('hidden.bs.modal', function () {
            $('#modTitulo').focus();
        });
});

/*
* function quitar(id){
        $('#containerModulos>#m'+id).remove();
    }
    function concatenar(i, valor){
        var html = ''
        html += '<tr id="m' + i +'">';
        html += '<td>';
        html += '<input class="titulo_modulo" type="hidden" name="titulo_modulo['+ i +']" value="'+
        valor + '"/>';
        html += valor;
        html += '</td>';
        html += '<td class="text-center">';
        html += '<button onclick="quitar(&#39;'+ i +'&#39;)" title="Eliminar modulo" class="btn btn-outline-danger btn-sm" type="button">';
        html += '<i class="fas fa-times"></i>';
        html += '</button>';
        html += '</td>';
        html += '</tr>';
        return html;
    }
    $('#addModulo').on('click', function () {
        if($('#modTitulo').val() != ''){
            var c = $('#containerModulos>tr').length + 1;
            var contenido = $('#containerModulos>tr').toArray();
            var inputs = $('#containerModulos>tr .titulo_modulo').toArray();
            var html = '';
            for(var i = 0; i < contenido.length; i++){
                html += concatenar((i+1), $(inputs[i]).val());
            }
            html += concatenar(c, $('#modTitulo').val());
            $('#containerModulos').html(html);
            $('#modTitulo').val('');
        }else{
            $('#exampleModalCenter').modal('show');
        }
    });
    $('#exampleModalCenter').on('hidden.bs.modal', function () {
        $('#modTitulo').focus();
    });
* */