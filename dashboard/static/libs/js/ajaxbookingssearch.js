$(function() {
	// body...
	$('#bsearch').keyup(function() {
		// body...
		$.ajax({
			type: "POST",
			url: "/bookingsearch/",
			data: {
				search_text : $('#bsearch').val(),
				'csrfmiddlewaretoken' : $("input[name=csrfmiddlewaretoken]").val()
			},
			success: searchSuccess,
			dataType:'html'
		});

	});
});

function searchSuccess(data,textStatus,jqXHR) 
{
	$('#searchresults6').html(data);
}

