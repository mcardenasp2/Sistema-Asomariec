var tblVenta;


$(function () {

    // $('.select2-selection--multiple').select2();


    tblVenta = $('#table_id').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        paging: true,
        // order:[[ 2, "desc" ]],
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
            {"data": "cliente.full_name"},
            {"data": "venFechaFin"},
            // {"data": "categoria.catDescripcion"},
            {"data": "venEstVenta"},
            {"data": "ventSubtotal"},
            {"data": "ventImpuesto"},

            {"data": "ventTotal"},
            {"data": "ventTotal"},

        ],
        columnDefs: [
            {
                targets:[1,2],
                class: 'text-center',
            },
            {
                targets: [3],
                class: 'text-center',
                orderable: true,
                render: function (data, type, row) {
                    if (data==2){
                         var buttons = '<span class="badge badge-success">PAGADO</span>';
                    }else {
                         var buttons = '<span class="badge badge-danger">PENDIENTE</span>';
                    }

                    // buttons += '<a href="/venta/contrato/editar/' + row.id + '/" class="btn btn-warning btn-sm btn-flat"><i class="fas fa-edit"></i></a> ';
                    // buttons += '<a rel="details" class="btn btn-success btn-sm btn-flat"><i class="fas fa-search"></i></a> ';
                    // buttons += '<a href="/venta/contrato/invoice/pdf/'+row.id+'" target="_blank" class="btn btn-info btn-sm btn-flat"><i class="fas fa-file-pdf"></i></a> ';

                    //var buttons = '<a href="/erp/sale/update/' + row.id + '/" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
                    return buttons;
                }
            },

            {
                targets: [-3, -4, -5],
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
                    var buttons = '<a title="Eliminar" href="/venta/contrato/eliminar/' + row.id + '/" class="btn btn-danger btn-sm btn-flat"><i class="fas fa-trash-alt"></i></a> ';
                    // buttons += '<a href="/venta/contrato/editar/' + row.id + '/" class="btn btn-warning btn-sm btn-flat"><i class="fas fa-edit"></i></a> ';
                    buttons += '<a title="Ver" href="/venta/contrato/detalle/' + row.id + '/" class="btn btn-warning btn-sm btn-flat"><i class="fas fa-edit"></i></a> ';
                    // buttons += '<a rel="details" class="btn btn-success btn-sm btn-flat"><i class="fas fa-search"></i></a> ';
                    buttons += '<a title="Imprimir" href="/venta/contrato/invoice/pdf/'+row.id+'" target="_blank" class="btn btn-info btn-sm btn-flat"><i class="fas fa-file-pdf"></i></a> ';

                    //var buttons = '<a href="/erp/sale/update/' + row.id + '/" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
                    return buttons;
                }
            },
        ],
        initComplete: function (settings, json) {
            // this.api().columns().every()
            // this.api().columns().every( function () {
            // // this.columns().every( function () {
            //     var column = this;
            //     var select = $('<select><option value=""></option></select>')
            //         .appendTo( $(column.footer()).empty() )
            //         .on( 'change', function () {
            //             var val = $.fn.dataTable.util.escapeRegex(
            //                 $(this).val()
            //             );
            //
            //             column
            //                 .search( val ? '^'+val+'$' : '', true, false )
            //                 .draw();
            //         } );
            //
            //     column.data().unique().sort().each( function ( d, j ) {
            //         select.append( '<option value="'+d+'">'+d+'</option>' )
            //     } );
            // } );
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
                    {"data": "producto.id"},
                    {"data": "producto.prodDescripcion"},
                    {"data": "producto.prodEstprod"},
                    {"data": "producto.prodPrecio"},
                    {"data": "detCant"},
                    {"data": "detSubtotal"},
                ],
                columnDefs: [
                    {
                        targets: [0],
                        class: 'text-center',
                        orderable: false,
                        render: function (data, type, row) {
                            var buttons = '<a href="/producto/producto/editar/' + data + '/" class="btn btn-warning btn-sm btn-flat" target="_blank"><i class="fas fa-edit"></i></a> ';
                            // buttons += '<a href="/venta/contrato/editar/' + row.id + '/" class="btn btn-warning btn-sm btn-flat"><i class="fas fa-edit"></i></a> ';
                            // buttons += '<a rel="details" class="btn btn-success btn-sm btn-flat"><i class="fas fa-search"></i></a> ';
                            //var buttons = '<a href="/erp/sale/update/' + row.id + '/" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
                            return buttons;
                        }
                    },
                    {
                        targets: [2],
                        class: 'text-center',
                        orderable: false,
                        render: function (data, type, row) {

                            if (data == 1) {
                                var buttons = '<span class="badge badge-success">Success</span>';
                            } else if (data == 0) {
                                var buttons = '<span class="badge badge-danger">Danger</span>';

                            }

                            // var buttons ='<a href="/producto/producto/editar/' + data+ '/" class="btn btn-warning btn-sm btn-flat" target="_blank"><i class="fas fa-edit"></i></a> ';
                            // buttons += '<a href="/venta/contrato/editar/' + row.id + '/" class="btn btn-warning btn-sm btn-flat"><i class="fas fa-edit"></i></a> ';
                            // buttons += '<a rel="details" class="btn btn-success btn-sm btn-flat"><i class="fas fa-search"></i></a> ';
                            //var buttons = '<a href="/erp/sale/update/' + row.id + '/" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
                            return buttons;
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