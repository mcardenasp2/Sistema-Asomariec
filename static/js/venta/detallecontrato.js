var tblInsumos;
var prod = {
    items: {
        producto: '',
        fecha: '',
        detalle: '',
        cantidad: 0,
        precio: 0.00,
        iva: 0.00,
        total: 0.00,
        subtotal: 0.00,
        totalproduc: 0.00,
        // subtolagast: 0.00,
        insumos: [],

    },
    calculate_invoce: function () {

        var subtotal = 0.00;
        $.each(this.items.insumos, function (pos, dict) {
            dict.subtotal = dict.cant * parseFloat(dict.insPrecio);
            subtotal += dict.subtotal;
        });
        this.items.totalproduc = subtotal;
        // console.log(this.items.totalproduc);
        $('input[name="prodcTotal"]').val(this.items.totalproduc.toFixed(2));
        // this.totalp();

    },
    get_ids: function () {
        var ids = [];
        $.each(this.items.insumos, function (key, value) {

            ids.push(value.id);

        })
        return ids;

    },
    add: function (item) {
        // console.clear();
        // console.log('ban inici ' + band);
        // $.each(this.items.insumos, function (pos, dict) {
        //
        // });
        // console.log('buenas ' + band);
        this.items.insumos.push(item);

        this.list();

    },
    list: function () {
        this.calculate_invoce();
        // this.totalp();
        tblInsumos = $('#tblInsumos').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            data: this.items.insumos,
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
                {"data": "insDescripcion"},
                {"data": "insStock"},
                {"data": "medida.medDescripcion"},
                {"data": "insPrecio"},
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
                // var ty = data.insStock;
                var pp = 15;
                if ($('input[name="action"]').val() == 'add') {
                    var ty = data.insStock;
                } else {
                    var ty = data.cant + data.insStock - ct;
                }


                $(row).find('input[name="cant"]').TouchSpin({
                    min: 1,
                    // max: parseInt(pp),
                    max: parseInt(ty),
                    // max: 10,
                    step: 1,

                    verticalbuttons: true,
                    verticalupclass: 'glyphicon glyphicon-plus',
                    verticaldownclass: 'glyphicon glyphicon-minus'
                    // boostat: 5,
                });

            },
            initComplete: function (settings, json) {

            }
        });

        // console.log(this.get_ids());

    },

};

function formatRepo(repo) {
    if (repo.loading) {
        return repo.text;
    }

    var option = $(
        '<div class="wrapper container">' +
        '<div class="row">' +
        '<div class="col-lg-1">' +
        '<img src="' + repo.insImagen + '" class="img-fluid img-thumbnail d-block mx-auto rounded">' +
        '</div>' +
        '<div class="col-lg-11 text-left shadow-sm">' +
        //'<br>' +
        '<p style="margin-bottom: 0;">' +
        '<b>Nombre:</b> ' + repo.insDescripcion + '<br>' +
        '<b>Stock:</b> ' + repo.insStock + '<br>' +
        // '<b>PVP:</b> <span class="badge badge-warning">$' + repo.insPrecio + '</span>' +
        '</p>' +
        '</div>' +
        '</div>' +
        '</div>');

    return option;
};


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
        observacion: '',
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
            // ajax: {
            //     url: window.location.pathname,
            //     type: 'POST',
            //     data: {
            //         'action': 'searchdata'
            //     },
            //     dataSrc: ""
            // },
            columns: [
                {"data": "id"},
                {"data": "prodDescripcion"},
                {"data": "prodEstprod"},
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
                        var boton;

                        if (row.prodEstprod == 1) {
                            boton = '<a rel="detailsinsumos"   class="btn btn-primary btn-sm btn-flat not-active"  style="color: white;background: #80bdff"><i class="fas fa-edit"></i></a>';

                        } else if (row.prodEstprod == 2) {
                            boton = '<a rel="detailsinsumos"   class="btn btn-primary btn-sm btn-flat"  style="color: white"><i class="fas fa-edit"></i></a>';
                        }
                        ;

                        // return '<a disabled="true" rel="remove" class="btn btn-primary btn-sm btn-flat not-active"  style="color: white"><i class="fas fa-edit"></i></a>';
                        return boton;
                    }
                },
                {
                    targets: [2],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        var estado;
                        if (data == 1) {
                            estado = '<spam class="badge badge-pill badge-success">Finalizado</spam>';
                        } else if (data == 2) {
                            estado = '<spam class="badge badge-pill badge-default">En Proceso</spam>';
                        }
                        ;

                        // return '<a disabled="true" rel="remove" class="btn btn-primary btn-sm btn-flat not-active"  style="color: white"><i class="fas fa-edit"></i></a>';
                        return estado;

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
                    /*

                    render: function (data, type, row) {
                        return '<input type="text" name="cant" class="form-control form-control-sm input-sm" autocomplete="off" value="' + row.cant + '">';
                    }
                    */
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        var subt;
                        subt=row.cant*row.prodPrecio
                        return '$' + parseFloat(subt).toFixed(2);
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
                // {"data": "gastDescripcion"},
                {"data": "gastDescripcion"},
                {"data": "gastPrecio"},
                // {"data": "pvp"},
                // {"data": "cant"},
                // {"data": "subtotal"},
            ],
            columnDefs: [

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

        //Abrir Modal para poner los insumos

        $('#tblProducto tbody').on('click', 'a[rel="detailsinsumos"]', function () {
            var tr = tblProducto.cell($(this).closest('td, li')).index();
            var data = tblProducto.row(tr.row).data();
            console.log(data);
            $('input[name="nomproducto"]').val(data.prodDescripcion);
            $('input[name="producCantidad"]').val(data.cant);
            prod.items.producto = data.id;
            // console.clear();
            // console.log(prod.items.producto);
            $('#myModelInsumos').modal('show');

        });

        //Cerrar modal de insumos
        $('#myModelInsumos').on('hidden.bs.modal', function (e) {
            // $('#formInsumos').trigger('reset');
            prod.items.insumos = [];
            prod.list();
            // prod.items.insumos=[];
        });
        // Buscar insumos en el modal
        $('select[name="search"]').select2({
            theme: "bootstrap4",
            language: 'es',
            allowClear: true,
            ajax: {
                delay: 250,
                type: 'POST',
                url: window.location.pathname,
                data: function (params) {
                    // console.log(params)
                    var queryParameters = {
                        term: params.term,
                        action: 'search_insumos',
                        ids: JSON.stringify(prod.get_ids())
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
                var data = e.params.data;
                // console.log(data);
                // data.stock=10;
                // data.insStock

                data.cant = 1;
                ct = data.cant;
                data.subtotal = 0.00;
                // console.log(data);
                // console.log(data.insStock);


                prod.add(data);
                $(this).val('').trigger('change.select2');
            });
        //Borrar todos los insumos en el modal
        $('.btnRemoveAll').on('click', function () {
            //si no hay productos retorno falso
            if (prod.items.insumos.length === 0) return false;
            alerta_action('Notificacion', 'Estas seguro de Eliminar todos los items de tu detalle?', function () {
                prod.items.insumos = [];
                prod.list();
            });
        });
        //    evento eiminar insumo del modal
        $('#tblInsumos tbody')
            .on('click', 'a[rel="remove"]', function () {
                //Obtengo la posicion
                var tr = tblInsumos.cell($(this).closest('td, li')).index();
                alerta_action('Notificacion', 'Estas seguro de Eliminar el insumo de tu detalle?', function () {
                    prod.items.insumos.splice(tr.row, 1);
                    //    actualizams
                    prod.list();
                });

            })

            //   evento cambiar cantidad keyup s no pongo el touchspin
            .on('change', 'input[name="cant"]', function () {
                console.clear();
                //obtengo el valor de la cantidd
                var cant = parseInt($(this).val());
                //me devuelve la fila para sacar el row
                var tr = tblInsumos.cell($(this).closest('td, li')).index();
                console.log(tr);
                //devuelvo el tr completo mediante la fila
                // var data= tblInsumos.row(tr.row).node();
                // console.log(data);
                prod.items.insumos[tr.row].cant = cant;
                //actualizo la factura
                prod.calculate_invoce();
                // console.log(data);
                $('td:eq(6)', tblInsumos.row(tr.row).node()).html('$' + prod.items.insumos[tr.row].subtotal.toFixed(2));

            });


        //guardar produccion
        $('#formInsumos').on('submit', function (e) {
            // alert(x);

            e.preventDefault();
            if (prod.items.insumos.length === 0) {
                message_error('Debe al menos tener un item en su detalle');
                return false;
            }
            // prod.items.producto = $('select[name="producto"]').val();
            // prod.items.detalle = $('textarea[name="prodCaracteristica"]').val();
            prod.items.cantidad = $('input[name="producCantidad"]').val();
            prod.items.fecha = date_now;
            prod.items.precio = $('input[name="prodcTotal"]').val();
            // prod.items.iva = $('input[name="prodIva"]').val();
            // prod.items.subtolagast = $('input[name="subtolagast"]').val();

            // console.log(prod.items);
            var parameters = new FormData();
            parameters.append('action', 'create_produccion');
            // parameters.append('imagen1',fileInputElement.files[0]);
            // parameters.append('imagen2', fi);
            // $('#file')[0].files[0]) una tercera coma para el nombre
            // parameters.append('imagen1', $('input[name="prodImagen"]')[0].files[0], 'Marco');
            // parameters.append('imagen1', $('input[name="prodImagen"]')[0].files[0]);
            // parameters.append('imagen2', $('input[name="prodImagen2"]')[0].files[0]);
            parameters.append('insumos', JSON.stringify(prod.items));
            parameters.forEach(function (value, key) {
                console.log(key + ':' + value);

            });
            // console.log(parameters);
            submit_with_ajax(window.location.pathname, 'Notification', '¿Estas seguro de realizar la siguiente acción?', parameters, function () {
                // location.href = '/producto/produccion/mostrar/';

                // produ.list();

                // console.log("no se :c")
                // tblProducto.ajax.reload();
                // tblProducto.ajax.reload();
                $('#myModelInsumos').modal('hide');
                location.href = window.location.pathname;
                // produ.list();

            });

        });

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
            gast.id = 0;
            gast.cant = 1;
            gast.subtotal = 0.00;
            if (gast.prodDescripcion === '' || gast.prodPrecio === '') return false;
            //
            produ.add(gast);

            $('input[name="descripcionc"]').val('');
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


        //evento guardar
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
            produ.items.ventestado = $('select[name="venEstVenta"]').val();
            // produ.items.observacion = $('input[name="ventObservacion"]').val();
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

        prod.list();


    }
);