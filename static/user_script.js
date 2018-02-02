function register() {
  var form = document.getElementById('registerForm');
  form.addEventListener('submit', function(e) {
      e.preventDefault();
  }, false);
  json_data = toJSONString(form);
  var XHR = new XMLHttpRequest();
  XHR.open('POST', '/api/register/');
  XHR.setRequestHeader('Content-Type', 'application/json;charset=UTF-8');
  XHR.send(json_data);
  XHR.onload = function() {
      var res = XHR.responseText;
      jsonData = JSON.parse(res);
      if (jsonData['status'] == 'success') {
          window.location.href = '/login/'
      } else if (jsonData['status'] == 'failure') {
          alert(jsonData['error']);
      }
  }
}

function login() {
  var form = document.getElementById('loginForm');
  form.addEventListener('submit', function(e) {
      e.preventDefault();
  }, false);
  json_data = toJSONString(form);
  var XHR = new XMLHttpRequest();
  XHR.open('POST', '/api/login/');
  XHR.setRequestHeader('Content-Type', 'application/json;charset=UTF-8');
  XHR.send(json_data);
  XHR.onload = function() {
      var res = XHR.responseText;
      jsonData = JSON.parse(res);
      if (jsonData['status'] == 'success') {
        window.location.href = '/tasks/'
      } else if (jsonData['status'] == 'failure') {
          alert(jsonData['error']);
      }
  }
}

function toJSONString(form) {
    var obj = {};
    var elements = form.querySelectorAll('input, textarea');
    for (var i = 0; i < elements.length; ++i) {
        var element = elements[i];
        var name = element.name;
        var value = element.value;
        if (name) {
            obj[name] = value;
        }
    }
    return JSON.stringify(obj);
}

function signin() {
    window.location.href = '/login/'
}
