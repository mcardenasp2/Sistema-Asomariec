var date_range = null;
var date_now = new moment().format('YYYY-MM-DD');
var fechaini = date_now;
var fechafin = date_now;
var tblGast;
var tblProducto;
var produ = {
    items: {
        cliente: '',
        fecha: '',
        fechafin: '',
        ventestado: '',
        observacion:'',
        // precio: 0.00,
        tgsto: 0.00,
        subproductos: 0.00,
        impuestos: 0.00,
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
        console.log(this.items.subproductos);

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
        var iva = 0.00;
        ga = parseFloat($('input[name="gastoadicionales"]').val());
        st = parseFloat($('input[name="subtotal"]').val());
        iva = parseFloat($('input[name="iva"]').val());
        t = ga + st + iva;
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
                {"data": "prodIva"},
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
                    targets: [-4],
                    class: 'text-center',
                    orderable: false,
                    // render: function (data, type, row) {
                    //     return '<div class="input-group input-group-sm"><input type="text" name="prodPrecio" class="form-control form-control-sm input-sm" autocomplete="off" value="' + row.prodPrecio + '"></div>';
                    // }
                },
                {
                    targets: [-3],
                    class: 'text-center',
                    orderable: false,
                    // render: function (data, type, row) {
                    //     return '<div class="input-group input-group-sm"><input type="text" name="prodIva" class="form-control form-control-sm input-sm" autocomplete="off" value="' + row.prodIva + '"></div>';
                    // }
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
                    verticalbuttons: true,
                    verticalupclass: 'glyphicon glyphicon-plus',
                    verticaldownclass: 'glyphicon glyphicon-minus'
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
        // $('#venFechaInici').datetimepicker({
        //     icons: {
        //         time: "fa fa-clock",
        //         date: "fa fa-calendar-day",
        //         up: "fa fa-chevron-up",
        //         down: "fa fa-chevron-down",
        //         previous: 'fa fa-chevron-left',
        //         next: 'fa fa-chevron-right',
        //         today: 'fa fa-screenshot',
        //         clear: 'fa fa-trash',
        //         close: 'fa fa-remove'
        //     },
        //     format: 'YYYY-MM-DD',
        //     // date: moment().format("YYYY-MM-DD"),
        //     locale: 'es',
        //     //minDate: moment().format("YYYY-MM-DD")
        // });
        // $('#venFechaFin').datetimepicker({
        //     icons: {
        //         time: "fa fa-clock",
        //         date: "fa fa-calendar-day",
        //         up: "fa fa-chevron-up",
        //         down: "fa fa-chevron-down",
        //         previous: 'fa fa-chevron-left',
        //         next: 'fa fa-chevron-right',
        //         today: 'fa fa-screenshot',
        //         clear: 'fa fa-trash',
        //         close: 'fa fa-remove'
        //     },
        //     format: 'YYYY-MM-DD',
        //     // date: moment().format("YYYY-MM-DD"),
        //     locale: 'es',
        //     // minDate: $('#venFechaInici').val(),
        //     //minDate: moment().format("YYYY-MM-DD")
        // });


        //anadir producto contrato
        $('.addcontr').on('click', function (e) {
            // alert('xxx');
            e.preventDefault();
            var gast = {};
            //
            gast.prodDescripcion = $('input[name="descripcionc"]').val();
            gast.prodPrecio = $('input[name="precioc"]').val();
            gast.prodIva = $('input[name="ivac"]').val();
            gast.categoria = $('select[name="categoria"]').val();
            gast.id = 0;
            gast.cant = 1;
            gast.subtotal = 0.00;
            if (gast.prodDescripcion === '' || gast.prodPrecio === ''||gast.categoria==='' ) return false;
            //
            console.log(gast)
            produ.add(gast);

            $('input[name="descripcionc"]').val('');
            // $('select[name="categoria"]').val="";
            $('input[name="precioc"]').val('1.00');
            $('input[name="ivac"]').val('0.12');
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
                $('td:eq(5)', tblProducto.row(tr.row).node()).html('$' + produ.items.productos[tr.row].subtotal.toFixed(2));
            }).on('change keyup', 'input[name="prodPrecio"]', function () {
            // prodPrecio
            // alert('x');
            var precio = parseFloat($(this).val());
            console.log(precio)
            var tr = tblProducto.cell($(this).closest('td, li')).index();
            // console.log(tr);
            produ.items.productos[tr.row].prodPrecio = precio;
            produ.calculate_invoice();
            $('td:eq(5)', tblProducto.row(tr.row).node()).html('$' + produ.items.productos[tr.row].subtotal.toFixed(2));

        }).on('change keyup', 'input[name="prodIva"]', function () {
            // prodPrecio
            // alert('x');
            var iva = parseFloat($(this).val());
            // console.log(precio)
            var tr = tblProducto.cell($(this).closest('td, li')).index();
            // console.log(tr);
            produ.items.productos[tr.row].prodIva = iva;
            produ.calculate_invoice();
            $('td:eq(5)', tblProducto.row(tr.row).node()).html('$' + produ.items.productos[tr.row].subtotal.toFixed(2));

        });

        //gastos
        $('.btnGastos').on('click', function () {
            $('#myModelDet').modal('show');

        });

        // $('input[name="preciogasto"]').TouchSpin({
        //     min: 1,
        //     max: 100,
        //     step: 0.1,
        //     decimals: 2,
        //     verticalbuttons: true,
        //     verticalupclass: 'glyphicon glyphicon-plus',
        //     verticaldownclass: 'glyphicon glyphicon-minus'
        //
        // });

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

        //Rango de Fechas
        // fechaini = $('#venFechaInici').val();
        // fechafin = $('#venFechaFin').val();
        fechaini = $('input[name="venFechaInici"]').val();
        // console.log(fechaini);
        fechafin = $('#venFechaFin').val();

        $('input[name="date_range"]').daterangepicker({
            startDate: fechaini,
            endDate: fechafin,
            locale: {
                format: 'YYYY-MM-DD',
                applyLabel: '<i class="fas fa-chart-pie"></i> Aplicar',
                cancelLabel: '<i class="fas fa-times"></i> Cancelar',
            }
        })
            .on('apply.daterangepicker', function (ev, picker) {
                date_range = picker;

            })
            .on('cancel.daterangepicker', function (ev, picker) {
                $(this).data('daterangepicker').setStartDate(fechaini);
                $(this).data('daterangepicker').setEndDate(fechafin);
                date_range = picker;
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


        //evento guardar Venta
        $('#frmVentaContrato').on('submit', function (e) {
            e.preventDefault();
            if (produ.items.productos.length === 0) {
                message_error('Debe al menos tener un item en su detalle de compra');
                return false;
            }
            if (date_range !== null) {
                produ.items.fecha = date_range.startDate.format('YYYY-MM-DD');
                produ.items.fechafin = date_range.endDate.format('YYYY-MM-DD');
            } else {
                produ.items.fecha = fechaini;
                produ.items.fechafin = fechafin;
            }
            // produ.items.fecha = $('input[name="venFechaInici"]').val();
            // produ.items.fechafin = $('input[name="venFechaFin"]').val();
            produ.items.cliente = $('select[name="cliente"]').val();
            // produ.items.ventestado = $('select[name="venEstVenta"]').val();
            produ.items.ventestado = 1;
            produ.items.observacion=$('input[name="ventObservacion"]').val();
            console.log(produ.items);
            var parameters = new FormData();
            parameters.append('action', $('input[name="action"]').val());
            parameters.append('ventas', JSON.stringify(produ.items));
            parameters.forEach(function (value, key) {
                console.log(key + ':' + value);

            });

            submit_with_ajax(window.location.pathname, 'Notification', '¿Estas seguro de realizar la siguiente acción?', parameters, function (response) {
                alerta_action2('Notificacion', '¿Desea Imprimir la Boleta de Venta?', function () {
                    window.open('/venta/contrato/invoice/pdf/' + response.id + '/', '_blank')
                    location.href = '/venta/contrato/mostrar/';
                }, function () {
                    location.href = '/venta/contrato/mostrar/';

                });

                // location.href = '/venta/contrato/mostrar/';
            });

        });

        produ.list();
        produ.list2();


    }
);