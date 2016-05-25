function show_commits(project) {
  project = project.replace(/\s+/g, '');
  var project_index = projects_json.semester.indexOf(project);
  var json = json_list[project_index];
  $('#page-wrapper').html('');
  $('#page-wrapper').append('<div class="row"> <div class="col-lg-12"> <h1 class="page-header">Commits - '+project+'</h1> </div></div>');
  for (var i in json) {
    var body = '<div class="row"><div class="col-lg-12"> <div class="panel panel-primary"> <div class="panel-heading">'+json[i].nombre+' ('+json[i].user+')'+ '<div class="pull-right">Total: '+json[i].commits.length+'</div> </div><div class="panel-body"> ';
    for (var j in json[i].commits) {
      body = body+'<p><b>message: '+json[i].commits[j].message+'</b><br>time: '+json[i].commits[j].time+'<br>branch: '+json[i].commits[j].branch+'<br>additions: <span class="text-success">'+json[i].commits[j].additions+'</span><br>deletions: <span class="text-danger">'+json[i].commits[j].deletions+'</span><br>url: <a target="_blank" href="'+json[i].commits[j].url+'">'+json[i].commits[j].url+'</a></p><hr>';
    }
    body = body+'</div></div></div></div>'
    $('#page-wrapper').append(body);
  }
}

function show_comments(project) {
  project = project.replace(/\s+/g, '');
  var project_index = projects_json.semester.indexOf(project);
  var json = json_list[project_index];
  $('#page-wrapper').html('');
  $('#page-wrapper').append('<div class="row"> <div class="col-lg-12"> <h1 class="page-header">Comments - '+project+'</h1> </div></div>');
  for (var i in json) {
    var body = '<div class="row"><div class="col-lg-12"> <div class="panel panel-primary"> <div class="panel-heading">'+json[i].nombre+' ('+json[i].user+')'+ '<div class="pull-right">Total: '+json[i].comments.length+'</div> </div><div class="panel-body"> ';
    for (var j in json[i].comments) {
      body = body+'<p>message: '+json[i].comments[j].comment+'<br>time: '+json[i].comments[j].time+'<br>url: <a target="_blank" href="'+json[i].comments[j].url+'">'+json[i].comments[j].url+'</a></p><hr>';
    }
    body = body+'</div></div></div></div>'
    $('#page-wrapper').append(body);
  }
}

function show_issues(project) {
  project = project.replace(/\s+/g, '');
  var project_index = projects_json.semester.indexOf(project);
  var json = json_list[project_index];
  var users_issues = [];
  for (var i in json) {
    users_issues[i] = [];
  }
  for (var i in json) { // recorro los usuarios
    for (var j in json[i].issues) { // recorro las issues creadas por ese usuario
      for (u in json) { // agrego a la lista del usuario la issue si la issue asignada
        if (json[i].issues[j].assigned == json[u].user) {
          users_issues[u].push(json[i].issues[j]);
        }
      }
    }
  }
  var converter = new Markdown.Converter();
  $('#page-wrapper').html('');
  $('#page-wrapper').append('<div class="row"> <div class="col-lg-12"> <h1 class="page-header">Issues assigned to - '+project+'</h1> </div></div>');
  for (var i in json) {
    var body = '<div class="row"><div class="col-lg-12"> <div class="panel panel-primary"> <div class="panel-heading">'+json[i].nombre+' ('+json[i].user+')'+ '<div class="pull-right">Total: '+users_issues[i].length+'</div> </div><div class="panel-body"> ';
    for (var j in users_issues[i]) {
      body = body+'<p><b>'+users_issues[i][j].title+'</b><br>'+converter.makeHtml(users_issues[i][j].body)+'<br>time: '+users_issues[i][j].time+'<br>url: <a target="_blank" href="'+users_issues[i][j].url+'">'+users_issues[i][j].url+'</a></p><hr>';
    }
    body = body+'</div></div></div></div>'
    $('#page-wrapper').append(body);
  }
}


function general_view(project) {
  project = project.replace(/\s+/g, '');
  var project_index = projects_json.semester.indexOf(project);
  var json = json_list[project_index];
  var users_issues = [];
  for (var i in json) {
    users_issues[i] = [];
  }
  for (var i in json) { // recorro los usuarios
    for (var j in json[i].issues) { // recorro las issues creadas por ese usuario
      for (u in json) { // agrego a la lista del usuario la issue si la issue asignada
        if (json[i].issues[j].assigned == json[u].user) {
          users_issues[u].push(json[i].issues[j]);
        }
      }
    }
  }
  $('#page-wrapper').html('');
  $('#page-wrapper').append('<div class="row"> <div class="col-lg-12"> <h1 class="page-header">Review - '+project+'</h1> </div></div>');
  $('#page-wrapper').append('<div id="bar"></div>');
  var datas = [];
  for (var i in json) {
    var usr_name = json[i].nombre.substring(json[i].nombre.indexOf(" ") + 1);
    var d = {user: usr_name, commits: json[i].commits.length, issues: users_issues[i].length, comments: json[i].comments.length};
    datas.push(d);
  }
  Morris.Bar({
    element: 'bar',
    data: datas,
    xkey: 'user',
    ykeys: ['commits', 'issues', 'comments'],
    labels: ['Commits', 'Issues', 'Comments'],
    stacked: true,
    resize:true
  });
}
