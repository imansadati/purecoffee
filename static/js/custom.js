(function ($) {
    "use strict";
    var Ayurveda = {
        initialised: false,
        version: 1.0,
        Solar: false,
        init: function () {

            if (!this.initialised) {
                this.initialised = true;
            } else {
                return;
            }

            // Functions Calling

            this.loader();
            this.product_slider();
            this.related_slider();
            this.tesimonial_slider();
            this.counter();
            this.quantity();
            this.menu();
            this.menu_toggle();
        },
        // preloader
        loader: function () {
            jQuery(window).on("load", function () {
                jQuery(".pa-ellipsis").fadeOut(), jQuery(".pa-preloader").delay(200).fadeOut("slow")
            });
        },
        // product sider
        product_slider: function () {
            var swiper = new Swiper('.pa-trending-product .swiper-container', {
                slidesPerView: 3,
                loop: true,
                spaceBetween: 0,
                speed: 1500,
                autoplay: true,
                navigation: {
                    nextEl: '.swiper-button-next',
                    prevEl: '.swiper-button-prev',
                },
                breakpoints: {
                    575: {
                        slidesPerView: 1,
                        spaceBetween: 0,
                    },
                    767: {
                        slidesPerView: 2,
                        spaceBetween: 0,
                    },
                    992: {
                        slidesPerView: 2,
                        spaceBetween: 0,
                    },
                }
            });
        },
        // related sider
        related_slider: function () {
            var swiper = new Swiper('.pa-related-product .swiper-container', {
                slidesPerView: 2,
                loop: true,
                spaceBetween: 0,
                speed: 1500,
                autoplay: true,
                navigation: {
                    nextEl: '.swiper-button-next',
                    prevEl: '.swiper-button-prev',
                },
                breakpoints: {
                    575: {
                        slidesPerView: 1,
                        spaceBetween: 0,
                    },
                    767: {
                        slidesPerView: 2,
                        spaceBetween: 0,
                    },
                    992: {
                        slidesPerView: 2,
                        spaceBetween: 0,
                    },
                }
            });
        },
        // testimonial sider
        tesimonial_slider: function () {
            var swiper = new Swiper('.pa-tesimonial .swiper-container', {
                slidesPerView: 1,
                loop: true,
                spaceBetween: 0,
                speed: 1500,
                autoplay: true,
                navigation: {
                    nextEl: '.swiper-button-next',
                    prevEl: '.swiper-button-prev',
                },
            });
        },
        // counter start
        counter: function () {
            if ($('.pa-counter-main').length > 0) {
                var a = 0;
                $(window).scroll(function () {

                    var oTop = $('#counter').offset().top - window.innerHeight;
                    if (a == 0 && $(window).scrollTop() > oTop) {
                        $('.counter-value').each(function () {
                            var $this = $(this),
                                countTo = $this.attr('data-count');
                            $({
                                countNum: $this.text()
                            }).animate({
                                    countNum: countTo
                                },
                                {
                                    duration: 5000,
                                    easing: 'swing',
                                    step: function () {
                                        $this.text(Math.floor(this.countNum));
                                    },
                                    complete: function () {
                                        $this.text(this.countNum);
                                    }
                                });
                        });
                        a = 1;
                    }
                });
            }
            ;
        },
        // quantity
        quantity: function () {
            $('#pa-add').click(function () {
                if ($(this).prev().val() < 50000) {
                    $(this).prev().val(+$(this).prev().val() + 1);
                }
            });
            $('.pa-sub').click(function () {
                if ($(this).next().val() > 1) {
                    if ($(this).next().val() > 1) $(this).next().val(+$(this).next().val() - 1);
                }
            });
        },
        // mobile menu
        menu: function () {
            if ($('.pa-toggle-nav').length > 0) {
                $(".pa-toggle-nav").on('click', function (e) {
                    event.stopPropagation();
                    $(".pa-nav-bar").toggleClass("pa-open-menu");
                });
                $("body").on('click', function () {
                    $(".pa-nav-bar").removeClass("pa-open-menu");
                });
                $(".pa-menu").on('click', function () {
                    event.stopPropagation();
                });
            }
            ;
        },
        menu_toggle: function () {
            // menu two
            $(".pa-menu-tow-child").on('click', function () {
                $(this).find(".pa-submenu-two").slideToggle();
            });
            // menu two stop propagation
            $(".pa-submenu-two").on('click', function () {
                event.stopPropagation();
            });
            // toggle two
            $(".pa-toggle-nav2").on('click', function (e) {
                event.stopPropagation();
                $(".pa-header-two").toggleClass("pa-open-menu");
            });
            // toggle
            $(".pa-menu-child").on('click', function (e) {
                event.stopPropagation();
                $(this).find(".pa-submenu").slideToggle();
            });
        },
    };
    Ayurveda.init();

})(jQuery);


// handmade JS

// login / signup form
const inputs = document.querySelectorAll('.input');

function focusFunc() {
    let parent = this.parentNode.parentNode;
    parent.classList.add('focus');
}

function blurFunc() {
    let parent = this.parentNode.parentNode;
    if (this.value == "") {
        parent.classList.remove('focus');
    }
}

inputs.forEach(input => {
    input.addEventListener('focus', focusFunc);
    input.addEventListener('blur', blurFunc);
});

// show the first selected color

// $(".choose-color").first().addClass('focused');
// var _color = $(".choose-color").first().attr('data-color');
// $(".color" + _color).show();
// $(".color" + _color).first().addClass('active');

$('.choose-color').on('click', function () {
    $(".choose-color").removeClass('border-3');
    $(this).addClass('border-3');
})

$('.choose-color').click(function () {
    var buttonText = $(this).attr('data-color');
    $('#color-id').val(buttonText);
})

$('.choose-grind').on('click', function () {
    $(".choose-grind").removeClass('border-3');
    $(this).addClass('border-3');
})

$('.choose-grind').click(function () {
    var buttonText = $(this).attr('value');
    $('#grind-id').val(buttonText);
})


// add product to order

$(document).on('click', '.add-to-cart', function () {
    const _vm = $(this);
    const _index = _vm.attr('data-index');
    const _count = $('#product-count').val();
    const _productId = $(".product-id-" + _index).val();
    const _color = $("#color-id").val();
    const _grind = $("#grind-id").val();

    if (_grind === '') {
        $.ajax({
            url: '/order/add-to-order/',
            data: {
                'id': _productId,
                'count': _count,
                'color': _color,
            },
            dataType: 'json',
            success: function (res) {
                Swal.fire({
                    title: 'اعلان',
                    text: res.text,
                    icon: res.icon,
                    showCancelButton: false,
                    confirmButtonColor: '#3085d6',
                    confirmButtonText: res.confirm_button_text
                }).then((result) => {
                    if (result.isConfirmed && res.status === 'not_auth') {
                        window.location.href = '/login';
                    }
                })
            }
        })
    } else {
        $.ajax({
            url: '/order/add-to-order/',
            data: {
                'id': _productId,
                'count': _count,
                'color': _color,
                'grind': _grind,
            },
            dataType: 'json',
            success: function (res) {
                Swal.fire({
                    title: 'اعلان',
                    text: res.text,
                    icon: res.icon,
                    showCancelButton: false,
                    confirmButtonColor: '#3085d6',
                    confirmButtonText: res.confirm_button_text,
                }).then((result) => {
                    if (result.isConfirmed && res.status === 'not_auth') {
                        window.location.href = '/login';
                    }
                })
            }
        })
    }
});

// function addProductToOrder(productId) {
//     const productCount = $('#product-count').val();
//     const productColor = $('#product-color').val();
//     const productGrind = $('#product-grind').val();
//     $.get('/order/add-to-order?product_id=' + productId + '&count=' + productCount + '&color=' + productColor + '&grind=' + productGrind)
//         .then(res => {
//             Swal.fire({
//                 title: 'اعلان',
//                 text: res.text,
//                 icon: res.icon,
//                 showCancelButton: false,
//                 confirmButtonColor: '#3085d6',
//                 confirmButtonText: res.confirm_button_text
//             }).then((result) => {
//                 if (result.isConfirmed && res.status === 'not_auth') {
//                     window.location.href = '/login';
//                 }
//             })
//         });
// }

function changeOrderDetailCount(detailId, state, color) {
    $.get('/user/change-order-detail?detail_id=' + detailId + '&state=' + state + '&color=' + color).then(res => {
        if (res.status === 'success') {
            $('#order-detail-content').html(res.body);
        }
        if (res.status === 'product_finished') {
            Swal.fire({
                title: 'اعلان',
                text: res.text,
                icon: res.icon,
                showCancelButton: false,
                confirmButtonColor: '#3085d6',
                confirmButtonText: res.confirm_button_text
            })
        }
    });
}

function removeOrderDetail(detailId) {
    $.get('/user/remove-order-detail?detail_id=' + detailId).then(res => {
        if (res.status === 'success') {
            $('#order-detail-content').html(res.body);
        }
    })
}


// $(document).ready(function() {
//     // Fetch product counts and update the UI
//     $.ajax({
//         url: '/user/show-basket-count',
//         dataType: 'json',
//         success: function(data) {
//             const productCounts = data.product_counts;
//             // Loop through product counts and update the UI
//             for (const productId in productCounts) {
//                 if (productCounts.hasOwnProperty(productId)) {
//                     const count = productCounts[productId];
//                     // Update the UI with the count for each product (you can use product IDs to identify elements)
//                     // For example, you can use jQuery selectors to find and update elements.
//                     $(`#product-count-${productId}`).text(count);
//                 }
//             }
//         }
//     });
// });

// updateBasketCount();

// function updateProductCount() {
//     var basketCountElement = document.getElementById('products-count');
//     if (basketCountElement) {
//         var currentCount = parseInt(basketCountElement.innerText) || 0;
//         var newCount = currentCount + 1;
//         basketCountElement.innerText = newCount;
//         localStorage.setItem('productCount', newCount.toString());
//     }
// }
//
// window.addEventListener('load', function () {
//     var basketCountElement = document.getElementById('products-count');
//     if (basketCountElement) {
//         var storedCount = localStorage.getItem('productCount');
//         if (storedCount) {
//             basketCountElement.innerText = parseInt(storedCount) || 0;
//         }
//     }
// });

