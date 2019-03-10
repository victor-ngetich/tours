
var numKid = 0;

// $("#adults11").change( function(){
//     numAdult = $("#adults11").val();
//     calcTotals();
// });
// $("#kids11").change( function() {
//     numKid = $("#kids11").val();
//     calcTotals();
// });

// function calcTotals(){
//     $("#total11").text(235*numAdult);

// }



// var callback = function(e){
//     var text = e.type;
//     var code = e.which ? e.which : e.keyCode;
// };

// $('#id_adults').keydown(callback);
// $('#id_adults').keypress(callback);
// $('#id_adults').keyup(callback);

// $('.keydown').click(function(e){
//     var code = $(this).data('code');
//     $('#adults1').trigger(
//         jQuery.Event( 'keydown', { keyCode: code, which: code } )
//     );
// });
// $('.keypress').click(function(e){
//     var code = $(this).data('code');
//     $('#adults1').trigger(
//         jQuery.Event( 'keypress', { keyCode: code, which: code } )
//     );
// });
// $('.keyup').click(function(e){
//     var code = $(this).data('code');
//     $('#adults').trigger(
//         jQuery.Event( 'keyup', { keyCode: code, which: code } )
//     );
// });


// function myFunction() {
//   var x = document.getElementById("adults11").value;
//   document.getElementById("demo").innerHTML = "You wrote: " + x;
// }


$('#id_adults').on('keypress keyup keydown',function(event) { 
    // create the event
     var press = jQuery.Event(event.type);
     var code = event.keyCode || event.which;
     press.which = code ;   
    // trigger 
    // $('*[id^="adults1"]').val(this.value);
    $('*[id^="adults1"]').trigger(event.type, {'event': press});
  });


// e = jQuery.Event("keypress")
// e.which = 13 //choose the one you want
//     $("#adults11").input(function(){
//      alert('keypress triggered')
//     }).trigger(e)

// var n = document.getElementById("id_adults"),
//     r = document.getElementById("adults11");

//     n.addEventListener("input", function(e) {
//         r.innerHTML += "input event triggered <br/>";
//     }, false);
    
//     n.addEventListener("keyup", function(e) {
//         r.innerHTML += "keyup event triggered <br/>";
//     }, false);
    
//     n.addEventListener("change", function(e) {
//         r.innerHTML += "change event triggered <br/>";
//     }, false);