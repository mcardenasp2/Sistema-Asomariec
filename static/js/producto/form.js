var ct = 0;
var tblInsumos;
var tblGast;
var prod = {
    items: {
        producto: '',
        detalle: '',
        cantidad: 0,
        precio: 0.00,
        iva: 0.00,
        total: 0.00,
        totalproduc: 0.00,
        subtolagast: 0.00,
        insumos: [],
        gastosad: [],
    },
    add: function (item) {
        // console.clear();
        var band;
        band = 1;
        console.log('ban inici ' + band);
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
    // calculate_invoce: function () {
    //
    //     var subtotal = 0.00;
    //     $.each(this.items.insumos, function (pos, dict) {
    //         // console.log(pos);
    //         // console.log(dict);
    //         dict.subtotal = dict.cant * parseFloat(dict.insPrecio);
    //         subtotal += dict.subtotal;
    //     });
    //     this.items.totalproduc = subtotal;
    //     // console.clear();
    //     // console.log('prueba');
    //     // console.log(this.items.totalproduc);
    //     $('input[name="totalproduc"]').val(this.items.totalproduc.toFixed(2));
    //     this.totalp();
    //
    // },
    // totalp: function () {
    //     var tot = 0.00;
    //     tot = this.items.totalproduc + this.items.subtolagast;
    //     this.items.total = parseFloat(tot)
    //     // this.items.total = 225.50
    //     // console.log(tot);
    //     $('input[name="prodTotal"]').val(this.items.total.toFixed(2));
    //     var pr = 0.00;
    //     pr = $('input[name="prodCantidad"]').val();
    //     pr = this.items.total / pr;
    //     // $('input[name="precioprod"]').val(this.items.total.toFixed(2));
    //     $('input[name="precioprod"]').val(pr.toFixed(2));
    //
    //
    // },
    list: function () {
        // this.calculate_invoce();
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
                    // boostat: 5,
                });

            },
            initComplete: function (settings, json) {

            }
        });

    },
    // addgasto: function (item) {
    //     this.items.gastosad.push(item);
    //     this.listgast();
    //
    // },
    // calculate_invoce_gasto: function () {
    //
    //     var subtotalg = 0.00;
    //     $.each(this.items.gastosad, function (pos, dict) {
    //         // console.log(pos);
    //         // console.log(dict);
    //         // dict.subtotal = dict.cant * parseFloat(dict.insPrecio);
    //         subtotalg += parseFloat(dict.gastPrecio);
    //     });
    //     this.items.subtolagast = subtotalg;
    //
    //     // $('input[name="gastoadicionales"]').val(this.items.subtolagast);
    //     $('input[name="gastoadicionales"]').val(this.items.subtolagast.toFixed(2));
    //     this.totalp();
    //
    //
    // },

    // listgast: function () {
    //     // this.total();
    //
    //     // this.calculate_invoce_gasto();
    //     // this.totalp();
    //     tblGast = $('#tblDet').DataTable({
    //         responsive: true,
    //         autoWidth: false,
    //         destroy: true,
    //         data: this.items.gastosad,
    //         language: {
    //             processing: 'Procesando...',
    //             // search: 'Buscar:',
    //             search: "Buscar: _INPUT_",
    //             // searchPlaceholder: "Buscar Registros",
    //             lengthMenu: '   Mostrar _MENU_ registros',
    //             info: 'Mostrando desde _START_ al _END_ de _TOTAL_ registros',
    //             infoEmpty: 'Mostrando ningún elemento.',
    //             infoFiltered: '(filtrado _MAX_ elementos total)',
    //             infoPostFix: '',
    //             loadingRecords: 'Cargando registros...',
    //             zeroRecords: 'No se encontraron registros',
    //             emptyTable: 'No hay datos disponibles en la tabla',
    //             paginate: {
    //                 first: 'Primero',
    //                 previous: '<-',
    //                 next: '->',
    //                 last: 'Último'
    //             }
    //         },
    //         columns: [
    //             // {"data": "id"},
    //             {"data": "gastDescripcion"},
    //             {"data": "gastDescripcion"},
    //             {"data": "gastPrecio"},
    //             // {"data": "pvp"},
    //             // {"data": "cant"},
    //             // {"data": "subtotal"},
    //         ],
    //         columnDefs: [
    //             {
    //                 targets: [0],
    //                 class: 'text-center',
    //                 orderable: false,
    //                 render: function (data, type, row) {
    //                     return '<a rel="remove" class="btn btn-danger btn-sm btn-flat" style="color: white"><i class="fas fa-trash-alt"></i></a>';
    //                 }
    //             },
    //             {
    //                 targets: [-1],
    //                 class: 'text-center',
    //                 orderable: false,
    //                 render: function (data, type, row) {
    //                     return '$' + parseFloat(data).toFixed(2);
    //                 }
    //             },
    //         ],
    //
    //         initComplete: function (settings, json) {
    //
    //         }
    //     });
    //
    // },


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

    //gastos adicionales

    // $('.btnGastos').on('click', function () {
    //     $('#myModelDet').modal('show');
    //
    // });

    // $('.addgast').on('click', function () {

        // var gast = {};
        // gast.gastDescripcion = $('input[name="descripcion"]').val();
        // gast.gastPrecio = $('input[name="precio"]').val();
        // if (gast.gastDescripcion === '' || gast.gastPrecio === '') return false;
        // prod.addgasto(gast);
        // $('input[name="descripcion"]').val('');
        // $('input[name="precio"]').val('');


    // });


    //total precio venta
    // $('input[name="prodCantidad"]').on('change keyup', function () {
    //     // alert('x');
    //     // prod.calculate_invoce();
    //     // prod.calculate_invoce_gasto();
    //     prod.totalp();
    //     // var uni=0.00
    //     // uni=prod.items.total/$(this).val();
    //     // $('input[name="precioprod"]').val(uni);
    //
    // });

    //eliminar item de gastos adicionales
    // $('#tblDet tbody')
    //     .on('click', 'a[rel="remove"]', function () {
    //         // alert('x');
    //         //Obtengo la posicion
    //
    //         var tr = tblGast.cell($(this).closest('td, li')).index();
    //         alerta_action('Notificacion', 'Estas seguro de Eliminar el insumo de tu detalle?', function () {
    //             prod.items.gastosad.splice(tr.row, 1);
    //             //    actualizams
    //             prod.listgast();
    //         });
    //
    //     });


    //    evento eiminar insumo de de la tabla
    $('#tblInsumos tbody')
        .on('click', 'a[rel="remove"]', function () {
            // alert('x');
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
            // prod.calculate_invoce();
            // console.log(data);
            $('td:eq(4)', tblInsumos.row(tr.row).node()).html('$' + prod.items.insumos[tr.row].subtotal.toFixed(2));

        });

    //BUscar Insumos

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
            ct = data.cant;
            data.subtotal = 0.00;
            console.log(data);
            console.log(data.insStock);


            prod.add(data);
            $(this).val('').trigger('change.select2');
        });

    //evento guardar
    $('form').on('submit', function (e) {
        // alert('c');
        e.preventDefault();
        if (prod.items.insumos.length === 0) {
            message_error('Debe al menos tener un item en su detalle de compra');
            return false;
        }
        // console.log('hol');
        prod.items.producto = $('input[name="prodDescripcion"]').val();
        prod.items.detalle = $('textarea[name="prodCaracteristica"]').val();
        prod.items.cantidad = $('input[name="prodCantidad"]').val();
        prod.items.precio = $('input[name="prodPrecio"]').val();
        prod.items.iva = $('input[name="prodIva"]').val();
        // prod.items.subtolagast = $('input[name="subtolagast"]').val();

        console.log(prod.items);
        var parameters = new FormData();
        parameters.append('action', $('input[name="action"]').val());
        // parameters.append('imagen1',fileInputElement.files[0]);
        // parameters.append('imagen2', fi);
        // $('#file')[0].files[0]) una tercera coma para el nombre
        // parameters.append('imagen1', $('input[name="prodImagen"]')[0].files[0], 'Marco');
        parameters.append('imagen1', $('input[name="prodImagen"]')[0].files[0]);
        parameters.append('imagen2', $('input[name="prodImagen2"]')[0].files[0]);
        parameters.append('compras', JSON.stringify(prod.items));
        parameters.forEach(function (value, key) {
            console.log(key + ':' + value);

        });
        // console.log(parameters);
        submit_with_ajax(window.location.pathname, 'Notification', '¿Estas seguro de realizar la siguiente acción?', parameters, function () {
            location.href = '/producto/producto/mostrar/';

        });

    });


    prod.list();

    // prod.listgast();
    // prod.total();

});