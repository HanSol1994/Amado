$(document).ready(function(){
    // $('input[type=number]').on('mousewheel',function(e){ console.log("hi") });
    // // Disable keyboard scrolling
    // $('input[type=number]').on('keydown',function(e) {
    //     var key = e.charCode || e.keyCode;
    //     // Disable Up and Down Arrows on Keyboard
    //     if(key == 38 || key == 40 ) {
    // 	e.preventDefault();
    //     } else {
    // 	return;
    //     }
    // });
    
    $(':input[type=number]').on('wheel',function(e){ $(this).blur(); });

    
    $('form').on('focus', 'input[type=number]', function (e) {
      $(this).on('mousewheel.disableScroll', function (e) {
        e.preventDefault()
      })
    })
    $('form').on('blur', 'input[type=number]', function (e) {
      $(this).off('mousewheel.disableScroll')
    })

    
})