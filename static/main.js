(function(WordCloud) {
	'use strict';

	function logError (error) {
		if (error.stack) {
			return console.error(error.stack);
		}
		console.error(error);
	}

	function post(url, data) {
		return new Promise(function(resolve, reject) {
			var request = new XMLHttpRequest();
			request.open('POST', url, true);
			request.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');

			request.onload = function() {
				if (request.status >= 200 && request.status < 300) {
					return resolve(JSON.parse(request.responseText));
				}
				reject({
					status: request.status,
					response: request.responseText
				});
			};

			request.onerror = reject;

			request.send(JSON.stringify(data));
		});
	}

	function clear_article (config) {
		config.title.innerHTML = '';
		config.context.clearRect(0, 0, 550, 400);
		config.article.style.maxHeight = '0px';
		config.article.style.padding = '0';

		config.spinner.spin();
		config.spinner_section.style.height = '100px';
		config.spinner_section.appendChild(config.spinner.el);
	}

	function article_loaded (config) {
		config.article.style.display = 'block';
		config.article.style.padding = '15px 20px';
		config.spinner_section.style.height = '0px';
		config.spinner.stop();
	}

	function organize_prediction (data) {
		var subreddits = Object.keys(data);
		var ordered = subreddits.map(function(subreddit) {
			return {
				name: subreddit,
				score: data[subreddit]
			}
		}).sort(function(a, b) {
			return a.score > b.score ? -1 : 1;
		});

		return {
			labels: ordered.map(function(subreddit) { return subreddit.name }),
			dataset: ordered.map(function(subreddit) { return subreddit.score })
		};
	}

	function normalize_salience (data) {
		var average_score = data.reduce(function(acc, entry) {
			return acc + entry[1];
		}, 0) / data.length;

		return data.map(function(entry) {
			entry[1] = Math.round(entry[1] / average_score * 50);
			return entry;
		});
	}

	function onload() {
		var config = {
			// search
			submit: document.querySelector('form button'),
			input: document.querySelector('form input'),
			
			// submission article
			article: document.querySelector('form > article'),
			title: document.querySelector('form > article h1'),
			link: document.querySelector('form > article a'),
			context: document.querySelector('article #chart').getContext('2d'),
			chart: {
				scaleShowGridLines: false,
				scaleFontSize: 16
			},

			// wordcloud
			wordcloud: document.querySelector('canvas#wordcloud'),

			// spinner
			spinner_section: document.querySelector('form > spinner'),
			spinner: new Spinner({
				color: 'white'
			})
		};

		
		config.spinner.stop();

		config.article.addEventListener('transitionend', function() {
			if (config.article.style.maxHeight === '0px') {
				config.article.style.display = 'none';
			}
		});

		config.submit.addEventListener('click', function() {
			clear_article(config);

			var url = config.input.value;

			post('/classify', {
				url: url
			}).then(function(response) {
				article_loaded(config);
				
				setTimeout(function() {
					config.article.style.maxHeight = '900px';
				}, 0);
				config.title.innerText = response.title;

				var data = response.data,
				prediction = organize_prediction(data['prediction']),
				salient_words = normalize_salience(data['salient_words']);

				config.link.href = 'http://reddit.com/r/' + prediction.labels[0] + '/submit/?url=' + 
				window.encodeURI(url) + '&title=' + window.encodeURIComponent(response.title);
				new Chart(config.context).Bar({
					labels: prediction.labels,
					datasets: [{
						fillColor : "rgba(67,72,83,1)",
						strokeColor : "rgba(238, 238, 238, 1)",
						data: prediction.dataset
					}]
				}, config.chart);

				WordCloud(config.wordcloud, {
					rotateRatio: 0.5,
					color: '#434853',
					list: salient_words
				});
			}).catch(function(error) {
				window.alert('Sorry, we couldn\'t parse this url! Try another.');
				logError(error);
			}).then(function() {
				config.spinner.stop();
			});
		});
}

window.addEventListener('DOMContentLoaded', onload);
})(window.WordCloud);