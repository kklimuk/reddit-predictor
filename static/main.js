(function() {
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

	var config = {
		submit: null,
		input: null,
		title: null,
		article: null,
		context: null
	};
	function onload() {
		config.submit = document.querySelector('form button');
		config.input = document.querySelector('form input');
		config.title = document.querySelector('form > article h1');
		config.article = document.querySelector('form > article');
		config.context = document.querySelector('article canvas').getContext('2d');

		config.submit.addEventListener('click', function() {
			post('/classify', {
				url: config.input.value
			}).then(function(response) {
				config.article.style.display = 'block';
				setTimeout(function() {
					config.article.style.maxHeight = '550px';
				}, 0);
				config.title.innerText = response.title;

				new Chart(config.context).Bar({
					labels: Object.keys(response.data),
					datasets: [{
						fillColor : "rgba(151,187,205,0.5)",
						strokeColor : "rgba(151,187,205,1)",
						data: Object.keys(response.data).map(function(key) {
							return response.data[key];
						})
					}]
				}, {
					scaleShowGridLines: false,
					scaleStepWidth: 20,
					scaleSteps: 5
				});
			}).catch(function(error) {
				window.alert('Sorry, we couldn\'t parse this url! Try another.');
				logError(error);
			});
		});
	}

	window.addEventListener('DOMContentLoaded', onload);
})();