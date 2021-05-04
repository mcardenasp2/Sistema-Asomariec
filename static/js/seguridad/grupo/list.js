$(function () {
    tbl=$('#data').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
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
            {"data": "name"},
            // {"data": "icono"},
            // {"data": "descripcion"},
            // {"data": "modulos"},
            // {"data": "permissions"},
            {"data": "id"},
        ],
        columnDefs: [
            // {
            //     targets: [-3],
            //     class: 'text-center',
            //     orderable: false,
            //     render: function (data, type, row) {
            //         var html = '';
            //         $.each(row.modulos, function (key, value) {
            //             html += '<span class="badge badge-success">' + value.nombre + '</span> ';
            //         });
            //         return html;
            //     }
            // },
            // {
            //     targets: [-2],
            //     class: 'text-center',
            //     orderable: false,
            //     render: function (data, type, row) {
            //         var html = '';
            //         $.each(row.permissions, function (key, value) {
            //             html += '<span class="badge badge-success">' + value.nombre + '</span> ';
            //         });
            //         return html;
            //     }
            // },
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<a title="Editar" href="/seguridad/grupo/editar/' + row.id + '/" class="btn btn-warning btn-sm btn-flat"><i class="fas fa-edit"></i></a> ';
                    // buttons += '<a title="Eliminar" href="/user/delete/' + row.id + '/" type="button" class="btn btn-danger btn-sm btn-flat"><i class="fas fa-trash-alt"></i></a>';
                    buttons += '<a title="Eliminar" href="#" onclick=Delete("' + row.id + '") type="button" class="btn btn-danger btn-sm btn-flat"><i class="fas fa-trash-alt"></i></a>';
                    return buttons;
                }
            },
        ],
        initComplete: function (settings, json) {

        }
    });
});


function Delete(id) {
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
                // url: window.location.pathname,
                url: '/seguridad/grupo/eliminar/',
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
    });
}
