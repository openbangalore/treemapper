var treemapper = {};
var user = null;

function repl(s, dict) {
	if(s==null)return '';
	for(key in dict) {
		s = s.split("%("+key+")s").join(dict[key]);
	}
	return s;
}

treemapper.render = function() {
	var map = L.map('map').setView([start_y, start_x], 13);

	L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
		maxZoom: 18,
		attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
	}).addTo(map);

	trees.forEach(function(tree) {
		L.marker([tree.point_y, tree.point_x]).addTo(map)
			.bindPopup(repl("<b>%(scientific)s</b><br />%(address)s", tree));
	})
};

treemapper.setup_persona = function() {
	navigator.id.watch({
	  loggedInUser: user,
	  onlogin: function(assertion) {
	    // A user has logged in! Here you need to:
	    // 1. Send the assertion to your backend for verification and to create a session.
	    // 2. Update your UI.
		console.log(assertion);
		return;
	    $.ajax({ /* <-- This example uses jQuery, but you can use whatever you'd like */
	      type: 'POST',
	      url: '/auth/login', // This is a URL on your website.
	      data: {assertion: assertion},
	      success: function(res, status, xhr) { window.location.reload(); },
	      error: function(xhr, status, err) {
	        navigator.id.logout();
	        alert("Login failure: " + err);
	      }
	    });
	  },
	  onlogout: function() {
	    // A user has logged out! Here you need to:
	    // Tear down the user's session by redirecting the user or making a call to your backend.
	    // Also, make sure loggedInUser will get set to null on the next page load.
	    // (That's a literal JavaScript null. Not false, 0, or undefined. null.)
	    $.ajax({
	      type: 'POST',
	      url: '/auth/logout', // This is a URL on your website.
	      success: function(res, status, xhr) { window.location.reload(); },
	      error: function(xhr, status, err) { alert("Logout failure: " + err); }
	    });
	  }
	});
	
	$(".btn-login").click(function() {
		navigator.id.request();
	});
}

$(document).ready(function() {
	treemapper.setup_persona();
});



