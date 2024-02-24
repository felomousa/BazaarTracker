// script.js content
$(document).ready(function () {
    // Initialize the DataTable
    var table = $('#pricesTable').DataTable({
        "paging": false,
        "lengthChange": false,
        "order": [[6, "desc"]],
        // Add any other DataTable configurations you might have
    });

    // Toggle visibility of columns
    $('.toggle-button').on('click', function () {
        var column = table.column($(this).attr('data-column'));
        column.visible(!column.visible());
        $(this).toggleClass('active');
    });

    // Refresh button functionality
    $('#refreshButton').on('click', function () {
        $(this).addClass('disabled');
        $.get('/refresh_prices', function (data) {
            if (data.success) {
                $('.last-updated').text('Last Updated: ' + data.last_updated);
                table.clear();
                for (var item_id in data.prices_data) {
                    if (data.prices_data.hasOwnProperty(item_id)) {
                        var product = data.prices_data[item_id];
                        table.row.add([
                            product.product_id || 'N/A',
                            formatNumber(product.first_buy_price),
                            formatNumber(product.first_sell_price),
                            formatNumber(product.first_buy_price - product.first_sell_price),
                            formatInteger(product.quick_status.buyMovingWeek),
                            formatInteger(product.quick_status.sellMovingWeek),
                            formatNumber(product.points)
                        ]);
                    }
                }
                table.draw();
            }
        }).always(function () {
            setTimeout(function () {
                $('#refreshButton').removeClass('disabled');
            }, 5000);
        });
    });

    // Change search input background color based on text input
    table.on('search.dt', function () {
        $('.dataTables_filter input').css('background-color', table.search() === '' ? 'transparent' : 'transparent');
    });

    // Number formatting functions
    function formatNumber(value, decimals = 2) {
        if (isNaN(value)) {
            return value;
        }
        return value.toFixed(decimals).replace(/\d(?=(\d{3})+\.)/g, '$&,');
    }

    function formatInteger(value) {
        return formatNumber(value, 0);
    }
});
