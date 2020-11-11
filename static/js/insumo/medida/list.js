var tblMedida;

function getData() {
    //datatable
    tblMedida= $('#table_id').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        paging: true,
        // {#Bolo#}
        ordering: true,
        info: true,
        pageLength: 5,
        searching: true,
        responsive: false,

          // scrollY: 400,
        // paging: false,


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
            {"data": "medDescripcion"},
            {"data": "medDescripcion"},
            // {"data": "desc"},
        ],
        columnDefs: [
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<a href="#" rel="edit" class="btn btn-warning btn-sm btn-flat"><i class="fas fa-edit"></i></a> ';
                    buttons += '<a href="#" type="button" rel="delete" class="btn btn-danger btn-sm btn-flat"><i class="fas fa-trash-alt"></i></a>';
                    // var buttons = '<a href="/insumo/categoria/editar/' + row.id + '/" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
                    // buttons += '<a href="/insumo/categoria/eliminar/' + row.id + '/" type="button" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a>';

                    return buttons;
                }
            },
        ],
        initComplete: function (settings, json) {

        }
    });

}


$(function () {

    getData();

    //aplastar el btn add
    $('.btnAdd').on('click', function () {
        $('#id_medDescripcion').val('');
        // $('input[id="id_medDescripcion"]').val('add');
        $('input[name="action"]').val('add');
        //limpio el formulario
        // $('form')[0].reset();

        //abro el modal
        $('#myModalMedida').modal('show');

    });
    //Editar
    $('#table_id tbody')
        .on('click', 'a[rel="edit"]', function () {
            // alert('x');
            //toma el valor si llega a ver un tr o li
            // var tr= tblCategoria.cell($(this).closest('td, li')).index();
            //otra forma de tomar datos
            // var data=  tblCategoria.row(tr.row).data();
            //para tomarme los datos
            var data = tblMedida.row($(this).parents('tr')).data();

            $('input[name="action"]').val('edit');
            // $('input[name="user1"]').val(1);
            //datos de la tabla
            $('input[name="medDescripcion"]').val(data.medDescripcion);
            $('input[name="id"]').val(data.id);

            //abro el modal
            $('#myModalMedida').modal('show');
            // console.log(data);


        })
        .on('click', 'a[rel="delete"]', function () {
            // alert('x');
            //toma el valor si llega a ver un tr o li
            // var tr= tblCategoria.cell($(this).closest('td, li')).index();
            //otra forma de tomar datos
            // var data=  tblCategoria.row(tr.row).data();
            //para tomarme los datos
            var data = tblMedida.row($(this).parents('tr')).data();

            // console.log(data);
            var user1 = $("#user1").val();
            // console.log(url);
            var parameters = new FormData();
            parameters.append('action', 'delete');
            parameters.append('id', data.id);
            parameters.append('user1', user1);
            submit_with_ajax(window.location.pathname, 'Notification', '¿Estas seguro de realizar la siguiente acción?', parameters, function () {
                // location.href = '{{ list_url }}';
                // location.reload();
                //Oculta el modal
                // $('#myModalCategoria').modal('hide');
                // getData();
                tblMedida.ajax.reload();
            });

            // $('input[name="action"]').val('edit');
            // $('input[name="user1"]').val(1);
            // $('input[name="catDescripcion"]').val(data.catDescripcion);
            // $('input[name="id"]').val(data.id);

            //abro el modal
            // $('#myModalCategoria').modal('show');
            // console.log(data);


        });


    $('#form_ID').on('submit', function (e) {
        e.preventDefault();
        // console.log('hola');
        var parameters = new FormData(this);
        submit_with_ajax(window.location.pathname, 'Notification', '¿Estas seguro de realizar la siguiente acción?', parameters, function () {
            // location.href = '{{ list_url }}';
            // location.reload();
            //Oculta el modal
            $('#myModalMedida').modal('hide');
            // getData();
            tblMedida.ajax.reload();
        });


    });


});


//Antiguo para cargar datos

// $(function () {
//     $('#table_id').DataTable({
//         responsive: true,
//         autoWidth: false,
//         destroy: true,
//         deferRender: true,
//         paging: true,
//         // {#Bolo#}
//         ordering: true,
//         info: true,
//         pageLength: 5,
//         searching: true,
//         responsive: false,
//         // {#lenguaje#}
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
//         ajax: {
//             url: window.location.pathname,
//             type: 'POST',
//             data: {
//                 'action': 'searchdata'
//             },
//             dataSrc: ""
//         },
//         columns: [
//             {"data": "id"},
//             {"data": "catDescripcion"},
//             {"data": "catDescripcion"},
//             // {"data": "desc"},
//         ],
//         columnDefs: [
//             {
//                 targets: [-1],
//                 class: 'text-center',
//                 orderable: false,
//                 render: function (data, type, row) {
//                     var buttons = '<a href="/insumo/categoria/editar/' + row.id + '/" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
//                     buttons += '<a href="/insumo/categoria/eliminar/' + row.id + '/" type="button" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a>';
//                     return buttons;
//                 }
//             },
//         ],
//         initComplete: function (settings, json) {
//
//         }
//     });
//
//
//
// });