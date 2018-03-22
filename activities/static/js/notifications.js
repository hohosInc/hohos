$(function () {
  $('#notifications').popover({html: true, content: 'Loading...', trigger: 'manual'});

  $("#notifications").click(function () {
    if ($(".popover").is(":visible")) {
      $("#notifications").popover('hide');
    }
    else {
      $("#notifications").popover('show');
      $.ajax({
        url: '/notifications/last/',
        beforeSend: function () {
          $(".popover-content").html("<div style='text-align:center'><i class='fa fa-spin fa-spinner fa-1x'></i></div>");
          $("#notifications").removeClass("new-notifications");
        },
        success: function (data) {   
          $(".popover-content").html(data);     
        }
      });
    }    
    return false;    
  });
 

$('body').on('click', function (e) {
    if ($(".popover").is(":visible")) {
      $("#notifications").popover('hide');
    }
});


  function check_notifications() {
    $.ajax({
      url: '/notifications/check/',
      cache: false,
      success: function (data) {
        if (data != "0") {
          $("#notifications").addClass("new-notifications");
          $(".badge").text(data);
        }
        else {
          $("#notifications").removeClass("new-notifications");
          $(".badge").text(''); 
        }
      },
      complete: function () {
        window.setTimeout(check_notifications, 30000);
      }
    });
  };
  check_notifications();
});



// $(document).ready(function(){

//   $("li.glyphicon-bell").click(function(){
//       $(".badge").hide();
//   });

// });