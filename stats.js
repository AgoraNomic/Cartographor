var stats = ["type"];

function getStats(x, y) {
	s = document.getElementById("stats");
	s.innerHTML = "";
	for (var i = 0; i < stats.length; i++) {
		s.innerHTML += stats[i] + ": " + document.getElementById("r" + y + "c" + x).getAttribute(stats[i]);
	}
}