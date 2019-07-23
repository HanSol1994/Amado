/**
 * Created by Haniyeh on 6/25/18.
 */

$(document).ready(function () {
    
    $(':input[type=number]').on('wheel',function(e){ $(this).blur(); });

    
    $('form').on('focus', 'input[type=number]', function (e) {
      $(this).on('mousewheel.disableScroll', function (e) {
        e.preventDefault()
      })
    })
    $('form').on('blur', 'input[type=number]', function (e) {
      $(this).off('mousewheel.disableScroll')
    })

    // count()


    // $(document).click(function () {
    //     count()
    // })

    // $('body').keypress(function () {
    //     count()
    // })

    // function count() {
    //     sum = 0
    //     $('.tabular .field-cost input').each(function (index,element) {

    //         // sum += parseInt($(element).val()

    //         s = parseInt($(element).val())
    //         if (s){
    //             sum += s
    //     }
    //     // console.log(element)

    //     })
    //     cash = 0
    //     cash = parseInt($("#id_sales_cash_cost").val())

    //     tot = 0
    //     tot = parseInt($("#id_sales_tot_cash_cost").val())

    //     $("#tot_fill").html(addCommas((cash+sum)+''))
    //     $("#balance_fill").html(addCommas(((cash+sum)-tot)+''))
    // }

    // function addCommas(nStr) {

    //     nStr += '';
    //     var x = nStr.split('.');
    //     var x1 = x[0];
    //     var x2 = x.length > 1 ? '.' + x[1] : '';
    //     var rgx = /(\d+)(\d{3})/;
    //     while (rgx.test(x1)) {
    //         x1 = x1.replace(rgx, '$1' + ',' + '$2');
    //     }
    //     x = x1 + x2;

    //     if (x=='NaN')
    //         return ''

    //     return x+' ریال'
    // }

})
