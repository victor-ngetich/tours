$(function() {
	// body...
	$('#apsearch').keyup(function() {
		// body...
		$.ajax({
			type: "POST",
			url: "/ourpackagesearch/",
			data: {
				search_text : $('#apsearch').val(),
				'csrfmiddlewaretoken' : $("input[name=csrfmiddlewaretoken]").val()
			},
			success: searchSuccess,
			dataType:'html'
		});

	});
});

function searchSuccess(data,textStatus,jqXHR) 
{
	$('#searchresults3').html(data);
}

