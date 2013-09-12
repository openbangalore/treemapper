var user=null;
var treemapper = {};
var sid = null;

$(document).ready(function() {
	if(!wn.get_sid())
		$("[data-label='Add A Tree']").toggle(false);
});

treemapper = {
	current_step: "1",
	render: function() {
		var map = L.map('map').setView([start_y, start_x], 13);

		L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
			maxZoom: 18,
			attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
		}).addTo(map);

		trees.forEach(function(tree) {
			L.marker([tree.point_y, tree.point_x]).addTo(map)
				.bindPopup(repl("<b>%(scientific)s</b><br />%(address)s", tree));
		})
	},
	show_step: function(n) {
		if(treemapper.current_step) {
			$(".step-" + treemapper.current_step).toggle(false);
		}
		treemapper.current_step = n;
		$(".step-" + treemapper.current_step).toggle(true);
		
		$(".progress-bar").css("width", ((parseInt(n)-1) * 100 / 5) + "%")
		
		scroll(0, 0);
	},
	setup_login: function() {
		$(".splash").toggle(true);
		$(".btn-login").click(function() {
			window.location.href = "login";
		});
	},
	show_add: function() {
		$(".splash").toggle(false);
		treemapper.get_location("Checking location services on your device...", function() {
				$(".add-tree").toggle(true);
		});
	},
	get_form_values: function(id) {
		var form = {};
		$.each($("#"+id).serializeArray(), function(i, obj) {
			form[obj.name] = obj.value;
		});
		return form;
	},
	get_location: function(message, callback) {
		NProgress.start();
		try {
			wn.show_message(message, "icon-map-marker icon-spin");
			navigator.geolocation.getCurrentPosition(function(pos) {
				NProgress.done();
				if(pos) {
					callback(pos);
					wn.hide_message();
				} else {
					treemapper.no_location();
				}
			});
		} catch(e) {
			console.log(e);
			NProgress.done();
			wn.hide_message();
			treemapper.no_location();
		}
	},
	no_location: function() {
		wn.show_message("Please use a device with GPS and allow your browser to capture your location.", 
			"icon-warning-sign")
	}
}