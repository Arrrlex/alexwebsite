$( document ).ready(function() {
	$( "rect.look" ).hover(function() {
		var overlay = $( "#overlay" );
		var pos = $(this)[0].getBoundingClientRect();
		overlay.css("visibility","visible");
		overlay.html($(this).data("width") 
			+ " &times; " 
			+ $(this).data("height") 
			+ " m<sup>2</sup>");
		var parentOffset = overlay.parent().offset();
		var scrollTop = document.body.scrollTop || document.documentElement.scrollTop;
		overlay.css("left", pos.left - parentOffset.left);
		overlay.css("top", pos.top + scrollTop - parentOffset.top);
		overlay.css("width", Math.max(pos.width, 100));
	}, function() {
		var overlay = $( "#overlay" );
		overlay.css("visibility", "hidden");
	});
});
$(document).ready(function() {
	$("#tiling-form").validate({
		rules: {
			width: {
				required: true,
				number: true,
				min: 0.1,
				max: 100,
				maxlength: 4
			},
			height: {
				required: true,
				number: true,
				min: 0.1,
				max: 100,
				maxlength: 4
			},
			side_length: {
				required: true,
				number: true,
				min: 0.1,
				max: 100,
				maxlength: 4
			},
			cost_per_tile: {
				number: true,
				min: 0,
				max: 1000,
				maxlength: 4
			}
		}
	});
	var func_dict = {
		'pi': 878,
		'e': 1937,
		'fib': 1554857,
		'prime_factors': 1000000,
		'to_binary': 10000000,
		'primes_list': 1000
	}
	$("#basic-form").validate({
		rules: {
			arg: {
				min: 0,
				max: func_dict[$("#func").val()]
			}
		}
	})
});
