$(function () {
    var nombre, cedula, correo, contraseña, tarjeta, codigo, fecha, direccion;
    $(".btnAction").on('click', function () {
        nombre = $(".nombre").val();
        cedula = $(".cedula").val();
        correo = $(".correo").val();
        contraseña = $(".contraseña").val();
        rcontraseña = $(".rcontraseña").val();
        tarjeta = $(".tarjeta").val();
        codigo = $(".codigo").val();
        fecha = $(".fecha").val();
        direccion = $(".direccion").val();

        if (nombre.length == 0 || cedula.length == 0 || correo.length == 0 || contraseña.length == 0 || rcontraseña.length == 0 || tarjeta.length == 0 || codigo.length == 0 || fecha.length == 0 || direccion.length == 0) {
            alert("Hay campos vacios");
        } else if (contraseña != rcontraseña) {
            alert("Las contraseñas no coinciden");}
        else {$(".formulario").submit();}
        


    });
});