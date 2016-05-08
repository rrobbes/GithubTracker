function show_commits(project) {
  project = project.replace(/\s+/g, '');
  var url = "../Jsons/"+project+".json";
  $.getJSON(url, function(json) {
    $('#page-wrapper').html('');
    $('#page-wrapper').append('<div class="row"> <div class="col-lg-12"> <h1 class="page-header">Commits - '+project+'</h1> </div></div>');
    $('#page-wrapper').append('<div class="row"><div class="col-lg-12"> <div class="panel panel-primary"> <div class="panel-heading"> Ismael Alvarez (IsmaelAlvarez)<div class="pull-right">Total: 1</div> </div><div class="panel-body"> <p>message: Solucionado problema con gradle/maven<br>time: 2016-04-27 19:05:00<br>url: <a target="_blank" href="https://github.com/IsmaelAlvarez/logisim/commit/0953d5355dca7044b651c1f246314842af7d1674">https://github.com/IsmaelAlvarez/logisim/commit/0953d5355dca7044b651c1f246314842af7d1674</a></p></div></div></div></div>')
  })
}

function general_view(project) {
  project = project.replace(/\s+/g, '');
  var url = "../Jsons/"+project+".json";
  $.getJSON(url, function(json) {
    $('#page-wrapper').html('');
    $('#page-wrapper').append('<div class="row"> <div class="col-lg-12"> <h1 class="page-header">Review - '+project+'</h1> </div></div>');
    $('#page-wrapper').append('<div id="bar"></div>');
    var datas = [];
    for (var i in json) {
      var d = {user: json[i].user, commits: json[i].commits.length, issues: json[i].issues.length, comments: json[i].comments.length};
      datas.push(d);
    }
    Morris.Bar({
      element: 'bar',
      data: datas,
      xkey: 'user',
      ykeys: ['commits', 'issues', 'comments'],
      labels: ['Commits', 'Issues', 'Comentarios'],
      stacked: true,
      resize:true
    });
  });
}
