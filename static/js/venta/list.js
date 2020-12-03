var tblVenta;


$(function () {

    // $('.select2-selection--multiple').select2();


    tblVenta = $('#table_id').DataTable({
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
            {"data": "cliente.cliNombre"},
            {"data": "venFechaInici"},
            // {"data": "categoria.catDescripcion"},
            {"data": "ventSubtotal"},
            {"data": "ventImpuesto"},

            {"data": "ventTotal"},
            {"data": "ventTotal"},

        ],
        columnDefs: [

            {
                targets: [-2, -3, -4],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    return '$' + parseFloat(data).toFixed(2);
                }
            },
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<a href="/venta/normal/delete/' + row.id + '/" class="btn btn-danger btn-sm btn-flat"><i class="fas fa-trash-alt"></i></a> ';
                    buttons += '<a href="/venta/normal/editar/' + row.id + '/" class="btn btn-warning btn-sm btn-flat"><i class="fas fa-edit"></i></a> ';
                    buttons += '<a rel="details" class="btn btn-success btn-sm btn-flat"><i class="fas fa-search"></i></a> ';
                    buttons += '<a href="/venta/normal/invoice/pdf/' + row.id + '" target="_blank" class="btn btn-info btn-sm btn-flat"><i class="fas fa-file-pdf"></i></a> ';

                    //var buttons = '<a href="/erp/sale/update/' + row.id + '/" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
                    return buttons;
                }
            },
        ],
        initComplete: function (settings, json) {

        }
    });


    $('#table_id tbody')
        .on('click', 'a[rel="details"]', function () {
            // alert('x');
            // console.log('hola');
            var tr = tblVenta.cell($(this).closest('td, li')).index();
            var data = tblVenta.row(tr.row).data();
            console.log(data);

            $('#tblDet').DataTable({
                responsive: true,
                autoWidth: false,
                destroy: true,
                deferRender: true,
                // data: data.det,
                // {#Bolo#}
                ordering: true,
                info: true,
                pageLength: 5,
                searching: true,
                responsive: false,

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
                        'action': 'search_details_ins',
                        'id': data.id
                    },
                    dataSrc: ""
                },
                columns: [
                    {"data": "producto.prodDescripcion"},
                    {"data": "producto.prodImagen"},
                    {"data": "producto.prodPrecio"},
                    {"data": "detCant"},
                    {"data": "detSubtotal"},
                ],
                columnDefs: [
                    {
                        targets: [1],
                        class: 'text-center',
                        orderable: false,
                        render: function (data, type, row) {
                            // return '<img src="' + data + '" class="avatar avatar-sm rounded-circle">';
                            var imagen = '<div class="avatar-group">';
                            imagen += '<a href="#" class="avatar avatar-sm rounded-circle" data-toggle="tooltip" data-original-title="Ryan Tompson">';
                            imagen += '<img alt="Image placeholder" src="' + data + '"></a>';
                            imagen += '<a href="#" class="avatar avatar-sm rounded-circle" data-toggle="tooltip" data-original-title="Romina Hadid">';
                            imagen += '<img alt="Image placeholder" src="' + row.producto.prodImagen2 + '"></a></div>';
                            return imagen;

                        }
                    },
                    {
                        targets: [-1, -3],
                        class: 'text-center',
                        render: function (data, type, row) {
                            return '$' + parseFloat(data).toFixed(2);
                        }
                    },
                    {
                        targets: [-2],
                        class: 'text-center',
                        render: function (data, type, row) {
                            return data;
                        }
                    },
                ],
                initComplete: function (settings, json) {

                }
            });

            $('#myModelDet').modal('show');
        });


});