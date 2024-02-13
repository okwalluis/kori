var tblProducts;
var vents = {
    items: {
        tipo_operacion: '',
        fecha: '',
        numero: '',
        deposito: '',
        observacion: '',
        products: []
    },

    add: function (item) {
        this.items.products.push(item);
        console.log('yyy1');
        console.log(this.items.products);
        this.list();
    },

    list: function () {
        //this.calculate_invoice();

        /*
        */
        console.log('yyy2');
        console.log( this.items.products);

        tblProducts = $('#tblProducts').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            data: this.items.products,
            // No tocal, al editar funciona bien.
            columns: [
                {"data": "id"},
                {"data": "producto.descripcion"},
                {"data": "producto.categoria"},
                {"data": "unidad_medida.sigla"},
                {"data": "cantidad"},
                {"data": "costo_mmnn"},
            ],
            columnDefs: [
                {
                    targets: [0],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<a rel="remove" class="btn btn-danger btn-xs btn-flat" style="color: white;"><i class="fas fa-trash-alt"></i></a>';
                    }
                },
                {
                    targets: [-2],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<input type="text" name="cantidad" class="form-control form-control-sm input-sm" autocomplete="off" value="' + row.cantidad + '">';
                    }
                },
                {
                    targets: [-1],  // Índice de la columna que contiene el campo DecimalField
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        // Suponiendo que "data" es el valor del campo DecimalField en este caso
                        var formattedValue = parseFloat(data).toFixed(2);  // Formatea el valor a dos decimales
                        return 'Gs ' + formattedValue;  // Agrega el símbolo de la moneda antes del valor
                    }
                }
            ],
            rowCallback(row, data, displayNum, displayIndex, dataIndex) {

                $(row).find('input[name="cantidad"]').TouchSpin({
                    min: 1,
                    max: 100000,
                    step: 1
                });

            },
            initComplete: function (settings, json) {
            }
        });
        $('.unidad_medida').change(function() {
            var selectedOption = $(this).val(); // Obtiene la opción seleccionada
            //var selectedOption = $('select[name="unidad_medida"]').val();
            // Carga las opciones del select de acuerdo a la unidad de medida seleccionada
            // Aquí debes implementar la lógica para cargar las opciones del select
            // Puedes hacer una solicitud AJAX al servidor para obtener las opciones según la unidad de medida
        });
        //console.clear();
        //console.log(this.items);
    },
};



function formatRepo(repo) {
    if (repo.loading) {
        return repo.text;
    }
    
    //console.log(repo);
    console.log('yyy3');
    var option = $(
        
        '<div class="wrapper container">'+
        '<div class="row">' +
        //'<div class="col-lg-1">' +
        //'<img src="' + repo.imagen + '" class="img-fluid img-thumbnail d-block mx-auto rounded">' +
        //'</div>' +
        '<div class="col-lg-11 text-left shadow-sm">' +
        //'<br>' +
        '<p style="margin-bottom: 0;">' +
        '<b>ID:</b> ' + repo.id + '<br>' +
        '<b>Descripción:</b> ' + repo.descripcion + '<br>' +
        '<b>Categoría:</b> ' + repo.categoria + '<br>' +
        '<b>Unidad de medida:</b> ' + repo.unidad_medida_sigla + '<br>' +
        '</p>' +
        '</div>' +
        '</div>' +
        '</div>');
    return option;
};

$(function () {
    console.log('yyy4');
    $('.select2').select2({
        theme: "bootstrap4",
        language: 'es'
    });
    $('#fecha').datetimepicker({
        format: 'YYYY-MM-DD',
        date: moment().format("YYYY-MM-DD"),
        locale: 'es',
        //minDate: moment().format("YYYY-MM-DD")
    });
    $('.btnRemoveAll').on('click', function () {
        if (vents.items.products.length === 0) return false;
        alert_action('Notificación', '¿Estas seguro de eliminar todos los items de tu detalle?', function () {
            vents.items.products = [];
            vents.list();
        }, function () {
        });
    });
    // event cant
    $('#tblProducts tbody')
        .on('click', 'a[rel="remove"]', function () {
            var tr = tblProducts.cell($(this).closest('td, li')).index();
            alert_action('Notificación', '¿Estas seguro de eliminar el producto de tu detalle?',
                function () {
                    vents.items.products.splice(tr.row, 1);
                    vents.list();
                }, function () {

                });
        })
        .on('change', 'input[name="cantidad"]', function () {
            console.clear();
            var cantidad = parseInt($(this).val());
            var tr = tblProducts.cell($(this).closest('td, li')).index();
            vents.items.products[tr.row].cantidad = cantidad;
            //$('td:eq(5)', tblProducts.row(tr.row).node()).html('$' + vents.items.products[tr.row].subtotal.toFixed(2));
        });

    $('.btnClearSearch').on('click', function () {
        $('input[name="search"]').val('').focus();
    });

    // event submit
    $('form').on('submit', function (e) {
        e.preventDefault();

        if (vents.items.products.length === 0) {
            message_error('Debe al menos tener un item en su detalle');
            return false;
        }

        vents.items.fecha = $('input[name="fecha"]').val();
        vents.items.numero = $('input[name="numero"]').val();
        vents.items.tipo_operacion = $('select[name="tipo_operacion"]').val();
        vents.items.deposito = $('select[name="deposito"]').val();
        vents.items.observacion = $('input[name="observacion"]').val();

        var parameters = new FormData();
        parameters.append('action', $('input[name="action"]').val());
        parameters.append('vents', JSON.stringify(vents.items));
        submit_with_ajax(window.location.pathname, 'Notificación',
            '¿Estas seguro de realizar la siguiente acción?', parameters, function (response) {    
                    location.href = '/erp/cab_movimiento/list/';
                });
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
                var queryParameters = {
                    term: params.term,
                    action: 'search_products'
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
        templateResult: formatRepo,
    }).on('select2:select', function (e) {
        var data = e.params.data;
        data.cantidad = 1;
        //data.subtotal = 0.00;
        vents.add(data);
        
        $(this).val('').trigger('change.select2');
    });

    // Esto se puso aqui para que funcione bien el editar y calcule bien los valores del iva. // sino tomaría el valor del iva de la base debe
    // coger el que pusimos al inicializarlo.
    vents.list();
});    