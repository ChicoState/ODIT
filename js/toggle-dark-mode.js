function tdm(){
	if (sessionStorage.getItem("theme") === "light"){
		sessionStorage.setItem("theme", "dark");
		$("#toggle-dark-mode").html("🌑");
		$("#style").attr("href", "styles-dark.css");
	} else {
		sessionStorage.setItem("theme", "light");
		$("#toggle-dark-mode").html("☀️");
		$("#style").attr("href", "styles.css");
	}
}