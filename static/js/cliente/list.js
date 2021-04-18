$(function () {
    tbl=$('#table_id').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        paging: true,
        // {#Bolo#}
        ordering: true,
        info: true,
        pageLength: 5,
        searching: true,
        responsive: false,
        // {#lenguaje#}
        language: {
            processing: 'Procesando...',
            // search: 'Buscar:',
            search: "Buscar: _INPUT_",
            // searchPlaceholder: "Buscar Registros",
            lengthMenu: '   Mostrar _MENU_ registros',
            info: 'Mostrando desde _START_ al _END_ de _TOTAL_ registros',
            infoEmpty: 'Mostrando ningún elemento.',
            infoFiltered: '(filtrado _MAX_ elementos total)',
            infoPostFix: '',
            loadingRecords: 'Cargando registros...',
            zeroRecords: 'No se encontraron registros',
            emptyTable: 'No hay datos disponibles en la tabla',
            paginate: {
                first: 'Primero',
                previous: '<-',
                next: '->',
                last: 'Último'
            }
        },
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: {
                'action': 'searchdata'
            },
            dataSrc: ""
        },
        columns: [
            {"data": "id"},
            {"data": "cliNombre"},
            {"data": "cliApellido"},
            {"data": "cliRuc"},
            {"data": "cliTelefono"},
            {"data": "id"},
            // {"data": "desc"},
        ],
        columnDefs: [
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<a title="Editar" href="/cliente/cliente/editar/' + row.id + '/" class="btn btn-warning btn-sm btn-flat"><i class="fas fa-edit"></i></a> ';
                    // buttons += '<a onclick=Delete(row.id)  title="Eliminar" href="/cliente/cliente/eliminar/' + row.id + '/" type="button" class="btn btn-danger btn-sm btn-flat"><i class="fas fa-trash-alt"></i></a>';
                    buttons += '<a href="#" onclick=Delete("' + row.id + '")  title="Eliminar"  type="button" class="btn btn-danger btn-sm btn-flat"><i class="fas fa-trash-alt"></i></a>';
                    return buttons;
                }
            },
        ],
        initComplete: function (settings, json) {

        }
    });


});


function Delete(id) {
    // console.log(id);
    // var parameters = new FormData();
    // parameters.append('action', 'eliminar');
    // parameters.append('id', url);

    // console.log(window.location.pathname);
    Swal.fire({
        title: "Esta seguro de borrar?",
        text: "Este contenido no se puede recuperar!",
        // type: "warning",
        showCancelButton: true,
        confirmButtonColor: "#DD6B55",
        confirmButtonText: "Si, borrar!",
        cancelButtonText:"Cancelar"
        // preConfirm: true
    }).then((result) => {
        if (result.value) {
            $.ajax({
                type: 'POST',
                url: window.location.pathname,
                data: {'id': id, 'action': 'eliminar'},
                success: function (data) {
                    Swal.fire(
                        'Borrado!',
                        'Tu registro fue borrado con éxito.',
                        'success'
                    )
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
        // else if (result.dismiss === Swal.DismissReason.cancel) {
        //     Swal.fire(
        //         'Cancelled',
        //         'Your imaginary file is safe :)',
        //         'error'
        //     )
        // }

        // , function () {
        //     $.ajax({
        //         url: window.location.pathname,
        //         type: 'POST',
        //         data: parameters,
        //
        //         dataType: 'json',
        //         processData: false,
        //         contentType: false,
        //         success: function (data) {
        //             if (data.success) {
        //                 toastr.success(data.message);
        //                 dataTable.ajax.reload();
        //             } else {
        //                 toastr.error(data.message);
        //             }
        //         }
        //     });
    });

    //
    // swal({
    //     title: "Esta seguro de borrar?",
    //     text: "Este contenido no se puede recuperar!",
    //     type: "warning",
    //     showCancelButton: true,
    //     confirmButtonColor: "#DD6B55",
    //     confirmButtonText: "Si, borrar!",
    //     closeOnconfirm: true
    // }, function () {
    //     $.ajax({
    //         // type: 'DELETE',
    //         type: 'POST',
    //         data: {'id': 1, 'action': 'eliminar'},
    //         // url: url,
    //         url: window.location.pathname,
    //         success: function (data) {
    //             if (data.success) {
    //                 toastr.success(data.message);
    //                 dataTable.ajax.reload();
    //             } else {
    //                 toastr.error(data.message);
    //             }
    //         }
    //     });
    // });
}
