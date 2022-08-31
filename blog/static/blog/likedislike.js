/*  likedislike.js
    This program sends an AJAX POST request
    to indicate a like or disklike on a comment
*/

function likeHandler(event) {
	event.preventDefault();
  
  // Get the element that was clicked on. It's the event
  // currentTarget property.
  const element = event.currentTarget;
  let href = element.href;
  if(href.substr(-5)!="like/") return;
  element.href="/";
  
  const response = fetch(href, {
    method: 'POST',
    // Set the CSRF token header
    headers: { 'X-CSRFToken': csrftoken,
        "Content-Type": "application/x-www-form-urlencoded" },
    credentials: 'include',
    body: [],
  })
  .then(response => response.text())
  // Get a response, then call listSuccess function
  .then(function(response) {
    let ht = element.innerHTML.trim();
    let sp = ht.lastIndexOf(" ");
    let val = parseInt(ht.substr(sp+1)) + 1;
    element.innerHTML = ht.substr(0, sp + 1) + val;
  });

	
}

// Select multiple classes: both like & dislike buttons
document.querySelectorAll('.like, .dislike')
	.forEach(function (link) {
		link.addEventListener('click', likeHandler);
	});