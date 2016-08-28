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