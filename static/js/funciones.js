function message_error(obj) {
    var html = '';
    if (typeof (obj) === 'object') {
        html = '<ul style="text-align: left;">';
        $.each(obj, function (key, value) {
            html += '<li>' + key + ': ' + value + '</li>';
        });
        html += '</ul>';
    } else {
        html = '<p>' + obj + '</p>';
    }
    Swal.fire({
        title: 'Error!',
        html: html,
        icon: 'error'
    });
}

function filePreview(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function (e) {
            $('.cambiar').attr("src", e.target.result);
            // $('#cambiar').attr({"src":e.target.result, "height":"500px"});
        }
        reader.readAsDataURL(input.files[0]);

    }
}

function filePreviewPerfil(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function (e) {
            $('.cambiarperfil').attr("src", e.target.result);
            // $('#cambiar').attr({"src":e.target.result, "height":"500px"});
        }
        reader.readAsDataURL(input.files[0]);

    }
}
function filePreview2(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function (e) {
            $('.cambiar2').attr("src", e.target.result);
            // $('#cambiar').attr({"src":e.target.result, "height":"500px"});
        };
        reader.readAsDataURL(input.files[0]);

    }
}



function submit_with_ajax(url, title, content, parameters, callback) {
    $.confirm({
        theme: 'material',
        title: title,
        icon: '',
        content: content,
        columnClass: 'small',
        typeAnimated: true,
        cancelButtonClass: 'btn-primary',
        draggable: true,
        dragWindowBorder: false,
        buttons: {
            info: {
                text: "Si",
                btnClass: 'btn-primary',
                action: function () {
                    $.ajax({
                        url: url, //window.location.pathname
                        type: 'POST',
                        data: parameters,
                        dataType: 'json',
                        processData: false,
                        contentType: false,
                    }).done(function (data) {
                        // console.log(data);
                        if (!data.hasOwnProperty('error')) {
                            callback(data);
                            return false;
                        }
                        message_error(data.error);
                    }).fail(function (jqXHR, textStatus, errorThrown) {
                        alert(textStatus + ': ' + errorThrown);
                    }).always(function (data) {

                    });
                }
            },
            danger: {
                text: "No",
                btnClass: 'btn-red',
                action: function () {

                }
            },
        }
    });
}
function alerta_action(title, content, callback) {
    $.confirm({
        theme: 'material',
        title: title,
        icon: '',
        content: content,
        columnClass: 'small',
        typeAnimated: true,
        cancelButtonClass: 'btn-primary',
        draggable: true,
        dragWindowBorder: false,
        buttons: {
            info: {
                text: "Si",
                btnClass: 'btn-primary',
                action: function () {
                    callback();
                }
            },
            danger: {
                text: "No",
                btnClass: 'btn-red',
                action: function () {
                    // cancel();

                }
            },
        }
    })
}
function alerta_action2(title, content, callback, cancel) {
    $.confirm({
        theme: 'material',
        title: title,
        icon: '',
        content: content,
        columnClass: 'small',
        typeAnimated: true,
        cancelButtonClass: 'btn-primary',
        draggable: true,
        dragWindowBorder: false,
        buttons: {
            info: {
                text: "Si",
                btnClass: 'btn-primary',
                action: function () {
                    callback();
                }
            },
            danger: {
                text: "No",
                btnClass: 'btn-red',
                action: function () {
                    cancel();

                }
            },
        }
    })
}



function Deletes(id, url) {
    Swal.fire({
        title: "Esta seguro de borrar?",
        text: "Este contenido no se puede recuperar!",
        // type: "warning",
        showCancelButton: true,
        confirmButtonColor: "#DD6B55",
        confirmButtonText: "Si, borrar!",
        cancelButtonText: "Cancelar"
        // preConfirm: true
    }).then((result) => {
        if (result.value) {
            $.ajax({
                type: 'POST',
                // url: window.location.pathname,
                // url: '/cliente/cliente/eliminar/',
                url: url,
                data: {'id': id, 'action': 'eliminar'},
                success: function (data) {
                    // console.log(data);
                    if (data.hasOwnProperty('success')) {
                        Swal.fire(
                            'Borrado!',
                            'Tu registro fue borrado con éxito.',
                            'success'
                        )

                    } else {

                        Swal.fire(
                            'Error!',
                            'No tiene permiso para ingresar a este módulo',
                            'error'
                        )
                    }


                    tbl.ajax.reload();
                    // if (data.success) {
                    //     toastr.success(data.message);
                    //     dataTable.ajax.reload();
                    // } else {
                    //     toastr.error(data.message);
                    // }
                }
            });


            // For more information about handling dismissals please visit
            // https://sweetalert2.github.io/#handling-dismissals
        }

    });

}
