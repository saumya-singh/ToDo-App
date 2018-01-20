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
				var para = document.createElement('p');
				para.textContent = jsonData["data"]["title"];
				divElement.appendChild(para);
			}
			else if (jsonData["status"] == "failure") {
				alert(jsonData["error"]);
			}
    }
		document.getElementById("taskForm").reset();
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
					var div = document.createElement('div');
					div.className = "taskDiv";
					var para = document.createElement('p');
					para.className = "taskPara";
					para.textContent = allTasksInfo[i]["title"];
					var btnDiv = document.createElement('div');
					btnDiv.className = "btnDiv";
					var updateBtn = document.createElement('button');
					updateBtn.className = "taskUpdateBtn";
					var updateText = document.createTextNode("Update");
					updateBtn.appendChild(updateText)
					var deleteBtn = document.createElement('button');
					deleteBtn.className = "taskDeleteBtn";
					var deleteText = document.createTextNode("Delete");
					deleteBtn.appendChild(deleteText)
					btnDiv.appendChild(updateBtn);
					btnDiv.appendChild(deleteBtn);
					div.appendChild(para);
					div.appendChild(btnDiv);
					divElement.appendChild(div);
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
