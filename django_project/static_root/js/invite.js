
         $(document).ready(function() {
            
            $("#invitebutton").click(function(){
              event.preventDefault()
              var email = document.getElementById('invite').value;

              if(email != undefined && email.includes("@") && email.includes(".")){

                $.ajax({

                url: '/invite/',
                data: $('.user-invite-form').serialize(),
                type: 'post',
                cache: false, 

                beforeSend : function(){
                  $("#invitebutton").html('<i class="fa fa-spin fa-spinner fa-1x"></i>');
                },

                success : function(data){
                      $("#invitebutton").html(data); 
                },
                
                complete : function () {
                	$("#invitebutton").html('<i class="fa fa-check fa-1x"></i>'+' Invited '+'<i class="fa fa-smile-o fa-1x"></i>');	
                  window.setTimeout(function(){ $("#invitebutton").text(' Invite '); },3000);
                },

               });
             }else{
              $("#invitebutton").html('<i class="fa fa-frown-o fa-1x"></i>'+' Wrong Email ');
                  window.setTimeout(function(){
                  $("#invitebutton").text(' Invite ');
                },3000);
            }

            });
         });


    // $(document).ready(function(){
    //   function show_invite_btn(){
    //       $("#invitebutton").css('display','block');
    //   }
    // });
