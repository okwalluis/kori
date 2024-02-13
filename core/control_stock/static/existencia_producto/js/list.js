$(function () {
    $('#data').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: {
                'action': 'searchdata'
            },
            dataSrc: ""
        },
        columns: [
            {"data": "deposito"},
            {"data": "producto"},
            {"data": "saldo"},
        ],
        
        columnDefs: [
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<a href="/control_stock/existencia_producto/list/' + row.id + '/" class="btn btn-primary btn-xs btn-flat"><i class="fas fa-searchengin"></i></a> ';
                    //buttons += '<a href="/control_stock/lote/delete/' + row.id + '/" type="button" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a>';
                    return buttons;
                }
            },
        ],
        
        initComplete: function (settings, json) {

        }
    });
});