$(function () {
    
    $('.vjDateField').datepicker({
            dateFormat: 'yy-mm-dd',
            changeMonth: true,
            changeYear: true,
            showOn: 'both',
            buttonImage: 'http://amadowh.ir/AmadoWHApp/static/admin/jquery.ui.datepicker.jalali/themes/base/images/icon-calendar.svg',
            buttonImageOnly: true,
        //     minDate: $('.vjDateField').val(),
        //     maxDate: '+30Y',
        });    
    
});
