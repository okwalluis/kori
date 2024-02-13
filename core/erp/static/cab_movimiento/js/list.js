var tblSale;

function format(d) {
    console.log('xxx1');
    console.log(d);
    var html = '<table class="table">';
    html += '<thead class="thead-dark">';
    html += '<tr><th scope="col">Productos</th>';
    html += '<th scope="col">Categoría</th>';
    html += '<th scope="col">Unidad medida</th>';
    html += '<th scope="col">Cantidad</th>';
    html += '<th scope="col">Costo</th></tr>';
    html += '</thead>';
    html += '<tbody>';
    d.forEach(function (item) {
        console.log('item xxx0');
        console.log(item);
        html+='<tr>'
        //html+='<td>'+item.producto.descripcion+'</td>'
        html+='<td>'+item.descripcion+'</td>'
        html+='<td>'+item.categoria+'</td>'
        //html+='<td>'+item.unidad_medida_sigla+'</td>'
        html+='<td>'+item.unidad_medida.sigla+'</td>'
        html+='<td>'+item.cantidad+'</td>'
        html+='<td>'+item.costo_mmnn+'</td>'
        html+='</tr>';
    });
    html += '</tbody>';
    return html;
}
$(function () {
    
    tblSale = $('#data').DataTable({
        //responsive: true,
        scrollX: true,
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
            {
                "className": 'details-control',
                "orderable": false,
                "data": null,
                "defaultContent": ''
            },
            {"data": "tipo_operacion.descripcion"},
            {"data": "numero"},
            {"data": "fecha"},
            {"data": "deposito.descripcion"},
            {"data": "id"},
        ],
        columnDefs: [
            /*
            {
                targets: [-2, -3, -4],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    return '$' + parseFloat(data).toFixed(2);
                }
            },
            */
            {   
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<a href="/erp/cab_movimiento/delete/' + row.id + '/" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a> ';
                    buttons += '<a href="/erp/cab_movimiento/update/' + row.id + '/" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
                    buttons += '<a rel="details" class="btn btn-success btn-xs btn-flat"><i class="fas fa-search"></i></a> ';
                    //buttons += '<a href="/erp/cab-movimiento/invoice/pdf/'+row.id+'/" target="_blank" class="btn btn-info btn-xs btn-flat"><i class="fas fa-file-pdf"></i></a> ';
                    return buttons;
                }
            },
        ],
        initComplete: function (settings, json) {

        }
    });

    $('#data tbody')
        .on('click', 'a[rel="details"]', function () {
            console.log('xxx3');
            var tr = tblSale.cell($(this).closest('td, li')).index();
            var data = tblSale.row(tr.row).data();
            console.log(data);

            $('#tblDet').DataTable({
                responsive: true,
                autoWidth: false,
                destroy: true,
                deferRender: true,
                //data: data.det,
                ajax: {
                    url: window.location.pathname,
                    type: 'POST',
                    data: {
                        'action': 'search_details_prod',
                        'id': data.id
                    },
                    dataSrc: ""
                },
                // No tocar, al listar detalle funciona
                columns: [
                    {"data": "producto.descripcion"},
                    {"data": "producto.categoria"},
                    {"data": "unidad_medida.sigla"},
                    {"data": "cantidad"},
                    {"data": "costo_mmnn"},
                ],
                columnDefs: [
                    {
                        targets: [-1],
                        class: 'text-center',
                        render: function (data, type, row) {
                            return '$' + parseFloat(data).toFixed(2);
                        }
                    },
                    /*
                    {
                        targets: [-3],
                        class: 'text-center',
                        render: function (data, type, row) {
                            return data;
                        }
                    },
                    */
                ],
                initComplete: function (settings, json) {

                }
            });

            $('#myModelDet').modal('show');
        })
        .on('click', 'td.details-control', function () {
            var tr = $(this).closest('tr');
            var row = tblSale.row(tr);
            if (row.child.isShown()) {
                row.child.hide();
                tr.removeClass('shown');
            } else {
                row.child(format(row.data())).show();
                tr.addClass('shown');
            }
        });
});
