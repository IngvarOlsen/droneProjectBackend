//The original background effect and input style was forked from https://codepen.io/Lewitje/pen/BNNJjo
//The Password strength is from https://codepen.io/ahsanrathore/pen/WvpEPJ
//Other than the mixing and some restyling, I've added views for "Create User" and "Forgot Password"
//Right now there is no checker for repeat password or if inputed email is an email

///////////////////
//View controller//
///////////////////
$('.registerForm').hide();

//  $('.newUserBtn').click(function(e) {
//    e.preventDefault();
// 	 $('.loginForm').hide();
// 	 $('.registerForm').fadeIn(500);
//  });

 function newUserView(){
    // this.preventDefault();
    $('.loginForm').hide();
    $('.registerForm').fadeIn(500);
 }

function cancelToStart(){
    $('.registerForm').hide();
    $('.forgotPasswordForm').hide();
    $('.loginForm').fadeIn(500);
}

function forgotPasswordView(){
    $('.loginForm').hide();
    $('.forgotPasswordForm').fadeIn(500);
}

// $('.cancelBtn').click(function(e) {
//    e.preventDefault();
// 	 $('.registerForm').hide();
// 	 $('.forgotPasswordForm').hide();
// 	 $('.loginForm').fadeIn(500);
	
//  });

$('.forgotPasswordBtn').click(function(e) {
   e.preventDefault();
	 $('.loginForm').hide();
	 $('.forgotPasswordForm').fadeIn(500);
 });

$("#login-button").click(function(event){
		 event.preventDefault();
	 
	 $('form').fadeOut(500);
	 $('.wrapper').addClass('form-success');
});


/////////////////////
// Password Match  //
/////////////////////
$("#login-button").click(function(event){
		 event.preventDefault();
	 
	 $('form').fadeOut(500);
	 $('.wrapper').addClass('form-success');
});


/////////////////////
//Password strength//
/////////////////////
$(document).ready(function() {
    console.log("Password str checker loaded");
    var result = $("#password-str");
    $('#newPassword').keyup(function(){
        $(".bar-text").html(checkStr($('#newPassword').val()))
    })  
 
    function checkStr(pas){
    //Start str
    var str = 0;
    
    if (pas.length == 0) {
        result.removeClass();
        return '';
    }
    //If pas is less than 7 return to normal
    if (pas.length < 9) {
        result.removeClass();
        result.addClass('normal');
        return 'Normal';
    }

    //If length is 8 chars or more, then increase str
    if (pas.length > 9){
        str += 1;
    } 
 
    //If pass cointains lower and uppercase chars, then increase str 
    if (pas.match(/([a-z].*[A-Z])|([A-Z].*[a-z])/)){
        str += 1;
    }  
 
    //If special chars, then increase str 
    if (pas.match(/([!,%,&,@,#,$,^,*,?,_,~])/))
    {
        str += 1;
    }  
 
    //If more special chars, then increase str
    if (pas.match(/(.*[!,%,&,@,#,$,^,*,?,_,~].*[!,",%,&,@,#,$,^,*,?,_,~])/)){
        str += 1;
    }
 
    //Returns message and removes and adds styles
    if (str < 2) {
        result.removeClass();
        result.addClass('medium');
        return 'Medium';
    } else if (str == 2 ) {
        result.removeClass();
        result.addClass('strong');
        return 'Strong';
    } else {
        result.removeClass();
        result.addClass('vstrong');
        return 'Very Strong';
    }
  }
});