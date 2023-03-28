const express = require("express");
const { spawn } = require("child_process");
const path = require("path");

const app = express();

app.use(express.static(path.join(__dirname, "assets")));
app.use("/bootstrap", express.static(path.join(__dirname, "node_modules", "bootstrap")));
app.use("/@popperjs", express.static(path.join(__dirname, "node_modules", "@popperjs")));
app.use("/jquery", express.static(path.join(__dirname, "node_modules", "jquery")));
app.use("/font-awesome", express.static(path.join(__dirname, "node_modules", "font-awesome")));

app.get("/", function (req, res) {
	let dataToSend;
	// spawn new child process to call the python script
	const python = spawn("python", [path.join(__dirname, "/script.py")]);
	// collect data from script
	python.stdout.on("data", function (data) {
		console.log("Pipe data from python script ...");
		dataToSend = data.toString();
		console.log(dataToSend);
	});

	// in close event we are sure that stream from child process is closed
	python.on("close", (code) => {
		console.log(`child process close all stdio with code ${code}`);
		// send data to browser
		// console.log(dataToSend);
	});

	console.log("hi");
	res.sendFile(path.join(__dirname, "/index.html"));
});

let listener = app.listen(process.env.PORT || 3000, function () {
	console.log("Server running at http://localhost:" + listener.address().port);
});
