$(function() {
	// body...
	$('#psearch').keyup(function() {
		// body...
		$.ajax({
			type: "POST",
			url: "/paymentsearch/",
			data: {
				search_text : $('#psearch').val(),
				'csrfmiddlewaretoken' : $("input[name=csrfmiddlewaretoken]").val()
			},
			success: searchSuccess,
			dataType:'html'
		});

	});
});

function searchSuccess(data,textStatus,jqXHR) 
{
	$('#searchresults4').html(data);
}

