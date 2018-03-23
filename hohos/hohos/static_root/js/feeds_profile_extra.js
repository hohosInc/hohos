  
$(function () {

  var substringMatcher = function(strs) {
    return function findMatches(q, cb) {
      var matches, substringRegex;
      matches = [];
      substrRegex = new RegExp(q, 'i');  
      $.each(strs, function(i, str) {
        if (substrRegex.test(str)) {
          matches.push({ value: str });
        }
      });
      cb(matches);
    };
  };

  $.ajax({
    url: '/searchusers_simple/',
    cache: false,    
    success: function (data) {    
      $('#to_user').typeahead({ 
        hint: true,   
        highlight: true,
        minLength: 2,
      },
      {  
        name: 'data',
        displayKey: 'value',
        source: substringMatcher(data)
      });
    }
  }); 

});


  $(".btn-post").click(function () {
    // var last_feed = $(".stream li:first-child").attr("feed-id");
    // if (last_feed == undefined) {
    //   last_feed = "0";
    // }
    // $("#compose-form input[name='last_feed']").val(last_feed);
    var to_user = $("#compose-form input[name='to_user']").val();
    var post = $("#compose-form textarea[name='post']").val();

    if(to_user!= "" && post!=""){
    $.ajax({
      url: '/feeds/post/',
      data: $("#compose-form").serialize(),
      type: 'post',   
      cache: false,
      success: function (data) {
        $("ul.stream").prepend(data);
        $("#compose-form input[name='to_user']").val('');
        $("#compose-form textarea[name='post']").val('');
        $(".compose").slideUp(900);
        $(".compose").removeClass("composing");
      }
    }),

    $.ajax({
      url: '/feeds/post/email/',
      data: $("#compose-form").serialize(),
      type: 'post', 
      cache: false,
      success: function (data) {
        // doing nothing with returned data, as this is to send main only
      }    
    
    });

    }

  });


  var load_feeds = function () {
    if (!$("#load_feed").hasClass("no-more-feeds")) {
      var next_page = parseInt($("#load_feed input[name='page']").val()) + 1;
      $("#load_feed input[name='page']").val(next_page);
      $.ajax({
        url: '/feeds/load/',
        data: $("#load_feed").serialize(),
        cache: false,
        beforeSend: function () {
          $(".load").show();
        },
        success: function (data) {
          if (data.length > 0) {
              $("ul.stream").append(data);
          }
          else {
            $("#load_feed").addClass("no-more-feeds");
          }
        },
        complete: function () {
          $(".load").hide();
        }
      });
    } 
  };

  $("#load_feed").bind("enterviewport", load_feeds).bullseye();


$(document).ready(function(){
  Tipped.create(".other", 'Click to see the OpenChat' ,{position:'bottom'});
});
