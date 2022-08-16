function createPosts(start, end) {
	fetch(`/posts?start=${start}&end=${end}`)
		.then((result) => result.json())
		.then((result) => {
			result.forEach((post) => {
				const data = post["fields"];
				createPost(data["topic"], data["content"]);
			});
		});
}

function createPost(name, content) {
	const post = document.createElement("div");
	post.className = "post";

	const postHeader = document.createElement("h4");
	postHeader.className = "postHeader";
	postHeader.innerHTML = name;
	post.appendChild(postHeader);

	const postContent = document.createElement("p");
	postContent.className = "postContent";
	postContent.innerHTML = content;
	post.appendChild(postContent);

	document.querySelector(".posts").appendChild(post);
}
