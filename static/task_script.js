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
		document.getElementById("taskForm").reset();
}

function updateTask(id) {
	console.log(id)
}

function deleteTask(id) {
	//console.log(id)
	var url = "/api/users/123/tasks/" + id + "/"
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
	var taskMarkup = `<p class = "taskPara">${taskInfo["title"]}</p>
		<div class = "btnDiv">
			<button class = "taskUpdateBtn" id = "${taskInfo["_id"]}" target = "_blank" onclick = "updateTask('${taskInfo["_id"]}')">Update</button>
			<button class = "taskDeleteBtn" id = "${taskInfo["_id"]}" target = "_blank" onclick = "deleteTask('${taskInfo["_id"]}')">Delete</button>
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
