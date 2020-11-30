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
        // if (item.id==this.items.insumos.id)
        //     alert('c');
        //     console.log('Estas en lo correcto');
        //esto puse yo el each para no guardar datos repetidos
        // for (var i = 0; i < this.items.insumos.length; i++ )
        // {
        //     if (this.items.insumos[i].id !== item.id){
        //         this.items.insumos.push(item);
        //     }else{
        //         this.items.insumos[i].cant += 1;
        //         return false;
        //     }
        // }
        this.items.insumos.push(item);
        this.list();

        // $.each(this.items.insumos, function (pos, dict) {
        //     // console.log(dict.id);
        //     if (dict.id == item.id)
        //         return false;
        //     else
        //         this.items.insumos.push(item);
        //         this.list();
        //     // console.log('ggg');
        // });
        // console.log(this.items.insumos.id.includes(1));


        // this.items.insumos.push(item);
        // this.list();

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
        this.items.subtotal = subtotal * 0.88;
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
                {"data": "medida.medDescripcion"},
                {"data": "insPrecio"},

                {"data": "cant"},
                {"data": "subtotal"},
            ],
            columnDefs: [
                {
                    targets: [1, 2],
                    class: 'text-center',
                    orderable: false,
                },
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
                    max: 100000,
                    step: 1,
                    verticalbuttons: true,
                    verticalupclass: 'glyphicon glyphicon-plus',
                    verticaldownclass: 'glyphicon glyphicon-minus',
                    // sufijo:'sss'
                    // boostat: 5,
                });

            },
            initComplete: function (settings, json) {

            }
        });


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
        '<b>Categoría:</b> ' + repo.categoria.catDescripcion + '<br>' +
        '<b>PVP:</b> <span class="badge badge-warning">$' + repo.insPrecio + '</span>' +
        '</p>' +
        '</div>' +
        '</div>' +
        '</div>');

    return option;
}


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
        // date: moment().format("YYYY-MM-DD"),
        locale: 'es',
        //minDate: moment().format("YYYY-MM-DD")
    });


// evento search insumos jquery ui
    /*
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

    */

//Evento eliminar items
    $('.btnRemoveAll').on('click', function () {
        //si no hay productos retorno falso
        if (comp.items.insumos.length === 0) return false;
        alerta_action2('Notificacion', 'Estas seguro de Eliminar todos los items de tu detalle?', function () {
            comp.items.insumos = [];
            comp.list();
        }, function () {

        });


    });

//    evento eiminar insumo de de la tabla
    $('#tblInsumos tbody')
        .on('click', 'a[rel="remove"]', function () {
            // alert('x');
            //Obtengo la posicion

            var tr = tblInsumos.cell($(this).closest('td, li')).index();
            alerta_action2('Notificacion', 'Estas seguro de Eliminar el insumo de tu detalle?', function () {
                comp.items.insumos.splice(tr.row, 1);
                //    actualizams
                comp.list();
            }, function () {

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
            comp.items.insumos[tr.row].cant = cant;
            //actualizo la factura
            comp.calculate_invoce();
            // console.log(data);
            $('td:eq(5)', tblInsumos.row(tr.row).node()).html('$' + comp.items.insumos[tr.row].subtotal.toFixed(2));

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
        comp.items.vendedor = $('input[name="ccoVendedor"]').val();
        comp.items.cedula = $('input[name="ccoCedVend"]').val();
        comp.items.usuaid = $('input[name="ccoCedVend"]').val();
        // console.log(comp.items);


        var parameters = new FormData();
        parameters.append('action', $('input[name="action"]').val());
        //convierto  string
        parameters.append('compras', JSON.stringify(comp.items));
        parameters.append('documento', $('input[name="ccoDocumento"]')[0].files[0]);
        // console.log(parameters);


        // console.log(parameters.get('insImagen')['name']);

        // parameters.forEach(function (value, key) {
        //     console.log(key + ':' + value);
        // });
        submit_with_ajax(window.location.pathname, 'Notification', '¿Estas seguro de realizar la siguiente acción?', parameters, function (response) {
            alerta_action2('Notificacion', '¿Desea Imprimir la Boleta de Compra?', function () {
                window.open('/compra/compra/invoice/pdf/' + response.id + '/', '_blank')
                location.href = '/compra/compra/mostrar/';
            }, function () {
                location.href = '/compra/compra/mostrar/';

            });

        });
    });


    //Buscar insumos
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
                    action: 'search_insumos'
                };
                return queryParameters;
            },
            processResults: function (data) {
                console.log(data);
                return {
                    results: data
                };
            },
        },
        placeholder: 'Ingrese una descripción',
        minimumInputLength: 1,
        templateResult: formatRepo,
    })
        .on('select2:select', function (e) {
            // alert('c');
            var data = e.params.data;
            // console.clear();
            // console.log(data);


            data.cant = 1;
            // data.canta = 1;
            data.subtotal = 0.00;

            // console.log(data);


            comp.add(data);
            $(this).val('').trigger('change.select2');
        });

    comp.list();

});
