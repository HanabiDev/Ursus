/*---LEFT BAR ACCORDION----*/
$(function() {
    $('#nav-accordion').dcAccordion({
        eventType: 'click',
        autoClose: true,
        saveState: true,
        disableLink: true,
        speed: 'slow',
        showCount: false,
        autoExpand: true,
//        cookie: 'dcjq-accordion-1',
        classExpand: 'dcjq-current-parent'
    });
});

var Script = function () {


//    sidebar dropdown menu auto scrolling

    jQuery('#sidebar .sub-menu > a').click(function () {
        var o = ($(this).offset());
        diff = 250 - o.top;
        if(diff>0)
            $("#sidebar").scrollTo("-="+Math.abs(diff),500);
        else
            $("#sidebar").scrollTo("+="+Math.abs(diff),500);
    });



//    sidebar toggle

    $(function() {
        function responsiveView() {
            var wSize = $(window).width();
            if (wSize <= 768) {
                $('#container').addClass('sidebar-close');
                $('#sidebar > ul').hide();
            }

            if (wSize > 768) {
                $('#container').removeClass('sidebar-close');
                $('#sidebar > ul').show();
            }
        }
        $(window).on('load', responsiveView);
        $(window).on('resize', responsiveView);
    });

    $('.fa-bars').click(function () {
        if ($('#sidebar > ul').is(":visible") === true) {
            $('#main-content').css({
                'margin-left': '0px'
            });
            $('#sidebar').css({
                'margin-left': '-210px'
            });
            $('#sidebar > ul').hide();
            $("#container").addClass("sidebar-closed");
        } else {
            $('#main-content').css({
                'margin-left': '210px'
            });
            $('#sidebar > ul').show();
            $('#sidebar').css({
                'margin-left': '0'
            });
            $("#container").removeClass("sidebar-closed");
        }
    });

// custom scrollbar
    $("#sidebar").niceScroll({styler:"fb",cursorcolor:"#ABABAB", cursorwidth: '5', cursorborderradius: '10px', background: '#404040', spacebarenabled:false, cursorborder: ''});

    $("html").niceScroll({styler:"fb",cursorcolor:"#ABABAB", cursorwidth: '8', cursorborderradius: '10px', background: '#404040', spacebarenabled:false,  cursorborder: '', zindex: '1000'});

// widget tools

    jQuery('.panel .tools .fa-chevron-down').click(function () {
        var el = jQuery(this).parents(".panel").children(".panel-body");
        if (jQuery(this).hasClass("fa-chevron-down")) {
            jQuery(this).removeClass("fa-chevron-down").addClass("fa-chevron-up");
            el.slideUp(200);
        } else {
            jQuery(this).removeClass("fa-chevron-up").addClass("fa-chevron-down");
            el.slideDown(200);
        }
    });

    jQuery('.panel .tools .fa-times').click(function () {
        jQuery(this).parents(".panel").parent().remove();
    });


//    tool tips

    $('.tooltips').tooltip();

//    popovers

    $('.popovers').popover();



// custom bar chart

    if ($(".custom-bar-chart")) {
        $(".bar").each(function () {
            var i = $(this).find(".value").html();
            $(this).find(".value").html("");
            $(this).find(".value").animate({
                height: i
            }, 2000)
        })
    }

    $("#add_user input").addClass('form-control');
    $("#add_user label").addClass('form-control-label');
    $("#add_user .helptext").remove();


    $("#search-box").chosen({
        placeholder_text_single:'Escribe para buscar...',
        width: "50%",
        search_contains: true
    });

    $("#id_type, #id_client").addClass('form-control').chosen({
        width: "50%",
    });

    $("#search-box").change(function(){
        document.location.href=$( "#search-box option:selected" ).attr('data-href'); 
    });

    $("#id_genre, #id_dni_type, select[id=id_role]").addClass('form-control').chosen({
        width: "100%",
        disable_search: true
    });

    $("#add_user input[type='checkbox']").removeClass('form-control');

    $("#add_user input[type='file']").attr('onchange','update_image(this)');

    $("#change-photo-btn").click(function(){
        $("#add_user input[type='file']").click();
    });


}();

    var update_image = function(obj){
        
        // if IE < 10 doesn't support FileReader
        if(!window.FileReader){
            // don't know how to proceed to assign src to image tag
        } else {
            var reader = new FileReader();
            var target = null;
             
            reader.onload = function(e) {
                target =  e.target || e.srcElement;
                $("#user-avatar").prop("src", target.result);
            };
            
            reader.readAsDataURL(obj.files[0]);
        }
    }
