const cargando = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>';
const err = 'Guardar Módulo';
function button_enunciado(label, funcion){
    var html = '<div class="input-group mb-3">';
    html += '<div class="input-group-prepend">';
    html += '<span class="input-group-text" id="basic-addon1">'+ label + '</span>';//Agregar Opción
    html += '</div>';
    html += '<input id="desc" type="text" class="form-control" aria-label="Opcion" aria-describedby="basic-addon1"/>';
    html += '<div class="input-group-append">';
    html += '<button onclick="' + funcion + '" title="Agregar" class="btn btn-outline-info" type="button" id="add">';
    html += '<i class="fas fa-folder-plus"></i>';
    html += '</button>';
    html += '</div>';
    html += '</div>';
    return html;
}
function addImage(idImg){
    var file = $('#fileImg')[0].files[0];
    imageType = /image.*/;

    if (!file.type.match(imageType)){
        return;
    }
    var reader = new FileReader();
    reader.onload = function (e) {
        var result=e.target.result;
        $('#'+idImg).attr("src",result);
    };
    reader.readAsDataURL(file);
}
function button_enunciado_file(label, funcion){
    var html = '<div class="input-group mb-3">';
    html += '<div class="input-group-prepend">';
    html += '<span class="input-group-text" id="basic-addon1">'+ label + '</span>';//Agregar Opción
    html += '</div>';
    html += '<input title="Imagen para la opción" id="fileImg" style="cursor:pointer;" type="file" accept="image/*" class="form-control pb-5 pt-3" aria-label="Opcion" aria-describedby="basic-addon1"/>';
    html += '<div class="input-group-append">';
    html += '<button onclick="' + funcion + '" title="Agregar" class="btn btn-outline-info" type="button" id="add">';
    html += '<i class="fas fa-folder-plus"></i>';
    html += '</button>';
    html += '</div>';
    html += '</div>';
    return html;
}
function agregar_opcion_img_rm(){
    if($('#fileImg')[0].files.length > 0){
        var c = $('#containerEnunciados>.custom-checkbox').length + 1;
        var contenido = $('#containerEnunciados>.custom-checkbox').toArray();
        var check = $('#containerEnunciados>.custom-checkbox .custom-control-input').toArray();
        var valores = '';
        var valores_select = '';
        for(var i = 0; i < contenido.length; i++){
            valores += valor_checkbox_img(i+1, '<img id="imgfc'+ (i+1) +'" class="img-fluid" src="'+ $('#imgfc'+(i+1)).attr('src')+'" width="200px"/>', $('#imgfc'+(i+1)).attr('src'));
            valores_select += '<option value="' + $('#imgfc'+(i+1)).attr('src') +'" selected>' + $('#imgfc'+(i+1)).attr('src') + '</option>';
        }
        valores += valor_checkbox_img(c, '<img id="imgfc'+ c +'" class="img-fluid" src="" width="200px"/>', 'None');
        valores_select += '<option value="' + c +'" selected>' + 'nel' + '</option>';
        valores += '<input type="hidden" id="tipo_enunciado" value="" />';
        $('#containerEnunciados').html(valores);
        $('#id_lista_de_enunciados').html(valores_select);
        $('#tipo_enunciado').val($('#id_tipo_respuesta option:selected').val());
        check = $('#containerEnunciados>.custom-checkbox .custom-control-input').toArray();
        $(check[0]).attr('checked', 'checked');
        var temp = $('#id_lista_de_enunciados>option').toArray();
        $(temp[0]).val($(temp[0]).val()+'|true');
        $(temp[0]).html($(temp[0]).val());
        addImage('imgfc'+c);
        $('#fileImg').val(null);
    }
}
function agregar_opcion_img_ru(){
    if($('#fileImg')[0].files.length > 0){
        var c = $('#containerEnunciados>.custom-radio').length + 1;
        var contenido = $('#containerEnunciados>.custom-radio').toArray();
        var radio = $('#containerEnunciados>.custom-radio .custom-control-input').toArray();
        var valores = '';
        var valores_select = '';
        for(var i = 0; i < contenido.length; i++){
            valores += valor_radio_img(i+1, '<img id="imgfc'+ (i+1) +'" class="img-fluid" src="'+ $('#imgfc'+(i+1)).attr('src')+'" width="200px"/>', $('#imgfc'+(i+1)).attr('src'));
            valores_select += '<option value="' + $('#imgfc'+(i+1)).attr('src') +'" selected>' + $('#imgfc'+(i+1)).attr('src') + '</option>';
        }
        valores += valor_radio_img(c, '<img id="imgfc'+ c +'" class="img-fluid" src="" width="200px"/>', 'None');
        valores_select += '<option value="' + c +'" selected>' + 'None' + '</option>';
        valores += '<input type="hidden" id="tipo_enunciado" value="" />';
        $('#containerEnunciados').html(valores);
        $('#id_lista_de_enunciados').html(valores_select);
        $('#tipo_enunciado').val($('#id_tipo_respuesta option:selected').val());
        radio = $('#containerEnunciados>.custom-radio .custom-control-input').toArray();
        $(radio[0]).attr('checked', 'checked');
        var temp = $('#id_lista_de_enunciados>option').toArray();
        $(temp[0]).val($(temp[0]).val()+'|true');
        $(temp[0]).html($(temp[0]).val());
        addImage('imgfc'+c);
        $('#fileImg').val(null);
    }
}
function valor_checkbox_img(item, val_item, src_img) {
    var valores = '';
    var outImg = val_item;
    valores += '<div style="cursor: pointer;" id="fc' + item + '" class="custom-control custom-checkbox my-1">';
    valores += '<input name="lista_enunciado[' + item + ']" value="' + src_img + '" style="cursor: pointer;" type="checkbox" class="custom-control-input" id="lista_enunciado' + item + '">';
    valores += '<label style="cursor: pointer;" class="custom-control-label" for="lista_enunciado' + item + '">' + outImg + '</label>';
    valores += '</div>';
    //addImage('imgfc' + item);
    return valores;
}
function valor_radio_img(item, val_item, src_img) {
    var valores = '';
    var outImg = val_item;
    valores += '<div style="cursor: pointer;" id="fr' + item + '" class="custom-control custom-radio my-1 mr-sm-2">';
    valores += '<input name="lista_enunciado" value="' + src_img + '" style="cursor: pointer;" type="radio" class="custom-control-input" id="lista_enunciado' + item + '">';
    valores += '<label style="cursor: pointer;" class="custom-control-label" for="lista_enunciado' + item + '">' + outImg + '</label>';
    valores += '</div>';
    //addImage('imgfc' + item);
    return valores;
}
function no_desc_empty() {
    if($('#desc').val() != ''){
        return true;
    }else{
        return false;
    }
}
function valor_checkbox(item, val_item) {
    var valores = '';
    valores += '<div style="cursor: pointer;" id="fc' + item + '" class="custom-control custom-checkbox my-1">';
    valores += '<input name="lista_enunciado[' + item + ']" value="' + val_item + '" style="cursor: pointer;" type="checkbox" class="custom-control-input" id="lista_enunciado' + item + '">';
    valores += '<label style="cursor: pointer;" class="custom-control-label" for="lista_enunciado' + item + '">' + val_item + '</label>';
    valores += '</div>';
    return valores;
}
function valor_radio(item, val_item) {
    var valores = '';
    valores += '<div style="cursor: pointer;" id="fr' + item + '" class="custom-control custom-radio my-1 mr-sm-2">';
    valores += '<input name="lista_enunciado" value="' + val_item + '" style="cursor: pointer;" type="radio" class="custom-control-input" id="lista_enunciado' + item + '">';
    valores += '<label style="cursor: pointer;" class="custom-control-label" for="lista_enunciado' + item + '">' + val_item + '</label>';
    valores += '</div>';
    return valores;
}
function agregar_opcion_rm(){
    if(no_desc_empty()){
        var c = $('#containerEnunciados>.custom-checkbox').length + 1;
        var contenido = $('#containerEnunciados>.custom-checkbox').toArray();
        var check = $('#containerEnunciados>.custom-checkbox .custom-control-input').toArray();
        var valores = '';
        var valores_select = '';
        for(var i = 0; i < contenido.length; i++){
            valores += valor_checkbox(i+1, $(check[i]).val());
            valores_select += '<option value="' + $(check[i]).val() +'" selected>' + $(check[i]).val() + '</option>';
        }
        valores += valor_checkbox(c, $('#desc').val());
        valores_select += '<option value="' + $('#desc').val() +'" selected>' + $('#desc').val() + '</option>';
        valores += '<input type="hidden" id="tipo_enunciado" value="" />';
        $('#containerEnunciados').html(valores);
        $('#id_lista_de_enunciados').html(valores_select);
        $('#tipo_enunciado').val($('#id_tipo_respuesta option:selected').val());
        check = $('#containerEnunciados>.custom-checkbox .custom-control-input').toArray();
        $(check[0]).attr('checked', 'checked');
        var temp = $('#id_lista_de_enunciados>option').toArray();
        $(temp[0]).val($(temp[0]).val()+'|true');
        $(temp[0]).html($(temp[0]).val());
        $('#desc').val('');
    }
}
function agregar_opcion_ru(){
    if(no_desc_empty()){
        var c = $('#containerEnunciados>.custom-radio').length + 1;
        var contenido = $('#containerEnunciados>.custom-radio').toArray();
        var radio = $('#containerEnunciados>.custom-radio .custom-control-input').toArray();
        var valores = '';
        var valores_select = '';
        for(var i = 0; i < contenido.length; i++){
            valores += valor_radio(i+1, $(radio[i]).val());
            valores_select += '<option value="' + $(radio[i]).val() +'" selected>' + $(radio[i]).val() + '</option>';
        }
        valores += valor_radio(c, $('#desc').val());
        valores_select += '<option value="' + $('#desc').val() +'" selected>' + $('#desc').val() + '</option>';
        valores += '<input type="hidden" id="tipo_enunciado" value="" />';
        $('#containerEnunciados').html(valores);
        $('#id_lista_de_enunciados').html(valores_select);
        $('#tipo_enunciado').val($('#id_tipo_respuesta option:selected').val());
        radio = $('#containerEnunciados>.custom-radio .custom-control-input').toArray();
        $(radio[0]).attr('checked', 'checked');
        var temp = $('#id_lista_de_enunciados>option').toArray();
        $(temp[0]).val($(temp[0]).val()+'|true');
        $(temp[0]).html($(temp[0]).val());
        $('#desc').val('');
    }
}
$(function () {
    var containerEnunciados = $('#containerEnunciados');
    var containerButton = $('#containerButton');
    $('#id_tipo_respuesta').change(function () {
        var html = '';
        var tipo_enunciado = $('#id_tipo_respuesta option:selected').val();
        if(tipo_enunciado != ''){
            $(containerEnunciados).html('');
            $('#id_lista_de_enunciados').html('');
            switch (tipo_enunciado) {
                case '0':
                    html=button_enunciado('Agregar Opcion', 'agregar_opcion_ru()');
                    break;
                case '1':
                    html=button_enunciado('Agregar Opcion', 'agregar_opcion_rm()');
                    break;
                case '2':
                    html=button_enunciado_file('Agregar Imagen', 'agregar_opcion_img_ru()');
                    break;
                case '3':
                    html=button_enunciado_file('Agregar Imagen', 'agregar_opcion_img_rm()');
                    break;
            }
        }
        $(containerButton).html(html);
    });
    $('body').on('change', '#containerEnunciados>.custom-checkbox .custom-control-input', function () {
        var arr = $('#containerEnunciados>.custom-checkbox .custom-control-input').toArray();
        var valores_select = '';
        for(var i = 0; i < arr.length; i++){
            if($(arr[i]).is(':checked')){
                valores_select += '<option value="' + $(arr[i]).val() +'|true" selected>' + $(arr[i]).val() + '|true</option>';
            }else{
                valores_select += '<option value="' + $(arr[i]).val() +'" selected>' + $(arr[i]).val() + '</option>';
            }
        }
        $('#id_lista_de_enunciados').html(valores_select);
    });
    $('body').on('change', '#containerEnunciados>.custom-radio .custom-control-input', function () {
        var arr = $('#containerEnunciados>.custom-radio .custom-control-input').toArray();
        var valores_select = '';
        for(var i = 0; i < arr.length; i++){
            if($(arr[i]).is(':checked')){
                valores_select += '<option value="' + $(arr[i]).val() +'|true" selected>' + $(arr[i]).val() + '|true</option>';
            }else{
                valores_select += '<option value="' + $(arr[i]).val() +'" selected>' + $(arr[i]).val() + '</option>';
            }
        }
        $('#id_lista_de_enunciados').html(valores_select);
    });
    $('#guardar').on('click',(e) =>{
        var tipo_enunciado = $('#id_tipo_respuesta option:selected').val();
        if(tipo_enunciado == '2' || tipo_enunciado == '3'){
            switch (tipo_enunciado) {
                case '2':
                    var arr = $('#containerEnunciados>.custom-radio .custom-control-input').toArray();
                    break;
                case '3':
                    var arr = $('#containerEnunciados>.custom-checkbox .custom-control-input').toArray();
                    break;
            }
            var valores_select = '';
            for(var i = 0; i < arr.length; i++){
                if($(arr[i]).is(':checked')){
                    valores_select += '<option value="' + $('#imgfc'+(i+1)).attr('src') +'|true" selected>' + $('#imgfc'+(i+1)).attr('src') + '|true</option>';
                }else{
                    valores_select += '<option value="' + $('#imgfc'+(i+1)).attr('src') +'" selected>' + $('#imgfc'+(i+1)).attr('src') + '</option>';
                }
            }
            $(arr[arr.length - 1]).val($('#imgfc'+arr.length).attr('src'));
            $('#id_lista_de_enunciados').html(valores_select);
        }
        $('#guardar').html(cargando);
        $('#guardar').attr("disabled", true);
        $('#frm').submit();
    });
});