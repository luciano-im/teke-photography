//REPLACE FOR JQUERY READY
//listen for changes to document.readyState - onreadystatechange is fired when readyState value is changed
//Alternative to 'DOMContentLoaded' - when readyState=='interactive' the event DOMContentLoaded was fired
document.onreadystatechange = function () {
	if(document.readyState === 'interactive') {

		function addItemsAjax() {
			var request = new XMLHttpRequest();
			request.open('GET', '/', true);
			request.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

			request.onload = function() {
				if (request.status >= 200 && request.status < 400) {
					// Success!
					var data = JSON.parse(request.response);
					console.log(data);
					var elems = [];
					var fragment = document.createDocumentFragment();
					for (i=0; i<data.length; i++) {
						var elem = getItemElement(data[i]);
						fragment.appendChild(elem);
						elems.push(elem);
					}
					imagesLoaded(elem, function() {
						// append elements to container
						grid.appendChild(fragment);
						msnry.appended(elems);
						msnry.layout();
					});
				} else {
					// Error!
					console.log("Error: "+request.status);
				}
			};

			request.send();
		}

		function getItemElement(url) {
			var img = document.createElement('img');
			img.src = url
			var lnk = document.createElement('a');
			lnk.appendChild(img);
			var figure = document.createElement('figure');
			figure.className = 'grid-item'
			figure.appendChild(lnk);
			return figure
		}

		window.onscroll = function(){
			if ((window.innerHeight + window.scrollY) == document.body.scrollHeight) {
				addItemsAjax();
			}
		}

		function hasClass(elem, className) {
			return new RegExp(' ' + className + ' ').test(' ' + elem.className + ' ');
		}

		function toggleClass(elem, className) {
			var newClass = ' ' + elem.className.replace( /[\t\r\n]/g, ' ' ) + ' ';
			if (hasClass(elem, className)) {
				while (newClass.indexOf(' ' + className + ' ') >= 0 ) {
					newClass = newClass.replace( ' ' + className + ' ' , ' ' );
				}
				elem.className = newClass.replace(/^\s+|\s+$/g, '');
			} else {
				elem.className += ' ' + className;
			}
		}

	}
}