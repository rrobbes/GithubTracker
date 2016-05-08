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
    Morris.Bar({
      element: 'bar',
      data: [
      { user: 'Ismael', commits: 1, issues: 3, comments: 2 },
      { user: 'Rodrigo', commits: 2,  issues: 5, comments: 0 },
      { user: 'Ana', commits: 2,  issues: 3, comments: 0 },
      { user: 'Patricio', commits: 5,  issues: 2, comments: 0 },
      { user: 'Matias', commits: 0,  issues: 0, comments: 1 },
      { user: 'Matilde', commits: 1,  issues: 2, comments: 1 },
      { user: 'Andrea', commits: 2, issues: 4, comments: 1 }
      ],
      xkey: 'user',
      ykeys: ['commits', 'issues', 'comments'],
      labels: ['Commits', 'Issues', 'Comentarios'],
      stacked: true,
      resize:true
    });
  });
}
