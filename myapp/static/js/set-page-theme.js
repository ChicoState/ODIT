function load_theme(){
	if (sessionStorage.getItem("theme") === "light"){
		$("#toggle-dark-mode").html("☀️");
		$("#style").attr("href", "{% static "styles.css" %}");
	} else {
		$("#toggle-dark-mode").html("🌑");
		$("#style").attr("href", "{% static "styles-dark.css" %}");
	}
}
// Toggle dark mode
function tdm(){
	if (sessionStorage.getItem("theme") === "light"){
		sessionStorage.setItem("theme", "dark");
		$("#toggle-dark-mode").html("🌑");
		$("#style").attr("href", "{% static "styles-dark.css" %}");
	} else {
		sessionStorage.setItem("theme", "light");
		$("#toggle-dark-mode").html("☀️");
		$("#style").attr("href", "{% static "styles.css" %}");
	}
}