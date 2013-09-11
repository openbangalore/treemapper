var user=null;
var treemapper = {};
var sid = null;

$(document).ready(function() {
	sid = getCookie("sid");
	treemapper.hide_message();
	if(sid && sid!=="Guest") {
		treemapper.show_add();
	} else {
		treemapper.setup_login();
	}
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
	show_message: function(text, icon) {
		if(!icon) icon="icon-refresh icon-spin";
		treemapper.hide_message();
		$('<div class="message-overlay"></div>')
			.html('<div class="content"><i class="'+icon+' text-muted"></i><br>'
				+text+'</div>').appendTo(document.body);
	},
	hide_message: function(text) {
		$('.message-overlay').remove();
	},
	show_step: function(n) {
		if(treemapper.current_step) {
			$(".step-" + treemapper.current_step).toggle(false);
		}
		treemapper.current_step = n;
		$(".step-" + treemapper.current_step).toggle(true);
		
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
		$(".add-tree").toggle(true);
	},
	call: function(cmd, data, success, error) {
		data.cmd = cmd;
		NProgress.start();
		$.ajax({
			type: 'POST',
			url: 'server.py', // This is a URL on your website.
			data: data,
			dataType: "json",
			success: function(r) {
				NProgress.done();
				if(r.action==="refresh") {
					window.location.reload();
				}
				success(r);
			},
			error: error
		});
	},
	get_form_values: function(id) {
		var form = {};
		$.each($("#"+id).serializeArray(), function(i, obj) {
			form[obj.name] = obj.value;
		});
		return form;
	},
}

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


