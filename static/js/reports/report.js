var date_range = null;
var datos;
var table;
var name = 'hola';
var date_now = new moment().format('YYYY-MM-DD');

function generate_report() {
    var parameters = {
        'action': 'search_report',
        // 'start_date': '2020-10-12',
        'start_date': date_now,
        'end_date': date_now,
    };

    if (date_range !== null) {
        parameters['start_date'] = date_range.startDate.format('YYYY-MM-DD');
        parameters['end_date'] = date_range.endDate.format('YYYY-MM-DD');
    }

    table = $('#datatable-buttons').DataTable({
        // dom:'b',
        dom: 'Bfrtip',
        // responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        // paging: true,
        // {#Bolo#}
        // ordering: true,
        // info: true,
        pageLength: 5,
        // searching: true,
        responsive: false,
        // {#lenguaje#}

        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: parameters,
            dataSrc: "",
            // success: function(data) {
            // datos=data;
            // return data;
            // },
        },
        // order: false,
        paging: false,
        ordering: false,
        info: false,
        searching: false,
        buttons: [
            // 'copy', 'excel', 'pdf',
            {
                extend: 'excelHtml5',
                text: 'Descargar Excel <i class="fas fa-file-excel"></i>',
                titleAttr: 'Excel',
                className: 'btn btn-success btn-flat btn-xs'
            },
            {
                extend: 'pdfHtml5',
                text: 'Descargar Pdf <i class="fas fa-file-pdf"></i>',
                titleAttr: 'PDF',
                className: 'btn btn-danger btn-flat btn-xs',
                download: 'open',
                orientation: 'landscape',
                pageSize: 'LEGAL',
                customize: function (doc) {
                    doc.styles = {
                        header: {
                            fontSize: 18,
                            bold: true,
                            alignment: 'center'
                        },
                        subheader: {
                            fontSize: 13,
                            bold: true
                        },
                        quote: {
                            italics: true
                        },
                        small: {
                            fontSize: 8
                        },
                        tableHeader: {
                            bold: true,
                            fontSize: 11,
                            color: 'white',
                            fillColor: '#2d4154',
                            alignment: 'center'
                        }
                    };
                    doc.content[1].table.widths = ['20%', '20%', '15%', '15%', '15%', '15%'];
                    doc.content[1].margin = [0, 35, 0, 0];
                    doc.content[1].layout = {};
                    doc['footer'] = (function (page, pages) {
                        return {
                            columns: [
                                {
                                    alignment: 'left',
                                    text: ['Fecha de creación: ', {text: date_now}]
                                },
                                {
                                    alignment: 'right',
                                    text: ['página ', {text: page.toString()}, ' de ', {text: pages.toString()}]
                                }
                            ],
                            margin: 20
                        }
                    });

                }
            }
        ],
        // columns: [
        //     {"data": "id"},
        //     {"data": "proveedor.proEmpresa"},
        //     {"data": "ccoFecCom"},
        //     // {"data": "categoria.catDescripcion"},
        //     {"data": "ccoSubtotal"},
        //     {"data": "ccoIva"},
        //
        //     {"data": "ccoTotal"},
        //     {"data": "ccoTotal"},
        //
        // ],
        columnDefs: [

            {
                targets: [-1, -2, -3],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    return '$' + parseFloat(data).toFixed(2);
                }
            },

        ],
        // rowCallback(row, data, displayNum, displayIndex, dataIndex) {
        //
        //     datos=row;
        //
        // },
        initComplete: function (settings, json) {

        }
    });

    // table .buttons().container()
    // .appendTo( $('btn btn-success', table.table().container() ) );
}

$(function () {
    // alert("x");
    $('input[name="date_range"]').daterangepicker({
        locale: {
            format: 'YYYY-MM-DD',
            applyLabel: '<i class="fas fa-chart-pie"></i> Aplicar',
            cancelLabel: '<i class="fas fa-times"></i> Cancelar',
        }
    }).on('apply.daterangepicker', function (ev, picker) {
        date_range = picker;

        // $('input[name="hola"]').val(table.data.id);
        generate_report();
        console.log(datos);
    }).on('cancel.daterangepicker', function (ev, picker) {
        $(this).data('daterangepicker').setStartDate(date_now);
        $(this).data('daterangepicker').setEndDate(date_now);
        date_range = picker;
        generate_report();
    });

    generate_report();

})