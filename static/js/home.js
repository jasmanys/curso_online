
$(function(){
    $('.nav-item').hover(function(){
        $('.undercontainer').css({'margin-top':'-5px'});
    }, function(){
        $('.undercontainer').css({'margin-top':'0px'});
    });
    $('.nav-item').hover(function(){
        $('#logo1').css({'margin-bottom':'5px'});
    }, function(){
        $('#logo1').css({'margin-bottom':'0px'})});
});
