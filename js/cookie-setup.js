if (typeof(Storage) !== "undefined") {
	// FIXME: Add heads up for user to consent to storage of cookies on their browser.
	// Code for localStorage/sessionStorage.
	// Doing session storage for now so people's browsers don't get STDs
	if (sessionStorage.getItem("theme") === null){
		sessionStorage.setItem("theme", "light");
	}
} else {
	console.log("Cookies are unsupported!");
}