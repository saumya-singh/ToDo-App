function insert() {
		var form = document.getElementById( "taskForm" );
		form.addEventListener( "submit", function(e) {
			e.preventDefault();
		}, false);
		json_data = toJSONString( form );
		var XHR = new XMLHttpRequest();
		XHR.open("POST", "/api/users/123/tasks/");
		XHR.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
		XHR.send(JSON.stringify(json_data));
		XHR.onload = function() {
			var res = XHR.responseText;
			var divElement = document.querySelector('.taskContainer');
			jsonData = JSON.parse(res);
			if (jsonData["status"] == "success"){
				var innerdiv = document.createElement('div');
				innerdiv.className = "taskDiv";
				innerdiv.innerHTML = taskMarkup(jsonData["data"]);
				divElement.appendChild(innerdiv);
			}
			else if (jsonData["status"] == "failure") {
				alert(jsonData["error"]);
			}
    }
}

function update(id) {
	var form = document.getElementById( "taskForm" );
	form.addEventListener( "submit", function(e) {
		e.preventDefault();
	}, false);
	json_data = toJSONString( form );
	var XHR = new XMLHttpRequest();
	var url = "/api/users/123/tasks/" + id + "/";
	XHR.open("PUT", url);
	XHR.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
	XHR.send(json_data);
	XHR.onload = function() {
		var res = XHR.responseText;
		jsonData = JSON.parse(res);
		var divElement = document.querySelector('.taskContainer');
		if (jsonData["status"] == "success"){
			document.getElementById(id).innerHTML = jsonData["data"]["title"];
		}
		else if (jsonData["status"] == "failure") {
			alert(jsonData["error"]);
		}
	}
	document.getElementById("formHeading").innerHTML = "Add Task";
	document.getElementById("formButton").innerHTML = "Add";
	document.getElementById("formButton").onclick = insert;
	document.getElementById("taskForm").reset();
}

function updateTask(taskInfo) {
	taskDetails = JSON.parse(decodeURIComponent(taskInfo));
	var id  = taskDetails["_id"];
	document.getElementById("formHeading").innerHTML = "Update Task";
	document.getElementById("formButton").innerHTML = "Update";
	document.getElementById("title").value = taskDetails["title"];
	document.getElementById("description").value = taskDetails["description"];
	//var date = taskDetails["deadline"];
	document.getElementById("deadline").value = taskDetails["deadline"];
	document.getElementById("formButton").onclick = function() { update(id); };
}

function deleteTask(id) {
	var url = "/api/users/123/tasks/" + id + "/";
	var XHR = new XMLHttpRequest();
	XHR.open("DELETE", url);
	XHR.send();
	XHR.onload = function() {
		var res = XHR.responseText;
		//var divElement = document.querySelector('.taskContainer');
		jsonData = JSON.parse(res);
		if (jsonData["status"] == "success"){
			var divElement = document.getElementById("taskCon");
			var divChild = document.getElementById(id);
			var throwawayNode = divElement.removeChild(divChild);
		}
		else if (jsonData["status"] == "failure") {
			alert(jsonData["error"]);
		}
	 }
 }

function taskMarkup(taskInfo) {
	updateData = encodeURIComponent(JSON.stringify(taskInfo));
	deleteData = taskInfo["_id"]
	var taskMarkup = `<p id = "${taskInfo["_id"]}" class = "taskPara">${taskInfo["title"]}</p>
		<div class = "btnDiv">
			<button class = "taskUpdateBtn" onclick = "updateTask('${updateData}')">Update</button>
			<button class = "taskDeleteBtn" onclick = "deleteTask('${deleteData}')">Delete</button>
		</div>`
	return taskMarkup
}

function listAllTasks() {
		var XHR = new XMLHttpRequest();
		XHR.open("GET", "/api/users/123/tasks/");
		XHR.send();
		XHR.onload = function() {
			var res = XHR.responseText;
			var divElement = document.querySelector('.taskContainer');
			jsonData = JSON.parse(res);
			if (jsonData["status"] == "success"){
				var allTasksInfo = jsonData["data"];
				for (var i = 0; i < allTasksInfo.length; i++) {
					var innerdiv = document.createElement('div');
					innerdiv.className = "taskDiv";
					innerdiv.innerHTML = taskMarkup(allTasksInfo[i]);
					divElement.appendChild(innerdiv);
				}
			}
			else if (jsonData["status"] == "failure") {
				alert(jsonData["error"]);
			}
		}
}

function toJSONString(form) {
		var obj = {};
		var elements = form.querySelectorAll("input, textarea");
		for( var i = 0; i < elements.length; ++i ) {
			var element = elements[i];
			var name = element.name;
			var value = element.value;
			if( name ) {
				obj[ name ] = value;
			}
		}
  return JSON.stringify(obj);
}
