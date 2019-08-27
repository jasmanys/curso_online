$(function(){
    $('#enviarEvaluacion').click(function () {
        var bandera = false;
        idEnunciados.forEach(function (element, index) {
            var enunciados = $(element+'>li>div>input').toArray();
            var contadorCheck = 0;
            enunciados.forEach(function (element2, index2) {
                if($(element2).is(':checked')){
                    contadorCheck++;
                }
            });
            if(contadorCheck==0){
                bandera = true;
                return;
            }
            if($(element).data('cantres')){
                if($(element).data('cantres')!=contadorCheck){
                    alert('Del enunciado: <'+$(element).data('enunciadoval')+'> debe contestar '+$(element).data('cantres')+' opciones');
                    bandera = true;
                    return;
                }
            }
        });
        if(bandera){
            alert('Debe contestar todo');
            return;
        }
        if(!bandera) {
            $('#frm').submit();
        }
    });
});