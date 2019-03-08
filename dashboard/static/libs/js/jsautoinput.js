$(function(){
    var $id_adults = $('#id_adults');
    var $adults1 = $('#adults1');
    function onChange() {
        $( "input[id^='adults1']" ).val($id_adults.val());
    };
    $('#id_adults')
        .ready(onChange)
        .change(onChange)
        .keyup(onChange);
});

$(function(){
    var $id_kids = $('#id_kids');
    var $kids1 = $('#kids1');
    function onChange() {
        $( "input[id^='kids1']" ).val($id_kids.val());
    };
    $('#id_kids')
        .ready(onChange)
        .change(onChange)
        .keyup(onChange);
});

$(function(){
    var $id_start_date = $('#id_start_date');
    var $start1 = $('#start1');
    function onChange() {
        $( "input[id^='start1']" ).val($id_start_date.val());
    };
    $('#id_start_date')
        .ready(onChange)
        .change(onChange)
        .keyup(onChange);
});

$(function(){
    var $id_end_date = $('#id_end_date');
    var $end1 = $('#end1');
    function onChange() {
        $( "input[id^='end1']" ).val($id_end_date.val());
    };
    $('#id_end_date')
        .ready(onChange)
        .change(onChange)
        .keyup(onChange);
});