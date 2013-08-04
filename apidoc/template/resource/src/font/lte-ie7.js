/* Load this script using conditional IE comments if you need to support IE 7 and IE 6. */

window.onload = function() {
	function addIcon(el, entity) {
		var html = el.innerHTML;
		el.innerHTML = '<span style="font-family: \'apidoc\'">' + entity + '</span>' + html;
	}
	var icons = {
			'i-arrow-right' : '&#xbb;',
			'i-upload' : '&#x2934;',
			'i-download' : '&#x2935;',
			'i-play' : '&#x25ba;',
			'i-shuffle' : '&#x25eb;',
			'i-target' : '&#x25c9;',
			'i-file' : '&#x25a0;',
			'i-switch' : '&#x21c4;',
			'i-add-to-list' : '&#x2630;',
			'i-info' : '&#x2713;',
			'i-stats' : '&#x2774;'
		},
		els = document.getElementsByTagName('*'),
		i, attr, html, c, el;
	for (i = 0; ; i += 1) {
		el = els[i];
		if(!el) {
			break;
		}
		attr = el.getAttribute('data-icon');
		if (attr) {
			addIcon(el, attr);
		}
		c = el.className;
		c = c.match(/i-[^\s'"]+/);
		if (c && icons[c[0]]) {
			addIcon(el, icons[c[0]]);
		}
	}
};