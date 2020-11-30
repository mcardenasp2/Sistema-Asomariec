$(function () {

    // $('.select2-selection--multiple').select2();


    $('#table_id').DataTable({
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
            {"data": "prodDescripcion"},
            {"data": "prodFecElab"},
            {"data": "prodCantidad"},
            {"data": "prodImagen"},
            {"data": "prodPrecioTotal"},
            {"data": "id"},

        ],
        columnDefs: [
            {
                targets: [-3],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    // return '<img src="' + data + '" class="avatar avatar-sm rounded-circle">';
                    var imagen = '<div class="avatar-group">';
                    imagen += '<a href="#" class="avatar avatar-sm rounded-circle" data-toggle="tooltip" data-original-title="Ryan Tompson">';
                    imagen += '<img alt="Image placeholder" src="' + data + '"></a>';
                    imagen += '<a href="#" class="avatar avatar-sm rounded-circle" data-toggle="tooltip" data-original-title="Romina Hadid">';
                    imagen += '<img alt="Image placeholder" src="' + row.prodImagen2 + '"></a></div>';
                    return imagen;

                }
            },
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<a href="/producto/producto/editar/' + row.id + '/" class="btn btn-warning btn-sm btn-flat"><i class="fas fa-edit"></i></a> ';
                    buttons += '<a href="/producto/producto/eliminar/' + row.id + '/" type="button" class="btn btn-danger btn-sm btn-flat"><i class="fas fa-trash-alt"></i></a>';
                    return buttons;
                }
            },
        ],
        initComplete: function (settings, json) {

        }
    });
});