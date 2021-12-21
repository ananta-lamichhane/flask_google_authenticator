$(document).ready(function(){
   setInterval(function(){
       $.ajax({
        type: "GET",
            url: '/?api=true', // query with the server every second
            success: function(response){
                        // since the response is nested json, finding out the time sent from the server
                        let count = 30 - (Object.values(Object.values(response)[0])[1] % 30)
                        // count goes to 30 hence percent is 3.33 times that
                        let percent = count * 3.33
                            //iterate through each label, code keypair
                            Object.values(response).forEach((element, index) =>{
                                let code = Object.values(element)[0]
                                //update the code
                                $('#code'+(index+1).toString()).text(code+"")
                            }
                                //update the countdown timer
                                $('#timeout').text(count);
                                //update the progress bar
                                $('.progress-bar').css('width', percent+'%')
            }
        });

           }, 1000);


});