$(function() {
	// body...
	$('#psearch1').keyup(function() {
		// body...
		$.ajax({
			type: "POST",
			url: "/paymentsearch1/",
			data: {
				search_text : $('#psearch1').val(),
				'csrfmiddlewaretoken' : $("input[name=csrfmiddlewaretoken]").val()
			},
			success: searchSuccess,
			dataType:'html'
		});

	});
});

function searchSuccess(data,textStatus,jqXHR) 
{
	$('#searchresults5').html(data);
}

