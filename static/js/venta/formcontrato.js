var tblGast;
var tblProducto;
var produ = {
    items: {
        cliente: '',
        fecha: '',
        fechafin: '',
        // precio: 0.00,
        tgsto: 0.00,
        subproductos: 0.00,
        productos: [],
        gastoad: [],
    },
    add: function (item) {
        // var band;
        // band = 1;
        // $.each(this.items.productos, function (pos, dict) {
        //     if (parseInt(dict.id) == parseInt(item.id)) {
        //         band = 0;
        //         return false;
        //
        //     }
        //
        // });
        // if (band == 1) {
        this.items.productos.push(item);
        this.list();
        // }


    },
    add2: function (item) {
        //gastos adicionales
        this.items.gastoad.push(item);
        this.list2();

    },
    calculate_invoice: function () {
        var subtotal = 0.00;
        $.each(this.items.productos, function (pos, dict) {
            // console.log(pos);
            // console.log(dict);
            dict.subtotal = dict.cant * parseFloat(dict.prodPrecio);
            subtotal += dict.subtotal;
        });
        this.items.subproductos = subtotal;
        console.log(this.items.subproductos);

        $('input[name="subtotal"]').val(this.items.subproductos.toFixed(2));
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
        ga = parseFloat($('input[name="gastoadicionales"]').val());
        st = parseFloat($('input[name="subtotal"]').val());
        t = ga + st;
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
                        return '<div class="input-group input-group-sm"><input type="text" name="prodPrecio" class="form-control form-control-sm input-sm" autocomplete="off" value="' + row.prodPrecio + '"></div>';
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
                // var ty = data.prodCantidad;
                // var pp = 15;


                $(row).find('input[name="cant"]').TouchSpin({
                    min: 1,
                    // max: parseInt(pp),
                    max: 1000,
                    step: 1,
                    // prefix: '$',
                    // boostat: 5,
                });

                // $(row).find('input[name="prodPrecio"]').TouchSpin({
                    // prefix: 'd',
                    // postfix_extraclass: "btn btn-default"
                // });

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


$(function () {
    // evento calendarip
    $('#venFechaInici').datetimepicker({
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
        date: moment().format("YYYY-MM-DD"),
        locale: 'es',
        //minDate: moment().format("YYYY-MM-DD")
    });
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
        date: moment().format("YYYY-MM-DD"),
        locale: 'es',
        // minDate: $('#venFechaInici').val(),
        //minDate: moment().format("YYYY-MM-DD")
    });


    //anadir producto contrato
    $('.addcontr').on('click', function (e) {
        // alert('xxx');
        e.preventDefault();
        var gast = {};
        //
        gast.prodDescripcion = $('input[name="descripcionc"]').val();
        gast.prodPrecio = $('input[name="precioc"]').val();
        gast.id = 0;
        gast.cant = 1;
        gast.subtotal = 0.00;
        if (gast.prodDescripcion === '' || gast.prodPrecio === '') return false;
        //
        produ.add(gast);

        $('input[name="descripcionc"]').val('');
        $('input[name="precioc"]').val('1.00');
        produ.list();

    });
    //eliminar un producto de contrato
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


    //evento guardar
    $('form').on('submit', function (e) {
        e.preventDefault();
        if (produ.items.productos.length === 0) {
            message_error('Debe al menos tener un item en su detalle de compra');
            return false;
        }
        produ.items.fecha = $('input[name="venFechaInici"]').val();
        produ.items.fechafin = $('input[name="venFechaFin"]').val();
        produ.items.cliente = $('select[name="cliente"]').val();
        console.log(produ.items);
        var parameters = new FormData();
        parameters.append('action', $('input[name="action"]').val());
        parameters.append('ventas', JSON.stringify(produ.items));
        parameters.forEach(function (value, key) {
            console.log(key + ':' + value);

        });

        submit_with_ajax(window.location.pathname, 'Notification', '¿Estas seguro de realizar la siguiente acción?', parameters, function () {
            location.href = '/venta/contrato/mostrar/';
        });

    });

    produ.list();
    produ.list2();


});