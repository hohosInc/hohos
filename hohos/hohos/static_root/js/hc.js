      
        $(document).ready(function() {
            
           //  var from_user = document.getElementById('from_user').text;
           //  var to_user = document.getElementById('to_user').text;
           //  // var from_user = undefined

           //  if(from_user!=undefined){ var username=from_user; }
           //  else { var username=to_user; }

           // $( "#log" ).append( "<div>mouse hovered on mytooltip items username is - </div>" + username);            

        $(".my-tooltip").mouseover(function() {

        //   $( "#log" ).append( "<div>mouse hovered on mytooltip items username is - </div>" + username);           
        
        var user_id = $(this).attr('id');
        var username = document.getElementById(user_id).text;
         $( "#log" ).append(username+' ');

            $.ajax({  

                  url : '/feeds/userinfo/',
                  data : { 'username': username,},

                  success : function(data){
                    // $("#log").text('got the html response from server and stored in datahtml');
                    var datahtml = data;
                    // $("#log").html(datahtml);

          $(function() {
              $('.my-tooltip').tooltipster({
                interactive: true,
                content: 'Loading...',
                contentCloning: false,
                contentAsHTML: true,
                animation: 'fade',
                cache : false,

                    functionBefore: function(origin, continueTooltip) {
                    // we'll make this function asynchronous and allow the tooltip to go ahead and show the loading notification while fetching our data.
                      continueTooltip();
                      origin.tooltipster('content', datahtml, false);
                    }
                });
              });  
            },

            // complete : function(){
            // 	var user_id = undefined 
            // },

           });

          });
       });