var tblGast;
var tblProducto;
var produ = {
    items: {
        cliente: '',
        precio: 0.00,
        productos: [],
        gastoad:[],
    },
    add: function (item) {
        var band;
        band = 1;
        $.each(this.items.productos, function (pos, dict) {
            if (parseInt(dict.id) == parseInt(item.id)) {
                band = 0;
                return false;

            }

        });
        if (band == 1) {
            this.items.productos.push(item);
            this.list();
        }


    },
    add2: function(item){
        //gastos adicionales
        this.items.gastoad.push(item);
        this.list2();

    },
    addcont: function(item){
        //contrato
        this.items.productos.push(item);
        this.listc();
        this.list();

    },
    calculate_invoice: function () {
        var subtotal = 0.00;
        $.each(this.items.productos, function (pos, dict) {
            // console.log(pos);
            // console.log(dict);
            dict.subtotal = dict.cant * parseFloat(dict.prodPrecio);
            subtotal += dict.subtotal;
        });

    },
    calculate_invoice2: function () {
        var subtotal = 0.00;
        $.each(this.items.productos, function (pos, dict) {
            // console.log(pos);
            // console.log(dict);
            dict.subtotal = dict.cant * parseFloat(dict.prodPrecio);
            subtotal += dict.subtotal;
        });

    },
    list: function () {
        this.calculate_invoice();


        tblProducto = $('#tblProducto').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            data: this.items.productos,
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
            columns: [
                {"data": "id"},
                {"data": "prodDescripcion"},
                {"data": "prodPrecio"},
                // {"data": "pvp"},
                {"data": "cant"},
                {"data": "subtotal"},
            ],
            columnDefs: [
                {
                    targets: [0],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<a rel="remove" class="btn btn-danger btn-sm btn-flat" style="color: white"><i class="fas fa-trash-alt"></i></a>';
                    }
                },
                {
                    targets: [-3],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '$' + parseFloat(data).toFixed(2);
                    }
                },
                {
                    targets: [-2],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<input type="text" name="cant" class="form-control form-control-sm input-sm" autocomplete="off" value="' + row.cant + '">';
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '$' + parseFloat(data).toFixed(2);
                    }
                },
            ],
            rowCallback(row, data, displayNum, displayIndex, dataIndex) {
                var ty = data.prodCantidad;
                var pp = 15;


                $(row).find('input[name="cant"]').TouchSpin({
                    min: 1,
                    // max: parseInt(pp),
                    max: parseInt(ty),
                    step: 1,
                    // boostat: 5,
                });

            },
            initComplete: function (settings, json) {

            }
        });

    },
    listc: function () {
        // this.calculate_invoice();


        tblProducto = $('#tblProductocont').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            data: this.items.productos,
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
            columns: [
                {"data": "id"},
                {"data": "prodDescripcion"},
                {"data": "prodPrecio"},
                // {"data": "pvp"},
                {"data": "cant"},
                {"data": "subtotal"},
            ],
            columnDefs: [
                {
                    targets: [0],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<a rel="remove" class="btn btn-danger btn-sm btn-flat" style="color: white"><i class="fas fa-trash-alt"></i></a>';
                    }
                },
                {
                    targets: [-3],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '$' + parseFloat(data).toFixed(2);
                    }
                },
                {
                    targets: [-2],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<input type="text" name="cant" class="form-control form-control-sm input-sm" autocomplete="off" value="' + row.cant + '">';
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '$' + parseFloat(data).toFixed(2);
                    }
                },
            ],
            rowCallback(row, data, displayNum, displayIndex, dataIndex) {
                var ty = data.prodCantidad;
                var pp = 15;


                $(row).find('input[name="cant"]').TouchSpin({
                    min: 1,
                    // max: parseInt(pp),
                    max: parseInt(ty),
                    step: 1,
                    // boostat: 5,
                });

            },
            initComplete: function (settings, json) {

            }
        });

    },
    list2: function () {
        tblGast = $('#tblDet').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            data: this.items.gastoad,
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
            columns: [
                // {"data": "id"},
                {"data": "gastDescripcion"},
                {"data": "gastDescripcion"},
                {"data": "gastPrecio"},
                // {"data": "pvp"},
                // {"data": "cant"},
                // {"data": "subtotal"},
            ],
            columnDefs: [
                {
                    targets: [0],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<a rel="remove" class="btn btn-danger btn-sm btn-flat" style="color: white"><i class="fas fa-trash-alt"></i></a>';
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '$' + parseFloat(data).toFixed(2);
                    }
                },
            ],

            initComplete: function (settings, json) {

            }
        });

    }

};

function formatRepo(repo) {
    if (repo.loading) {
        return repo.text;
    }

    var option = $(
        '<div class="wrapper container">' +
        '<div class="row">' +
        '<div class="col-lg-1">' +
        '<img src="' + repo.prodImagen + '" class="img-fluid img-thumbnail d-block mx-auto rounded">' +
        '</div>' +
        '<div class="col-lg-11 text-left shadow-sm">' +
        //'<br>' +
        '<p style="margin-bottom: 0;">' +
        '<b>Nombre:</b> ' + repo.prodDescripcion + '<br>' +
        '<b>Stock:</b> ' + repo.prodCantidad + '<br>' +
        '<b>PVP:</b> <span class="badge badge-warning">$' + repo.prodPrecio + '</span>' +
        '</p>' +
        '</div>' +
        '</div>' +
        '</div>');

    return option;
}

$(function () {
    //contrato
     $('.addcontr').on('click', function (e) {
        // alert('xxx');
         e.preventDefault();
        var gast={};

        gast.prodDescripcion = $('input[name="descripcionc"]').val();
        gast.prodPrecio = $('input[name="precioc"]').val();
        gast.id=1;
        gast.cant=1;
        gast.subtotal=0.00;
        if (gast.prodDescripcion === '' || gast.prodPrecio === '') return false;

        produ.addcont(gast);
        $('input[name="descripcionc"]').val('');
        $('input[name="precioc"]').val('');

    });

    //gastos
    $('.btnGastos').on('click', function () {
        $('#myModelDet').modal('show');

    });

    //anadir gasto
    $('.addgast').on('click', function () {
        // alert('xxx');
        var gast={};
        gast.gastDescripcion = $('input[name="descripcion"]').val();
        gast.gastPrecio = $('input[name="precio"]').val();
        if (gast.gastDescripcion === '' || gast.gastPrecio === '') return false;

        produ.add2(gast);
        $('input[name="descripcion"]').val('');
        $('input[name="precio"]').val('');

    });
    //eliminar gasto
    $('#tblDet tbody')
        .on('click', 'a[rel="remove"]', function () {
            var tr = tblGast.cell($(this).closest('td, li')).index();
            alerta_action('Notificacion', 'Estas seguro de Eliminar el insumo de tu detalle?', function () {
                produ.items.gastoad.splice(tr.row, 1);
                //    actualizams
                produ.list2();
            });

        });




    //eliminar un producto
    $('#tblProducto tbody')
        .on('click', 'a[rel="remove"]', function () {
            var tr = tblProducto.cell($(this).closest('td, li')).index();
            alerta_action('Notificacion', 'Estas seguro de Eliminar el insumo de tu detalle?', function () {
                produ.items.productos.splice(tr.row, 1);
                //    actualizams
                produ.list();
            });

        })
        .on('change', 'input[name="cant"]', function () {
            // console.clear();
            var cant = parseInt($(this).val());
            // console.log(cant)
            var tr = tblProducto.cell($(this).closest('td, li')).index();
            // console.log(tr);
            produ.items.productos[tr.row].cant = cant;
            produ.calculate_invoice();
            $('td:eq(4)', tblProducto.row(tr.row).node()).html('$' + produ.items.productos[tr.row].subtotal.toFixed(2));
        });

//    Buscar producto
    $('select[name="search"]').select2({
        theme: "bootstrap4",
        language: 'es',
        allowClear: true,
        ajax: {
            delay: 250,
            type: 'POST',
            url: window.location.pathname,
            data: function (params) {
                var queryParameters = {
                    term: params.term,
                    action: 'search_productos'
                };
                return queryParameters;
            },
            processResults: function (data) {
                return {
                    results: data
                };
            },
        },
        placeholder: 'Ingrese una descripcion',
        minimumInputLength: 1,
        templateResult: formatRepo,
    })
        .on('select2:select', function (e) {
            // alert('c');
            var data = e.params.data;
            // console.log(data);
            // data.stock=10;
            // data.insStock

            data.cant = 1;
            data.subtotal = 0.00;
            console.log(data);
            // console.log(data.insStock);
            //
            //
            produ.add(data);
            $(this).val('').trigger('change.select2');
        });

    produ.list();
    produ.list2();
    produ.listc();

});