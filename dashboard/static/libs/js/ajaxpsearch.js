$(function() {
	// body...
	$('#isearch').keyup(function() {
		// body...
		$.ajax({
			type: "POST",
			url: "/packagesearch/",
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
	$('#searchresults2').html(data);
}

