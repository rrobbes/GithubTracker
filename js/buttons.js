function length_by_dates(element) {
  var l = 0;
  for (var j in element) {
    if (Date.parse(element[j].time) >= Date.parse(init_date) && Date.parse(element[j].time) <= Date.parse(final_date)) {
      l++;
    }
  }
  return l;
}

function length_by_date(element, date) {
  var l = 0;
  for (var j in element) {
    var ti = new Date(Date.parse(element[j].time));
    if (ti.getDate() == date.getDate() && ti.getMonth() == date.getMonth() && ti.getFullYear() == date.getFullYear()) {
      l++;
    }
  }
  return l;
}

function show_commits(json, i) {
  var commits = '<div class="panel panel-primary"> <div class="panel-heading">commits<div class="pull-right">Total: '+length_by_dates(json[i].commits)+'</div> </div><div class="panel-body"> ';
  for (var j in json[i].commits) {
    if (Date.parse(json[i].commits[j].time) >= Date.parse(init_date) && Date.parse(json[i].commits[j].time) <= Date.parse(final_date)) {
      commits = commits+'<p><b>message: '+json[i].commits[j].message+'</b><br>time: '+json[i].commits[j].time+'<br>branch: <a href="'+json[i].commits[j].branch_link+'">'+json[i].commits[j].branch+'</a><br>additions: <span class="text-success">'+json[i].commits[j].additions+'</span><br>deletions: <span class="text-danger">'+json[i].commits[j].deletions+'</span><br>url: <a target="_blank" href="'+json[i].commits[j].url+'">'+json[i].commits[j].url+'</a></p><hr>';
    }
  }
  commits = commits+'</div></div>'
  return commits;
}

function show_comments(json, i) {
  var comments = '<div class="panel panel-primary"> <div class="panel-heading">comments<div class="pull-right">Total: '+length_by_dates(json[i].comments)+'</div> </div><div class="panel-body"> ';
  for (var j in json[i].comments) {
    if (Date.parse(json[i].comments[j].time) >= Date.parse(init_date) && Date.parse(json[i].comments[j].time) <= Date.parse(final_date)) {
      comments = comments+'<p>message: '+json[i].comments[j].comment+'<br>time: '+json[i].comments[j].time+'<br>url: <a target="_blank" href="'+json[i].comments[j].url+'">'+json[i].comments[j].url+'</a></p><hr>';
    }
  }
  comments = comments+'</div></div>'
  return comments;
}

function parse_issues(json) {
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
  return users_issues;
}

function show_issues(json, i) {
  var users_issues = parse_issues(json);
  var converter = new Markdown.Converter();
  var issues = '<div class="panel panel-primary"> <div class="panel-heading">issues assigned<div class="pull-right">Total: '+length_by_dates(users_issues[i])+'</div> </div><div class="panel-body"> ';
  for (var j in users_issues[i]) {
    if (Date.parse(users_issues[i][j].time) >= Date.parse(init_date) && Date.parse(users_issues[i][j].time) <= Date.parse(final_date)) {
      issues = issues+'<p><b>'+users_issues[i][j].title+'</b><br>'+converter.makeHtml(users_issues[i][j].body)+'<br>time: '+users_issues[i][j].time+'<br>url: <a target="_blank" href="'+users_issues[i][j].url+'">'+users_issues[i][j].url+'</a></p><hr>';
    }
  }
  issues = issues+'</div></div>'
  return issues;
}


function general_view(project) {
  project = project.replace(/\s+/g, '');
  var project_index = projects_json.semester.indexOf(project);
  var json = json_list[project_index];
  var users_issues = parse_issues(json);
  $('#page-wrapper').html('');
  $('#page-wrapper').append('<div class="row"> <div class="col-lg-12"> <h1 class="page-header">Review - '+project+'</h1> </div></div>');
  $('#page-wrapper').append('<div id="bar"></div>');
  $('#page-wrapper').append('<div class="row"> <div class="col-lg-12"><h2 class="page-header" id="user-info-name"></h2><div style="overflow-x: scroll; margin-bottom: 20px;" id="user-info-graph"></div><div id="user-info-body"></div></div></div>');
  var datas = [];
  for (var i in json) {
    var usr_name = json[i].nombre.substring(json[i].nombre.indexOf(" ") + 1);
    var d = {nombre: usr_name, commits: length_by_dates(json[i].commits), issues: length_by_dates(users_issues[i]), comments: length_by_dates(json[i].comments), user: json[i].user};
    datas.push(d);
  }
  Morris.Bar({
    element: 'bar',
    data: datas,
    xkey: 'nombre',
    ykeys: ['commits', 'issues', 'comments'],
    labels: ['Commits', 'Issues', 'Comments'],
    stacked: true,
    resize:true
  }).on('click', function(i, row){
    show_user_info(json, i);
  });
}

function show_user_graph(json, i) {
  var users_issues = parse_issues(json);
  var datas = [];
  var days = 0;
  for (var d = new Date(Date.parse(init_date)); d <= final_date; d.setDate(d.getDate() + 1)) {
    days++;
    var o = { date: ''+d.getDate()+'/'+(d.getMonth()+1),
              commits: length_by_date(json[i].commits, d),
              issues: length_by_date(users_issues[i], d),
              comments: length_by_date(json[i].comments, d)};
    datas.push(o);
  }
  $('#user-info-graph').html('<div style="width: '+30*days+'px; min-width: 100%;" id="bar_user"></div>')
  Morris.Bar({
    element: 'bar_user',
    data: datas,
    xkey: 'date',
    ykeys: ['commits', 'issues', 'comments'],
    labels: ['Commits', 'Issues', 'Comments'],
    stacked: true,
    resize:true
  })
}

function show_user_info(json, i) {
  $('#user-info-name').html(json[i].nombre);
  var commits = show_commits(json, i);
  var issues = show_issues(json, i);
  var comments = show_comments(json, i);
  $('#user-info-body').html(commits+issues+comments)
  show_user_graph(json, i);
}
