
  
  $(document).ready(function(){

  // profilefeeds
  // Tipped.create(".userinfotip",{position : "bottom"});  

  // for introho page
  Tipped.create(".most_liked_feed_today",{position : 'top'});
  Tipped.create(".responseimgs",{position: 'top'});

  // special feeds page
  Tipped.create(".responselikes", {position : 'bottomleft'});
  Tipped.create(".challenge", {position : 'topright'});      // if you could do it better text in right upper side
  Tipped.create(".challengeimgrightside", {position : 'topright'});
  Tipped.create(".challenge_imgs_vertical",{position: 'right'});

  // partial feeds_feed_profile.html
  Tipped.create(".agreedtip",{position : 'bottomright'});

  //feeds.html   common with others
 
  //challenge_feeds.html
  Tipped.create(".tip", {position : 'bottomleft'});  // for new style link button
  Tipped.create(".mostliked", {position : 'topright'});
  Tipped.create(".shownowtip", {position : 'bottomleft'});
  Tipped.create(".challengelikes", {position : 'bottomleft'});
  Tipped.create(".btn-compose", {position : 'bottomleft'}); 
  Tipped.create(".challengefeedsimg", {position : 'right'});
  Tipped.create(".challenge_img_horizontal", {position : 'top'});

  //introho.html
  Tipped.create("#invite",'Enter your friends email address',{position : 'left'});  
  Tipped.create(".explorebtn",'Hey There, Click to explore the new things on hohos',{position : 'right'});
  Tipped.create(".fb-like",'Like hohos on Facebook',{position : 'bottom'});
  Tipped.create(".hohoslogo",'Explore the New world of strange Expressions and styles coming from human behaviour',{position : 'top'}); 
  Tipped.create(".Welcomebtn",'Enter the world of strange Human behaviour & expressions formed naturally',{position : 'bottom'});
  Tipped.create(".whatsup",'Hope you are awesome. Lets Enter the world of strange Human behaviour & expressions formed naturally',{position : 'bottom'});
  Tipped.create(".navbar-brand", 'hohos' ,{position:'bottom'});
  Tipped.create(".privacy", 'Learn about our Privacy Policy', {position: 'top'});
  Tipped.create(".terms", 'Learn about Terms', {position: 'top'});
  Tipped.create(".contact", 'Contact Us', {position: 'top'});
  Tipped.create(".about", 'Know more about hohos', {position: 'top'});

  //header
  Tipped.create(".response",'See the strange human behavious and expressions?',{position:'bottomleft'});
  Tipped.create(".challenge",'challenge people with your expressions',{position:'bottomleft'});
  Tipped.create(".response",'See the strange human behavious and expressions?',{position:'bottomleft'});
  Tipped.create(".wearehere",'About hohos',{position:'bottomleft'});


});


// the common tipped in different pages are commented out and different are remained, makes work faster really :)