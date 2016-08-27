$( document ).ready(function() {
	$( "rect.look" ).hover(function() {
		var overlay = $( "#overlay" );
		var pos = $(this)[0].getBoundingClientRect();
		overlay.css("visibility","visible");
		overlay.html($(this).data("width") 
			+ " &times; " 
			+ $(this).data("height") 
			+ " m<sup>2</sup>");
		// Calculating the x-offset
		var mainML = getCSSVal('main', 'margin-left');
		var bodyML = getCSSVal('body', 'margin-left');
		var xOffset = mainML + bodyML;
		// Calculating the y-offset
		var bodyMT = getCSSVal('body', 'margin-top');
		var titleH = getCSSVal('h1', 'height');
		var titleMB = getCSSVal('h1', 'margin-bottom');
		var menuH = getCSSVal('nav', 'height');
		var mainMT = getCSSVal('main', 'margin-top');
		var yOffset = bodyMT + titleH + titleMB + menuH + mainMT;
		overlay.css("left", pos.left - xOffset);
		overlay.css("top", pos.top + window.pageYOffset - yOffset);
		overlay.css("width", Math.max(pos.width, 100));
	}, function() {
		var overlay = $( "#overlay" );
		overlay.css("visibility", "hidden");
	});
});

function getCSSVal(selector, attr) {
	var valStr = $( selector ).css(attr);
	return parseInt(valStr.substring(0, valStr.length - 2));
}