var tblInsumos;
var comp = {
    items: {
        proveedor: '',
        vendedor: '',
        cedula: '',
        usuaid: '',
        fecha: '',
        subtotal: 0.00,
        iva: 0.00,
        total: 0.00,
        insumos: []

    },
    add: function (item) {
        //anado el detalle
        this.items.insumos.push(item);
        this.list();

    },
    //calculo de subtotal de la tabla
    calculate_invoce: function () {
        //contiene la suma total
        var subtotal = 0.00;
        var iva = $('input[name="ccoIva"]').val();
        //por cada item de insumo, me devuelve posicion y valor
        $.each(this.items.insumos, function (pos, dict) {
            // console.log(pos);
            // console.log(dict);
            dict.subtotal = dict.cant * parseFloat(dict.insPrecio);
            subtotal += dict.subtotal;
        });
        // console.log(subtotal);
        //cambie y multilique or 0.88
        this.items.subtotal = subtotal*0.88;
        //cambie y puse lo de abajo
        // this.items.iva = this.items.subtotal * iva;
        this.items.iva = subtotal * 0.12;
        this.items.total = this.items.subtotal + this.items.iva;
        // console.log(subtotal);
        //solo cundo el valor es float
        //devolucion en el input subtotal
        $('input[name="subtotal"]').val(this.items.subtotal.toFixed(2));
        $('input[name="ivacalc"]').val(this.items.iva.toFixed(2));
        $('input[name="total"]').val(this.items.total.toFixed(2));

    },
    list: function () {
        this.calculate_invoce();
        tblInsumos = $('#tblInsumos').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            data: this.items.insumos,
            columns: [
                {"data": "id"},
                {"data": "insDescripcion"},
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

                $(row).find('input[name="cant"]').TouchSpin({
                    min: 1,
                    max: 1000000000,
                    step: 1
                });

            },
            initComplete: function (settings, json) {

            }
        });


    },


};

$(function () {
    //numeros cambie y lo desapareci
    // $("input[name='ccoIva']").TouchSpin({
    //     min: 0,
    //     max: 1,
    //     step: 0.01,
    //     decimals: 2,
    //     boostat: 5,
    //     maxboostedstep: 10,
    //     postfix: '%'
    // })
    //     .on('change', function () {
    //         //calculo de nuevo la factura para que se actualice
    //         comp.calculate_invoce();
    //
    //     })
    //     .val(0.12);
    //   evento  iva
    // $('input[name="iva"]')
    //     .on('change', function () {
    //         //calculo de nuevo la factura para que se actualice
    //         comp.calculate_invoce();
    //
    //     })
    //     .val(0.12);

    $('.mySelect2').select2({

        dropdownAutoWidth: true,


        width: 'auto',

        placeholder: 'Seleccione una opcion',


    });

// evento calendarip
    $('#ccoFecCom').datetimepicker({
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


// evento search insumos
    $('input[name="search"]').autocomplete({


        source: function (request, response) {

            $.ajax({
                url: window.location.pathname,
                type: 'POST',
                data: {
                    'action': 'search_insumos',
                    //enviamos el termino
                    'term': request.term

                },
                dataType: 'json',
            }).done(function (data) {
                response(data);
                // console.log();

            }).fail(function (jqXHR, textStatus, errorThrown) {
                //alert(textStatus + ': ' + errorThrown);
            }).always(function (data) {

            });

        },
        delay: 500,
        minLength: 1,
        select: function (event, ui) {
            event.preventDefault();
            // console.log('hola');
            // console.log(ui.item);
            console.clear();
            //agrego los insumo uno por uno
            ui.item.cant = 1;
            ui.item.subtotal = 0.00;
            // comp.items.insumos.push(ui.item);
            // comp.list();
            comp.add(ui.item);
            console.log(comp.items.insumos);
            $(this).val('');
        }
    });
//Evento eliminar items
    $('.btnRemoveAll').on('click', function () {
        //si no hay productos retorno falso
        if (comp.items.insumos.length === 0) return false;
        alerta_action('Notificacion', 'Estas seguro de Eliminar todos los items de tu detalle?', function () {
            comp.items.insumos = [];
            comp.list();
        });


    });

//    evento eiminar insumo de de la tabla
    $('#tblInsumos tbody')
        .on('click', 'a[rel="remove"]', function () {
            // alert('x');
            //Obtengo la posicion

            var tr = tblInsumos.cell($(this).closest('td, li')).index();
            alerta_action('Notificacion', 'Estas seguro de Eliminar el insumo de tu detalle?', function () {
                comp.items.insumos.splice(tr.row, 1);
                //    actualizams
                comp.list();
            });

        })

        //   evento cambiar cantidad
        .on('change keyup', 'input[name="cant"]', function () {
            console.clear();
            //obtengo el valor de la cantidd
            var cant = parseInt($(this).val());
            //me devuelve la fila para sacar el row
            var tr = tblInsumos.cell($(this).closest('td, li')).index();
            console.log(tr);
            //devuelvo el tr completo mediante la fila
            // var data= tblInsumos.row(tr.row).node();
            // console.log(data);
            comp.items.insumos[tr.row].cant = cant;
            //actualizo la factura
            comp.calculate_invoce();
            // console.log(data);
            $('td:eq(4)', tblInsumos.row(tr.row).node()).html('$' + comp.items.insumos[tr.row].subtotal.toFixed(2));

        });

//    Elimiminar lo del buscador
    $('.btnClearSearch').on('click', function () {
        $('input[name="search"]').val('').focus();
    });

//    evento guardar

    $('form').on('submit', function (e) {
        e.preventDefault();
        if (comp.items.insumos.length === 0) {
            message_error('Debe al menos tener un item en su detalle de compra');
            return false;

        }

        comp.items.fecha = $('input[name="ccoFecCom"]').val();
        comp.items.proveedor = $('select[name="proveedor"]').val();
        comp.items.vendedor = $('input[name="Vendedor"]').val();
        comp.items.cedula = $('input[name="Cedula"]').val();
        comp.items.usuaid = $('input[name="usuaReg"]').val();


        var parameters = new FormData();
        parameters.append('action', $('input[name="action"]').val());
        //convierto  string
        parameters.append('compras', JSON.stringify(comp.items));
        console.log(parameters);


        // console.log(parameters.get('insImagen')['name']);

        // parameters.forEach(function (value, key) {
        //     console.log(key + ':' + value);
        // });
        submit_with_ajax(window.location.pathname, 'Notification', '¿Estas seguro de realizar la siguiente acción?', parameters, function () {
            location.href = '{{ list_url }}';
        });
    });

    comp.list();

});
