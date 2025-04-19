// some scripts

// jquery ready start
$(document).ready(function () {
    // jQuery code


    /* ///////////////////////////////////////

    THESE FOLLOWING SCRIPTS ONLY FOR BASIC USAGE, 
    For sliders, interactions and other

    */ ///////////////////////////////////////


    //////////////////////// Prevent closing from click inside dropdown
    $(document).on('click', '.dropdown-menu', function (e) {
        e.stopPropagation();
    });


    $('.js-check :radio').change(function () {
        var check_attr_name = $(this).attr('name');
        if ($(this).is(':checked')) {
            $('input[name=' + check_attr_name + ']').closest('.js-check').removeClass('active');
            $(this).closest('.js-check').addClass('active');
            // item.find('.radio').find('span').text('Add');

        } else {
            item.removeClass('active');
            // item.find('.radio').find('span').text('Unselect');
        }
    });


    $('.js-check :checkbox').change(function () {
        var check_attr_name = $(this).attr('name');
        if ($(this).is(':checked')) {
            $(this).closest('.js-check').addClass('active');
            // item.find('.radio').find('span').text('Add');
        } else {
            $(this).closest('.js-check').removeClass('active');
            // item.find('.radio').find('span').text('Unselect');
        }
    });



    //////////////////////// Bootstrap tooltip
    if ($('[data-toggle="tooltip"]').length > 0) {  // check if element exists
        $('[data-toggle="tooltip"]').tooltip()
    } // end if


    setTimeout(function () {
        // Closing the alert after 5 seconds
        $('#alert').alert('close'); // call the Bootstrap's alert('close') method to dismiss it.
    }, 5000);
    
    
    $('.plus-cart').click(function() { 
        let product_id = $(this).attr("data-product_id");
        let cart_id = $(this).attr("data-cart_id");
        let quantityElement = $(this).closest('.input-group-append').prev('.quantity');
        let row = this.closest('tr');
        let priceElement = row.querySelector('.price');
        let minusBtn = $(this).closest('.input-group').find('.minus-cart');

        $.ajax({
            type: "GET",
            url: "plus-cart/",
            data: {
                "product_id": product_id,
                "cart_id": cart_id,
            },
            success: function (response) {
                quantityElement.text(response.quantity);
                if (response.disabled === "false") {
                    minusBtn.removeClass('disabled');
                    minusBtn.addClass('enabled');
                }
                priceElement.innerText = (response.total_price).toFixed(1);
                document.getElementById('total-amount').innerText = (response.total_amount).toFixed(1); 
                document.getElementById('grand-total').innerText = (response.grand_total).toFixed(1);
            }
        });
    });

    $('.minus-cart').click(function() { 
        let product_id = $(this).attr("data-product_id");
        let cart_id = $(this).attr("data-cart_id");
        let quantityElement = $(this).closest('.input-group-prepend').next('.quantity');
        let row = this.closest('tr');
        let priceElement = row.querySelector('.price');
        let elem = this;

        $.ajax({
            type: "GET",
            url: "minus-cart/",
            data: {
                "product_id": product_id,
                "cart_id": cart_id,
            },
            success: function (response) {
                quantityElement.text(response.quantity);
                if (response.disabled === "true") {
                    $(elem).removeClass('enabled');
                    $(elem).addClass('disabled');
                }
                priceElement.innerText = (response.total_price).toFixed(1);
                document.getElementById('total-amount').innerText = (response.total_amount).toFixed(1); 
                document.getElementById('grand-total').innerText = (response.grand_total).toFixed(1);
            }
        });
    });

    $('.remove-item').click(function() { 
        let product_id = $(this).attr("data-product_id");
        let cart_id = $(this).attr("data-cart_id");
        let elem = this; // get the reference of remove tag that is clicked

        $.ajax({
            type: "GET",
            url: "remove-cart-item/",
            data: {
                "product_id": product_id,
                "cart_id": cart_id,
            },
            success: function (response) {
                elem.parentElement.parentElement.remove();
                let tbody = document.querySelector('#cart-table tbody'); 
                if (tbody.childElementCount === 0) {
                    window.location.reload(); 
                }
                document.getElementById('total-amount').innerText = (response.total_amount).toFixed(1); 
                document.getElementById('grand-total').innerText = (response.grand_total).toFixed(1);
            }
        });
    });

});


