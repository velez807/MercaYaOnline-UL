$(function () {
    var cedula, contraseña ;
    $(".btnAction").on('click', function () {
        cedula = $(".cedula").val();
        contraseña = $(".contraseña").val();

        if (cedula.length == 0 || contraseña.length == 0 ) {
            alert("Hay campos vacios");
        } 
        else {$(".formulario").submit();}
        


    });
});