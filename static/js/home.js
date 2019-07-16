
$(function(){
    $('.navbar-nav>.nav-item').hover(function(){
        $('.undercontainer').css({'margin-top':'-5px'});
        $('#logo1').css({'margin-bottom':'5px'});
    }, function(){
        $('#logo1').css({'margin-bottom':'0px'})
        $('.undercontainer').css({'margin-top':'0px'});
    });
});
