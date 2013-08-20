var user=null;
var treemapper = {};

treemapper = {
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
	setup_login: function() {
		$(".toolbar-message").html('Login to add a tree.');
		$('<button class="btn btn-primary btn-login">Login</button>')
			.appendTo($(".toolbar-btn-area").empty())
			.click(function() {
				treemapper.setup_persona();
				navigator.id.request();
			});
	},
	setup_toolbar: function() {
		$(".toolbar-message").html(repl('%(email)s, <a href="#" class="logout"">Logout</a></p>',
				{email: getCookie("email")}));

		$('<button class="btn btn-primary pull-right btn-add">Add A Tree</button>')
			.appendTo($(".toolbar-btn-area").empty())
			.click(function() {
				alert("Nothing to see yet!")
			});

		$(".logout").click(function() {
			treemapper.setup_persona();
			navigator.id.logout();
			return false;
		});
	},
	call: function(cmd, data, success, error) {
		data.cmd = cmd;
		$.ajax({
			type: 'POST',
			url: 'server.py', // This is a URL on your website.
			data: data,
			dataType: "json",
			success: function(r) {
				if(r.action==="refresh") {
					window.location.reload();
				}
				success(r);
			},
			error: error
		});
	},
	setup_persona: function() {
		navigator.id.watch({
			loggedInUser: getCookie("email"),
			onlogin: function(assertion) {
				$(".btn-login").html("Verifying...").attr("disabled", "disabled");
				treemapper.call("login", {assertion: assertion}, function(res) {
					treemapper.setup_toolbar();
				})
			},
			onlogout: function() {
				treemapper.call("logout", {}, function(res) {
					treemapper.setup_login();
				})
			}
		})
	},
	get_form_values: function(id) {
		$("#"+id).find('["name"]')
	},
	setup_add_tree: function() {
		treemapper.call("add_tree", { tree: {  }}, 
			function(res) {
			
			});
	}
}

$(document).ready(function() {
	if(getCookie("sid")) {
		treemapper.call("verify", {}, function(res) { 
			if(res.session_status!="okay") {
				treemapper.setup_login();
			} else {
				treemapper.setup_toolbar();
				treemapper.setup_add_tree();
			}
		});
	} else {
		treemapper.setup_login();
	}
});

function repl(s, dict) {
	if(s==null)return '';
	for(key in dict) {
		s = s.split("%("+key+")s").join(dict[key]);
	}
	return s;
}

function getCookie(c) {
	if(!document.cookie) return "";
	var clist = (document.cookie+'').split(';');
	var cookies = {};
	for(var i=0;i<clist.length;i++) {
		var tmp = clist[i].split('=');
		cookies[tmp[0].trim()] = tmp[1].trim();
	}
	ret = cookies[c];
	if(ret && ret.substr(0,1)=='"') ret = ret.substr(1, ret.length-2);
	return ret;
}


