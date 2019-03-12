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

// Delete Confirmation
function deleteFunction(e) {
    if(!confirm("Are you sure you want to delete?")){
        e.preventDefault();
    }else{
     $('#person-delete').submit();
    }            
}
// Delete Confirmation
