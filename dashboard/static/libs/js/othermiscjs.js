// Django Delete Confirmation
$(document).on('click', '.confirm-delete', function(){
    return confirm('Are you sure you want to delete this?');
})
// Django Delete Confirmation

// Django Cancel Booking Confirmation
$(document).on('click', '.confirm-cancel1', function(){
    return confirm('Are you sure you want to cancel this booking?');
})
// Django Cancel Booking Confirmation

// Django Package Delete Confirmation
$(document).on('click', '.confirm-delete1', function(){
    return confirm('Are you sure you want to delete this package?');
})
// Django Package Delete Confirmation

// Django User Account Delete Confirmation
$(document).on('click', '.confirm-delete2', function(){
    return confirm('Are you sure you want to delete your account!?');
})
// Django User Account Delete Confirmation

// Delete Confirmation
function deleteFunction(e) {
    if(!confirm("Are you sure you want to delete?")){
        e.preventDefault();
    }else{
     $('#person-delete').submit();
    }            
}
// Delete Confirmation

//Modal auto load
$(window).load(function(){        
    $('#myModal').modal('show');
     }); 
//Modal auto load

//Date picker
function checkDate() {
    var selectedText = document.getElementById('id_start_date').value;
    var selectedDate = new Date(selectedText);
    var now = new Date();
    if (selectedDate < now) {
     alert("Date must be in the future");
    }
  }

//Date picker2
// var maxDate = year + '-' + month + '-' + day;
// alert(maxDate);
// $('#txtDate').attr('min', maxDate);

$(function(){
    var dtToday = new Date();
    
    var month = dtToday.getMonth() + 1;
    var day = dtToday.getDate();
    var year = dtToday.getFullYear();
    if(month < 10)
        month = '0' + month.toString();
    if(day < 10)
        day = '0' + day.toString();
    
    var maxDate = year + '-' + month + '-' + day;
    alert(maxDate);
    $('#txtDate').attr('min', maxDate);
});

// Date picker3
$(function () {

    $('#datetimepicker').datetimepicker({  minDate:new Date()});
});
