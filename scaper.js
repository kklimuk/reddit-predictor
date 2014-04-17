var mined_from = 'music';
(function(mined_from) {
	var PROHIBITED_DOMAINS = ['imgur','instagram', 'flickr', 'photobucket', 'memebase', '9gag', 'failblog', 'quickmeme', 'youtube', 'vimeo'],
		PROHIBITED_FORMATS = ['.gif', '.jpeg', '.jpg', '.png'];

	var data = [].map.call(document.querySelectorAll('.thing'), function(el) {
		var title_el = el.querySelector('a.title'),
			rank_el = el.querySelector('.rank');

		var id = el.classList;
		for (var i = 0; i < id.length; i++) {
			if (id[i].indexOf('id-') !== -1) {
				id = id[i].substring(3);
				break;
			}
		}

		return {
			'reddit_id': id,
			'title': title_el.innerText,
			'link': title_el.href,
			'mined_from': mined_from,
			'upvotes': el.getAttribute('data-ups'),
			'downvotes': el.getAttribute('data-downs'),
			'rank': rank_el ? +(rank_el.innerText) : 0
		};
	}).filter(function(entry) {
		if (entry.rank === 0) {
			return false;
		}

		for (var i = 0; i < PROHIBITED_DOMAINS.length; i++) {
			if (entry.link.indexOf(PROHIBITED_DOMAINS[i]) !== -1) {
				return false;
			}
		}

		for (var i = 0; i < PROHIBITED_FORMATS.length; i++) {
			if (entry.link.indexOf(PROHIBITED_FORMATS[i]) !== -1) {
				return false;
			}
		}

		return true;
	});

	var url = URL.createObjectURL(new Blob([JSON.stringify(data)], { type: 'application/json '}));
	var a = document.createElement('a');
	a.href = url;
	a.download = mined_from + '.json';
	a.click();

})(window.mined_from)