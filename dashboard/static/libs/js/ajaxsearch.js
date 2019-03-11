$(function() {
	// body...
	$('#isearch').keyup(function() {
		// body...
		$.ajax({
			type: "POST",
			url: "/indexsearch/",
			data: {
				search_text : $('#isearch').val(),
				'csrfmiddlewaretoken' : $("input[name=csrfmiddlewaretoken]").val()
			},
			success: searchSuccess,
			dataType:'html'
		});

	});
});

function searchSuccess(data,textStatus,jqXHR) 
{
	$('#searchresults').html(data);
}

