var ct = 0;
var tblInsumos;
var prod = {
    items: {
        producto: '',
        fecha:'',
        detalle: '',
        cantidad: 0,
        precio: 0.00,
        iva: 0.00,
        total: 0.00,
        subtotal: 0.00,
        totalproduc: 0.00,
        // subtolagast: 0.00,
        insumos: [],
        gastosad: [],
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
        var band;
        band = 1;
        // console.log('ban inici ' + band);
        $.each(this.items.insumos, function (pos, dict) {
            // console.log('dentro ' + dict.id);
            // console.log('fuera ' + item.id);
            if (parseInt(dict.id) == parseInt(item.id)) {
                // console.log('vamos a ver');
                // console.log('bandera' + band);
                // console.log('xxxxx');
                band = 0;
                return false;

            }


        });
        // console.log('buenas ' + band);
        if (band == 1) {
            this.items.insumos.push(item);
        }


        // console.log(band);
        band = 1;
        this.list();

    },
    calculate_invoce: function () {

        var subtotal = 0.00;
        $.each(this.items.insumos, function (pos, dict) {
            // console.log(pos);
            // console.log(dict);
            dict.subtotal = dict.cant * parseFloat(dict.instotalprecio);
            subtotal += dict.subtotal;
        });
        this.items.totalproduc = subtotal;
        // console.clear();
        // console.log('prueba');
        // console.log(this.items.totalproduc);
        $('input[name="prodcTotal"]').val(this.items.totalproduc.toFixed(2));
        // this.totalp();

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
                {"data": "instotalprecio"},
                // {"data": "pvp"},
                {"data": "cant"},
                {"data": "subtotal"},
            ],
            columnDefs: [
                {
                    targets: [1,2,3,4],
                    class: 'text-center',
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
        '<div class="col-lg-2">' +
        '<img src="' + repo.insImagen + '" style="height: 100px; width: 200px" class="img-fluid img-thumbnail d-block mx-auto rounded">' +
        '</div>' +
        '<div class="col-lg-10 text-left shadow-sm">' +
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
}


$(function () {


    $('#prodcFecElab').datetimepicker({
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

    //eliminar todos los productos
    $('.btnRemoveAll').on('click', function () {
        //si no hay productos retorno falso
        if (prod.items.insumos.length === 0) return false;
        alerta_action('Notificacion', 'Estas seguro de Eliminar todos los items de tu detalle?', function () {
            prod.items.insumos = [];
            prod.list();
        });


    });

    //    evento eiminar insumo de de la tabla
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

     //evento guardar
    $('form').on('submit', function (e) {
        // alert('c');
        e.preventDefault();
        if (prod.items.insumos.length === 0) {
            message_error('Debe al menos tener un item en su detalle');
            return false;
        }
        // console.log('hol');
        prod.items.producto = $('select[name="producto"]').val();
        // prod.items.detalle = $('textarea[name="prodCaracteristica"]').val();
        prod.items.cantidad = $('input[name="prodcCantidad"]').val();
        prod.items.fecha = $('input[name="prodcFecElab"]').val();
        prod.items.precio = $('input[name="prodcTotal"]').val();
        // prod.items.iva = $('input[name="prodIva"]').val();
        // prod.items.subtolagast = $('input[name="subtolagast"]').val();

        console.log(prod.items);
        var parameters = new FormData();
        parameters.append('action', $('input[name="action"]').val());
        // parameters.append('imagen1',fileInputElement.files[0]);
        // parameters.append('imagen2', fi);
        // $('#file')[0].files[0]) una tercera coma para el nombre
        // parameters.append('imagen1', $('input[name="prodImagen"]')[0].files[0], 'Marco');
        // parameters.append('imagen1', $('input[name="prodImagen"]')[0].files[0]);
        // parameters.append('imagen2', $('input[name="prodImagen2"]')[0].files[0]);
        parameters.append('compras', JSON.stringify(prod.items));
        parameters.forEach(function (value, key) {
            console.log(key + ':' + value);

        });
        // console.log(parameters);
        submit_with_ajax(window.location.pathname, 'Notification', '¿Estas seguro de realizar la siguiente acción?', parameters, function () {
            location.href = '/producto/produccion/mostrar/';

        });

    });


     prod.list();

});