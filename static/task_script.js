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
				innerdiv.className = "taskMainDiv";
				innerdiv.id = jsonData["data"]["_id"];
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
			//var targetDiv = document.getElementById(id).getElementsByClassName("taskPara")[0];
			document.getElementById(id).getElementsByClassName("taskPara")[0].innerHTML = jsonData["data"]["title"];
			var targetDiv = document.getElementById(id).getElementsByClassName("taskDetail")[0];
			if (targetDiv.style.display === "block") {
				targetDiv.innerHTML = taskDetailsMarkup(jsonData["data"]);
			}
			// document.getElementById(id).getElementsByClassName("title")[0].innerHTML = jsonData["data"]["title"];
			// document.getElementById(id).getElementsByClassName("description")[0].innerHTML = jsonData["data"]["description"];
			// document.getElementById(id).getElementsByClassName("deadline")[0].innerHTML = jsonData["data"]["deadline"];
			//document.getElementById(id).innerHTML = jsonData["data"]["title"];
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

function updateTask(id) {
	document.getElementById("formHeading").innerHTML = "Update Task";
	document.getElementById("formButton").innerHTML = "Update";
	//taskDetails = JSON.parse(decodeURIComponent(taskInfo));
	//var id  = taskDetails["_id"];
	var XHR = new XMLHttpRequest();
	var url = "/api/users/123/tasks/" + id + "/";
	XHR.open("GET", url);
	//XHR.send();
	XHR.onload = function() {
	var res = XHR.responseText;
	//var divElement = document.querySelector('.taskContainer');
	jsonData = JSON.parse(res);
	console.log(jsonData)
	if (jsonData["status"] == "success"){
		document.getElementById("title").value = jsonData["data"]["title"];
		document.getElementById("description").value = jsonData["data"]["description"];
		//var date = taskDetails["deadline"];
		document.getElementById("deadline").value = jsonData["data"]["deadline"];
		document.getElementById("formButton").onclick = function() { update(id); };
	}
	else if (jsonData["status"] == "failure") {
		alert(jsonData["error"]);
	}
}
XHR.send();
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

function taskDetailsMarkup(taskInfo) {
	var taskDetailsMarkup = `<p class = "title">Title: ${taskInfo["title"]}</p>
		<p class = "description">Description: ${taskInfo["description"]}</p>
		<p class = "deadline">Deadline: ${taskInfo["deadline"]}</p>
		<p class = "completionStatus">Completion Status: ${taskInfo["completed"]}</p>
		<p class = "createdBy">Created By: ${taskInfo["created_by"]}</p>
		<p class = "createdTime">Created Time: ${taskInfo["created_time"]}</p>`
	return taskDetailsMarkup
}

function taskDetails(id) {
		 	 var targetDiv = document.getElementById(id).getElementsByClassName("taskDetail")[0];
		   if (targetDiv.style.display === "none") {
			 		var XHR = new XMLHttpRequest();
			 		var url = "/api/users/123/tasks/" + id + "/";
					XHR.open("GET", url);
					//XHR.send();
					XHR.onload = function() {
					var res = XHR.responseText;
					//var divElement = document.querySelector('.taskContainer');
					jsonData = JSON.parse(res);
					if (jsonData["status"] == "success"){
					targetDiv.innerHTML = taskDetailsMarkup(jsonData["data"]);
		      targetDiv.style.display = "block";
		      }
				  else if (jsonData["status"] == "failure") {
						alert(jsonData["error"]);
				 	}
				}
				XHR.send();
			}
			  else {
		       targetDiv.style.display = "none";
		   }
}

function taskMarkup(taskInfo) {
	//dataDetails = encodeURIComponent(JSON.stringify(taskInfo));
	//deleteData = taskInfo["_id"]
	var taskMarkup = `<div class = "taskDiv"><p class = "taskPara">${taskInfo["title"]}</p>
		<div class = "btnDiv">
			<button class = "taskDetailBtn" onclick = "taskDetails('${taskInfo["_id"]}')">Details</button>
			<button class = "taskUpdateBtn" onclick = "updateTask('${taskInfo["_id"]}')">Update</button>
			<button class = "taskDeleteBtn" onclick = "deleteTask('${taskInfo["_id"]}')">Delete</button>
		</div></div>
		<div style="display:none" class = "taskDetail"></div>`
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
					innerdiv.className = "taskMainDiv";
					innerdiv.id = allTasksInfo[i]["_id"];
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
