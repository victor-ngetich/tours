$(function() {
	// body...
	$('#cat-2').change(function() {
		// body...
		$.ajax({
			type: "POST",
			url: "/p_filter/",
			data: {
				search_text : $('#cat-2').val(),
				'csrfmiddlewaretoken' : $("input[name=csrfmiddlewaretoken]").val()
			},
			success: searchSuccess,
			dataType:'html'
		});

	});
});

function searchSuccess(data,textStatus,jqXHR) 
{
	$('#search-results').html(data);
}

