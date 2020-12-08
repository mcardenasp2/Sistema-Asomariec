$(document).ready(function () {
    $('#id_cliente').css('width', '50%');
});


var ct = 0;
var tblGast;
var tblProducto;
var produ = {
    items: {
        cliente: '',
        fecha: '',
        // precio: 0.00,
        tgsto: 0.00,
        subproductos: 0.00,
        impuestos: 0.00,
        productos: [],
        gastoad: [],
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
    add2: function (item) {
        //gastos adicionales
        this.items.gastoad.push(item);
        this.list2();

    },
    calculate_invoice: function () {
        var subtotal = 0.00;
        var impuesto = 0.00;
        $.each(this.items.productos, function (pos, dict) {
            // console.log(pos);
            // console.log(dict);
            dict.subtotal = dict.cant * parseFloat(dict.prodPrecio);
            impuesto += dict.subtotal * dict.prodIva;
            subtotal += dict.subtotal;
        });
        this.items.subproductos = subtotal;
        this.items.impuestos = impuesto;
        // console.log(this.items.subproductos);
        // console.log(impuesto);

        $('input[name="subtotal"]').val(this.items.subproductos.toFixed(2));
        $('input[name="iva"]').val(this.items.impuestos.toFixed(2));
        this.tpago();

    },
    calculate_invoice2: function () {
        var subtotal = 0.00;
        $.each(this.items.gastoad, function (pos, dict) {
            // console.log(pos);
            // console.log(dict);
            // dict.subtotal = dict.cant * parseFloat(dict.prodPrecio);
            subtotal += parseFloat(dict.gastPrecio);
        });
        // console.log(subtotal);
        this.items.tgsto = subtotal;
        console.log(this.items.tgsto);

        $('input[name="gastoadicionales"]').val(this.items.tgsto.toFixed(2));
        this.tpago();

    },
    tpago: function () {
        var ga = 0.00;
        var st = 0.00;
        var t = 0.00;
        var im = 0.00;
        ga = parseFloat($('input[name="gastoadicionales"]').val());
        st = parseFloat($('input[name="subtotal"]').val());
        im = parseFloat($('input[name="iva"]').val());
        t = ga + st + im;
        $('input[name="topagar"]').val(t.toFixed(2));

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
                // var ty = data.cant-1+data.prodCantidad;
                // var ty = parseInt(data.prodCantidad)+parseInt(row.cant);
                var pp = 15;
                if ($('input[name="action"]').val() == 'add') {
                    var ty = data.prodCantidad;
                } else {
                    var ty = data.cant + data.prodCantidad - ct;
                }


                $(row).find('input[name="cant"]').TouchSpin({
                    min: 1,
                    // max: parseInt(pp),
                    // max: 10,
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
        this.calculate_invoice2();
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
                        // var p=parseFloat(data).toFixed(2);
                        return '$' + parseFloat(data).toFixed(2);
                        // return '<input type="text" name="cant" class="form-control form-control-sm input-sm" autocomplete="off" value="$' + data+ '">';
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
    // evento calendarip
    $('#venFechaFin').datetimepicker({
        icons: {
            time: "fa fa-clock",
            date: "fa fa-calendar-day",
            up: "fa fa-chevron-up",
            down: "fa fa-chevron-down",
            previous: 'fa fa-chevron-left',
            next: 'fa fa-chevron-right',
            today: 'fa fa-screenshot',
            clear: 'fa fa-trash',
            close: 'fa fa-remove'
        },
        format: 'YYYY-MM-DD',
        // date: moment().format("YYYY-MM-DD"),
        locale: 'es',
        //minDate: moment().format("YYYY-MM-DD")
    });


    //gastos
    $('.btnGastos').on('click', function () {
        $('#myModelDet').modal('show');

    });

    $('input[name="preciogasto"]').TouchSpin({
        min: 1,
        max: 100,
        step: 0.1,
        decimals: 2,
        verticalbuttons: true,
        verticalupclass: 'glyphicon glyphicon-plus',
        verticaldownclass: 'glyphicon glyphicon-minus'

    });

    //anadir gasto
    $('.addgast').on('click', function () {
        // alert('xxx');
        var gast = {};
        gast.gastDescripcion = $('input[name="descripcion"]').val();
        gast.gastPrecio = $('input[name="preciogasto"]').val();
        if (gast.gastDescripcion === '' || gast.gastPrecio === '') return false;

        produ.add2(gast);
        $('input[name="descripcion"]').val('');
        $('input[name="preciogasto"]').val('1.00');

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
//eliminar todos los productos
    $('.btnRemoveAll').on('click', function () {
        //si no hay productos retorno falso
        if (produ.items.productos.length === 0) return false;
        alerta_action('Notificacion', 'Estas seguro de Eliminar todos los items de tu detalle?', function () {
            produ.items.productos = [];
            produ.list();
        });


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

            // data.cant = 0;

            data.cant = 1;
            ct = data.cant;
            data.subtotal = 0.00;
            console.log(data);
            // console.log(data.insStock);
            //
            //
            produ.add(data);
            $(this).val('').trigger('change.select2');
        });

    //Buscar cliente
    $('select[name="cliente"]').select2({
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
                    action: 'search_clients'
                }
                return queryParameters;
            },
            processResults: function (data) {
                return {
                    results: data
                };
            },
        },
        placeholder: 'Ingrese una descripción',
        minimumInputLength: 1,
    });

    $('.btnAddClient').on('click', function () {
        $('#MyModalClient').modal('show');

    });

    $('#MyModalClient').on('hidden.bs.modal', function (e) {
        $('#formClient').trigger('reset');
    })


    //evento guardar cliente
    $('#formClient').on('submit', function (e) {
        e.preventDefault();
        var parameters = new FormData(this);
        parameters.append('action', 'create_client');
        parameters.forEach(function (value, key) {
            console.log(key + ':' + value);

        });

        submit_with_ajax(window.location.pathname, 'Notification', '¿Estas seguro de crear el siguiente cliente', parameters, function (response) {
            console.log(response);
            var newOption = new Option(response.full_name, response.id, false, true);
            $('select[name="cliente"]').append(newOption).trigger('change');
            $('#MyModalClient').modal('hide');


        });

    });

    //evento guardar venta
    $('#frmVentaNormal').on('submit', function (e) {
        e.preventDefault();
        if (produ.items.productos.length === 0) {
            message_error('Debe al menos tener un item en su detalle de compra');
            return false;
        }
        produ.items.fecha = $('input[name="venFechaFin"]').val();
        produ.items.cliente = $('select[name="cliente"]').val();
        console.log(produ.items);
        var parameters = new FormData();
        parameters.append('action', $('input[name="action"]').val());
        parameters.append('ventas', JSON.stringify(produ.items));
        parameters.forEach(function (value, key) {
            console.log(key + ':' + value);

        });

        submit_with_ajax(window.location.pathname, 'Notification', '¿Estas seguro de realizar la siguiente acción?', parameters, function (response) {
            alerta_action2('Notificacion', '¿Desea imprimir la Boleta de Venta?', function () {
                // print('fff');
                // print(response);
                window.open('/venta/normal/invoice/pdf/' + response.id + '/', '_blank')
                location.href = '/venta/normal/mostrar/';
            }, function () {
                location.href = '/venta/normal/mostrar/';

            });


        });

    });

    produ.list();
    produ.list2();


});