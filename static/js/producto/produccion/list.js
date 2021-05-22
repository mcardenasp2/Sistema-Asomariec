var tblProduccion;

$(function () {

    tblProduccion = $('#table_id').DataTable({
        // responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        paging: true,
        order:[[ 2, "desc" ]],
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
            {"data": "producto.prodDescripcion"},
            {"data": "prodcFecElab"},
            {"data": "prodcCantidad"},
            // {"data": "prodImagen"},
            {"data": "prodcTotal"},
            {"data": "id"},

        ],
        columnDefs: [
            {
                targets: [1, 3],
                class: 'text-center',
            },
            {
                targets: [3],
                class: 'text-center',
                render: function (data, type, row) {
                    var dato;
                    if (data > 9) {
                        dato = '<spam disabled class="badge badge-pill badge-lg bg-success text-white">' + data + '</spam>';
                    } else if (data > 0) {
                        dato = '<spam disabled class="badge badge-pill badge-lg bg-yellow text-dark">' + data + '</spam>';
                    } else {
                        dato = '<spam disabled class="badge badge-pill badge-lg bg-danger text-white">' + data + '</spam>';
                    }
                    // var dato='<a class="badge badge-lg badge-pill badge-danger">'+data+'</a>';


                    return dato;

                }
            },
            {
                targets: [-3],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    // return '<img src="' + data + '" class="avatar avatar-sm rounded-circle">';
                    var imagen = '<div class="avatar-group">';
                    imagen += '<a href="#" class="avatar avatar-sm rounded-circle" data-toggle="tooltip" >';
                    imagen += '<img alt="Image placeholder" src="' + data + '"></a>';
                    imagen += '<a href="#" class="avatar avatar-sm rounded-circle" data-toggle="tooltip" >';
                    imagen += '<img alt="Image placeholder" src="' + row.prodImagen2 + '"></a></div>';
                    return imagen;

                }
            },
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<a title="Visualizar" rel="details" class="btn btn-success btn-sm btn-flat"><i class="fas fa-search"></i></a> ';
                    // buttons += '<a href="/producto/produccion/eliminar/' + row.id + '/" type="button" class="btn btn-danger btn-sm btn-flat"><i class="fas fa-trash-alt"></i></a>';
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
            var tr = tblProduccion.cell($(this).closest('td, li')).index();
            var data = tblProduccion.row(tr.row).data();
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
                    {"data": "insumo.insDescripcion"},
                    {"data": "insumo.insImagen"},
                    {"data": "detprecio"},
                    // {"data": "insIva"},
                    {"data": "detCantidad"},
                    {"data": "detSubtotal"},
                ],
                columnDefs: [

                    {
                        targets: [1],
                        class: 'text-center',
                        orderable: false,
                        render: function (data, type, row) {
                            // return '<img src="' + data + '" class="avatar avatar-sm rounded-circle">';
                            return '<img src="' + data + '" class="avatar avatar-sm rounded-circle">';
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