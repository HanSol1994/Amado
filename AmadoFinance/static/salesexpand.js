/**
 * Created by Haniyeh on 6/25/18.
 */

function removecomma(str) {
    str = str.replace(',','')
    str = str.replace(',','')
    str = str.replace(',','')
    str = str.replace(',','')
    str = str.replace(',','')
    str = str.replace(',','')
    return str
}

function addCommas(nStr) {

        nStr += '';
        var x = nStr.split('.');
        var x1 = x[0];
        var x2 = x.length > 1 ? '.' + x[1] : '';
        var rgx = /(\d+)(\d{3})/;
        while (rgx.test(x1)) {
            x1 = x1.replace(rgx, '$1' + ',' + '$2');
        }
        x = x1 + x2;

        if (x=='NaN')
            return ''

        return x
    }

function collapsedays(){

    dateTemp = ''
    var firstElem
    day = ''
    date = 0
    tot_cash = 0
    net = 0
    pos = 0
    tot_calc = 0
    tot_sales = 0
    balance = 0
    tot_fisch_salon = 0
    tot_salon = 0
    tot_fisch_del = 0
    tot_del = 0

    table = $("#result_list tbody")
    index = 1
    $("#result_list tbody tr").each(function (element) {
        $children = $(this).children()
        date = $children[3]


        if (dateTemp == '') {
            dateTemp = $(date).html()
            day = $($children[2]).html()
            firstElem = $(this)
        }


        if ($(date).html() != dateTemp ){

            $(firstElem).before(
                '<tr>' +
                    '<td style="text-align: center" class="action-checkbox text-center"><a href="#" class="expand_collapse" id="'+dateTemp+'"><i class="fas fa-plus-square"></i></a></td>' +
                    '<td style="text-align: center" class="field-id text-center">'+index+'</td>' +
                    '<td style="text-align: center" class="field-date text-center">'+day+'</td>' +
                    '<td style="text-align: center" class="field-sales_date text-center">'+dateTemp+'</td>' +

                    '<td style="text-align: center" class="field-sales_branch text-center">همه</td>' +
                    '<td style="text-align: center" class="field-sales_cash_cost text-center">'+addCommas(tot_cash)+'</td>' +
                    '<td style="text-align: center" class="field-tot_net text-center">'+addCommas(net)+'</td>' +
                    '<td style="text-align: center" class="field-tot_pos text-center">'+addCommas(pos)+'</td>' +
                    '<td style="text-align: center" class="field-tot text-center">'+addCommas(tot_calc)+'</td>' +
                    '<td style="text-align: center" class="field-sales_tot_cash_cost text-center">'+addCommas(tot_sales)+'</td>' +
                    '<td style="text-align: center" class="field-balance text-center">'+addCommas(balance)+'</td>' +
                    '<td style="text-align: center" class="field-tot_fish_salon text-center">'+addCommas(tot_fisch_salon)+'</td>' +
                    '<td style="text-align: center" class="field-tot_salon text-center">'+addCommas(tot_salon)+'</td>' +
                    '<td style="text-align: center" class="field-tot_fish_del text-center">'+addCommas(tot_fisch_del)+'</td>' +
                    '<td style="text-align: center" class="field-sales_delivery_cost text-center">'+addCommas(tot_del)+'</td>' +
                '</tr>')
            dateTemp = $(date).html()
            index++

            date = 0
            tot_cash = 0
            net = 0
            pos = 0
            tot_calc = 0
            tot_sales = 0
            balance = 0
            tot_fisch_salon = 0
            tot_salon = 0
            tot_fisch_del = 0
            tot_del = 0
            firstElem=$(this)
        }


        tot_cash += parseInt(removecomma($($children[5]).html()))
        net += parseInt(removecomma($($children[6]).html()))
        pos += parseInt(removecomma($($children[7]).html()))
        tot_calc += parseInt(removecomma($($children[8]).html()))
        tot_sales += parseInt(removecomma($($children[9]).html()))
        balance += parseInt(removecomma($($children[10]).html()))
        tot_fisch_salon += parseInt(removecomma($($children[11]).html()))
        tot_salon += parseInt(removecomma($($children[12]).html()))
        tot_fisch_del += parseInt(removecomma($($children[13]).html()))
        tot_del += parseInt(removecomma($($children[14]).html()))
        day = $($children[2]).html()

        $(this).hide()

    })
    $(firstElem).before(
        '<tr>' +
            '<td style="text-align: center" class="action-checkbox text-center"><a href="#" class="expand_collapse" id="'+dateTemp+'"><i class="fas fa-plus-square"></i></a></td>' +
            '<td style="text-align: center" class="field-id text-center">'+index+'</td>' +
            '<td style="text-align: center" class="field-date text-center">'+day+'</td>' +
            '<td style="text-align: center" class="field-sales_date text-center">'+dateTemp+'</td>' +
            '<td style="text-align: center" class="field-sales_branch text-center">همه</td>' +
            '<td style="text-align: center" class="field-sales_cash_cost text-center">'+addCommas(tot_cash)+'</td>' +
            '<td style="text-align: center" class="field-tot_net text-center">'+addCommas(net)+'</td>' +
            '<td style="text-align: center" class="field-tot_pos text-center">'+addCommas(pos)+'</td>' +
            '<td style="text-align: center" class="field-tot text-center">'+addCommas(tot_calc)+'</td>' +
            '<td style="text-align: center" class="field-sales_tot_cash_cost text-center">'+addCommas(tot_sales)+'</td>' +
            '<td style="text-align: center" class="field-balance text-center">'+addCommas(balance)+'</td>' +
            '<td style="text-align: center" class="field-tot_fish_salon text-center">'+addCommas(tot_fisch_salon)+'</td>' +
            '<td style="text-align: center" class="field-tot_salon text-center">'+addCommas(tot_salon)+'</td>' +
            '<td style="text-align: center" class="field-tot_fish_del text-center">'+addCommas(tot_fisch_del)+'</td>' +
            '<td style="text-align: center" class="field-sales_delivery_cost text-center">'+addCommas(tot_del)+'</td>' +
        '</tr>')

}

function collapsemonths(){

    dateTemp = ''
    var firstElem

    date = 0
    tot_cash = 0
    net = 0
    pos = 0
    tot_calc = 0
    tot_sales = 0
    balance = 0
    tot_fisch_salon = 0
    tot_salon = 0
    tot_fisch_del = 0
    tot_del = 0

    table = $("#result_list tbody")
    index = 1
    $("#result_list tbody tr").each(function (element) {
        $children = $(this).children()
        date = $children[3]


        if (dateTemp == '') {
            dateTemp = '*-'+$(date).html().split('-')[0]+"-"+$(date).html().split('-')[1]
            firstElem = $(this)
        }


        if ('*-'+$(date).html().split('-')[0]+"-"+$(date).html().split('-')[1] != dateTemp ){

            $(firstElem).before(
                '<tr>' +
                    '<td style="text-align: center" class="action-checkbox text-center"><a href="#" class="expand_collapse" id="'+dateTemp+'"><i class="fas fa-plus-square"></i></a></td>' +
                    '<td style="text-align: center" class="field-id text-center">'+index+'</td>' +
                    '<td style="text-align: center" class="field-date text-center">*</td>' +
                    '<td style="text-align: center" class="field-sales_date text-center">'+dateTemp+'</td>' +

                    '<td style="text-align: center" class="field-sales_branch text-center">همه</td>' +
                    '<td style="text-align: center" class="field-sales_cash_cost text-center">'+addCommas(tot_cash)+'</td>' +
                    '<td style="text-align: center" class="field-tot_net text-center">'+addCommas(net)+'</td>' +
                    '<td style="text-align: center" class="field-tot_pos text-center">'+addCommas(pos)+'</td>' +
                    '<td style="text-align: center" class="field-tot text-center">'+addCommas(tot_calc)+'</td>' +
                    '<td style="text-align: center" class="field-sales_tot_cash_cost text-center">'+addCommas(tot_sales)+'</td>' +
                    '<td style="text-align: center" class="field-balance text-center">'+addCommas(balance)+'</td>' +
                    '<td style="text-align: center" class="field-tot_fish_salon text-center">'+addCommas(tot_fisch_salon)+'</td>' +
                    '<td style="text-align: center" class="field-tot_salon text-center">'+addCommas(tot_salon)+'</td>' +
                    '<td style="text-align: center" class="field-tot_fish_del text-center">'+addCommas(tot_fisch_del)+'</td>' +
                    '<td style="text-align: center" class="field-sales_delivery_cost text-center">'+addCommas(tot_del)+'</td>' +
                '</tr>')
            dateTemp = '*-'+$(date).html().split('-')[0]+"-"+$(date).html().split('-')[1]
            index++

            date = 0
            tot_cash = 0
            net = 0
            pos = 0
            tot_calc = 0
            tot_sales = 0
            balance = 0
            tot_fisch_salon = 0
            tot_salon = 0
            tot_fisch_del = 0
            tot_del = 0
            firstElem=$(this)
        }


        tot_cash += parseInt(removecomma($($children[5]).html()))
        net += parseInt(removecomma($($children[6]).html()))
        pos += parseInt(removecomma($($children[7]).html()))
        tot_calc += parseInt(removecomma($($children[8]).html()))
        tot_sales += parseInt(removecomma($($children[9]).html()))
        balance += parseInt(removecomma($($children[10]).html()))
        tot_fisch_salon += parseInt(removecomma($($children[11]).html()))
        tot_salon += parseInt(removecomma($($children[12]).html()))
        tot_fisch_del += parseInt(removecomma($($children[13]).html()))
        tot_del += parseInt(removecomma($($children[14]).html()))
        day = $($children[2]).html()

        $(this).hide()

    })
    $(firstElem).before(
        '<tr>' +
            '<td style="text-align: center" class="action-checkbox text-center"><a href="#" class="expand_collapse" id="'+dateTemp+'"><i class="fas fa-plus-square"></i></a></td>' +
            '<td style="text-align: center" class="field-id text-center">'+index+'</td>' +
            '<td style="text-align: center" class="field-date text-center">*</td>' +
            '<td style="text-align: center" class="field-sales_date text-center">'+dateTemp+'</td>' +
            '<td style="text-align: center" class="field-sales_branch text-center">همه</td>' +
            '<td style="text-align: center" class="field-sales_cash_cost text-center">'+addCommas(tot_cash)+'</td>' +
            '<td style="text-align: center" class="field-tot_net text-center">'+addCommas(net)+'</td>' +
            '<td style="text-align: center" class="field-tot_pos text-center">'+addCommas(pos)+'</td>' +
            '<td style="text-align: center" class="field-tot text-center">'+addCommas(tot_calc)+'</td>' +
            '<td style="text-align: center" class="field-sales_tot_cash_cost text-center">'+addCommas(tot_sales)+'</td>' +
            '<td style="text-align: center" class="field-balance text-center">'+addCommas(balance)+'</td>' +
            '<td style="text-align: center" class="field-tot_fish_salon text-center">'+addCommas(tot_fisch_salon)+'</td>' +
            '<td style="text-align: center" class="field-tot_salon text-center">'+addCommas(tot_salon)+'</td>' +
            '<td style="text-align: center" class="field-tot_fish_del text-center">'+addCommas(tot_fisch_del)+'</td>' +
            '<td style="text-align: center" class="field-sales_delivery_cost text-center">'+addCommas(tot_del)+'</td>' +
        '</tr>')

}

function collapseyears(){

    dateTemp = ''
    var firstElem

    date = 0
    tot_cash = 0
    net = 0
    pos = 0
    tot_calc = 0
    tot_sales = 0
    balance = 0
    tot_fisch_salon = 0
    tot_salon = 0
    tot_fisch_del = 0
    tot_del = 0

    table = $("#result_list tbody")
    index = 1
    $("#result_list tbody tr").each(function (element) {
        $children = $(this).children()
        date = $children[3]


        if (dateTemp == '') {
            dateTemp = '*-*-'+$(date).html().split('-')[0]
            firstElem = $(this)
        }


        if ('*-*-'+$(date).html().split('-')[0] != dateTemp ){

            $(firstElem).before(
                '<tr>' +
                    '<td style="text-align: center" class="action-checkbox text-center"><a href="#" class="expand_collapse" id="'+dateTemp+'"><i class="fas fa-plus-square"></i></a></td>' +
                    '<td style="text-align: center" class="field-id text-center">'+index+'</td>' +
                    '<td style="text-align: center" class="field-date text-center">*</td>' +
                    '<td style="text-align: center" class="field-sales_date text-center">'+dateTemp+'</td>' +

                    '<td style="text-align: center" class="field-sales_branch text-center">همه</td>' +
                    '<td style="text-align: center" class="field-sales_cash_cost text-center">'+addCommas(tot_cash)+'</td>' +
                    '<td style="text-align: center" class="field-tot_net text-center">'+addCommas(net)+'</td>' +
                    '<td style="text-align: center" class="field-tot_pos text-center">'+addCommas(pos)+'</td>' +
                    '<td style="text-align: center" class="field-tot text-center">'+addCommas(tot_calc)+'</td>' +
                    '<td style="text-align: center" class="field-sales_tot_cash_cost text-center">'+addCommas(tot_sales)+'</td>' +
                    '<td style="text-align: center" class="field-balance text-center">'+addCommas(balance)+'</td>' +
                    '<td style="text-align: center" class="field-tot_fish_salon text-center">'+addCommas(tot_fisch_salon)+'</td>' +
                    '<td style="text-align: center" class="field-tot_salon text-center">'+addCommas(tot_salon)+'</td>' +
                    '<td style="text-align: center" class="field-tot_fish_del text-center">'+addCommas(tot_fisch_del)+'</td>' +
                    '<td style="text-align: center" class="field-sales_delivery_cost text-center">'+addCommas(tot_del)+'</td>' +
                '</tr>')
            dateTemp = '*-*-'+$(date).html().split('-')[0]
            index++

            date = 0
            tot_cash = 0
            net = 0
            pos = 0
            tot_calc = 0
            tot_sales = 0
            balance = 0
            tot_fisch_salon = 0
            tot_salon = 0
            tot_fisch_del = 0
            tot_del = 0
            firstElem=$(this)
        }


        tot_cash += parseInt(removecomma($($children[5]).html()))
        net += parseInt(removecomma($($children[6]).html()))
        pos += parseInt(removecomma($($children[7]).html()))
        tot_calc += parseInt(removecomma($($children[8]).html()))
        tot_sales += parseInt(removecomma($($children[9]).html()))
        balance += parseInt(removecomma($($children[10]).html()))
        tot_fisch_salon += parseInt(removecomma($($children[11]).html()))
        tot_salon += parseInt(removecomma($($children[12]).html()))
        tot_fisch_del += parseInt(removecomma($($children[13]).html()))
        tot_del += parseInt(removecomma($($children[14]).html()))
        day = $($children[2]).html()

        $(this).hide()

    })
    $(firstElem).before(
        '<tr>' +
            '<td style="text-align: center" class="action-checkbox text-center"><a href="#" class="expand_collapse" id="'+dateTemp+'"><i class="fas fa-plus-square"></i></a></td>' +
            '<td style="text-align: center" class="field-id text-center">'+index+'</td>' +
            '<td style="text-align: center" class="field-date text-center">*</td>' +
            '<td style="text-align: center" class="field-sales_date text-center">'+dateTemp+'</td>' +
            '<td style="text-align: center" class="field-sales_branch text-center">همه</td>' +
            '<td style="text-align: center" class="field-sales_cash_cost text-center">'+addCommas(tot_cash)+'</td>' +
            '<td style="text-align: center" class="field-tot_net text-center">'+addCommas(net)+'</td>' +
            '<td style="text-align: center" class="field-tot_pos text-center">'+addCommas(pos)+'</td>' +
            '<td style="text-align: center" class="field-tot text-center">'+addCommas(tot_calc)+'</td>' +
            '<td style="text-align: center" class="field-sales_tot_cash_cost text-center">'+addCommas(tot_sales)+'</td>' +
            '<td style="text-align: center" class="field-balance text-center">'+addCommas(balance)+'</td>' +
            '<td style="text-align: center" class="field-tot_fish_salon text-center">'+addCommas(tot_fisch_salon)+'</td>' +
            '<td style="text-align: center" class="field-tot_salon text-center">'+addCommas(tot_salon)+'</td>' +
            '<td style="text-align: center" class="field-tot_fish_del text-center">'+addCommas(tot_fisch_del)+'</td>' +
            '<td style="text-align: center" class="field-sales_delivery_cost text-center">'+addCommas(tot_del)+'</td>' +
        '</tr>')

}

$(document).ready(function () {

    if (window.location.href.includes("aggregate=days")){
        collapsedays()
    }
    if (window.location.href.includes("aggregate=months")){
        collapsemonths()
    }
    if (window.location.href.includes("aggregate=years")){
        collapseyears()
    }
    
    
    $(".expand_collapse").click(function (element) {
        date = $(this).attr('id')
        if ($(this).html() == '<i class="fas fa-plus-square"></i>'){
            $(this).html('<i class="fas fa-minus-square"></i>')
            $("td:contains('"+date+"')").parent('.row1,.row2').show()

        }
        else if ($(this).html() == '<i class="fas fa-minus-square"></i>'){
            $(this).html('<i class="fas fa-plus-square"></i>')
            $("td:contains('"+date+"')").parent('.row1,.row2').hide()
        }


    })



})
