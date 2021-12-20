$(document).ready(function(){
  let  prev_code = ""
    console.log("ok")




    $('#timeout').text("30");
   let count = 30 - Math.round(new Date() / 1000) % 30
    let percent = 100.0 - count*3.33
    console.log(percent)
   setInterval(function(){
       $.ajax({
        type: "GET",
            url: '/?api=true',
            success: function(response){

                        let new_code = Object.values(response)[0]
                        if(new_code+"" !== prev_code){
                            Object.values(response).forEach((element, index) =>{
                                $('#code'+(index+1).toString()).text(element+"")
                                prev_code = new_code
                            })
                            }

                            $('#timeout').text(count);
                            $('.progress-bar').css('width', percent+'%')
                            percent <1.0?percent=100.0: percent =percent - 3.33
                            count==0?count=30:count--

                        $('.progress-bar').css('width', percent+'%')//.attr('aria-valuenow', 0);





            }
        });

           }, 1000);


});