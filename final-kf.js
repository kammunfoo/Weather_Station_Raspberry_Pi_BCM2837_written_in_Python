function popup() {
	alert("Welcome To The Weather Station! \nCheck The Weather Before You Go Out.")
}

function highlight(x) {
	document.getElementById(x).style.color = "red";
	document.getElementById(x).style.fontSize = "20px";
}

function reset(x) {
	document.getElementById(x).style.color = "black";
	document.getElementById(x).style.fontSize = "16px";
}
