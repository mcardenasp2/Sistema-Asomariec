$(function () {
    $('#table_id').DataTable({
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
            {"data": "proEmpresa"},
            {"data": "proRuc"},
            {"data": "proEmail"},
            {"data": "provincia.prvDescripcion"},
            {"data": "proEmpresa"},
            // {"data": "desc"},
        ],
        columnDefs: [
            {
                targets: [0,1,2,3,4],
                class: 'text-center'
            },
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<a title="Editar" href="/proveedor/proveedor/editar/' + row.id + '/" class="btn btn-warning btn-sm btn-flat"><i class="fas fa-edit"></i></a> ';
                    buttons += '<a title="Eliminar" href="/proveedor/proveedor/eliminar/' + row.id + '/" type="button" class="btn btn-danger btn-sm btn-flat"><i class="fas fa-trash-alt"></i></a>';
                    return buttons;
                }
            },
        ],
        initComplete: function (settings, json) {

        }
    });
});