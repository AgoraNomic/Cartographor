var stats = ["type", "ownership"];

function getStats(x, y) {
	s = document.getElementById("stats");
	s.innerHTML = "lat: " + y + "<br>long: " + x + "<br>";
	for (var i = 0; i < stats.length; i++) {
		s.innerHTML += stats[i] + ": " + document.getElementById("r" + y + "c" + x).getAttribute(stats[i]) + "<br>";
	}
}