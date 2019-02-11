$(function() {
	// body...
	$('#cat-1').change(function() {
		// body...
		$.ajax({
			type: "POST",
			url: "/d_filter/",
			data: {
				search_text : $('#cat-1').val(),
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

