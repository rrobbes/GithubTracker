function show_commits(project) {
  project = project.replace(/\s+/g, '');
  var url = "../Jsons/"+project+".json";
  $.getJSON(url, function(json) {
    $('#page-wrapper').html('');
    $('#page-wrapper').append('<div class="row"> <div class="col-lg-12"> <h1 class="page-header">Commits - '+project+'</h1> </div></div>');
    for (var i in json) {
      $('#page-wrapper').append('<div class="row"><div class="col-lg-12"> <div class="panel panel-primary"> <div class="panel-heading">'+json[i].nombre+' ('+json[i].user+')'+ '<div class="pull-right">Total: '+json[i].commits.length+'</div>')
      for (var j in json[i].commits) {
        $('#page-wrapper').append('<div class="panel-body"> <p>message: '+json[i].commits[j].message+'<br>time: '+json[i].commits[j].time+'<br>url: <a target="_blank" href="'+json[i].commits[j].url+'">'+json[i].commits[j].url+'</a></p></div>')
      }
      $('#page-wrapper').append('</div></div></div>');
    }
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
      var usr_name = json[i].nombre.substring(json[i].nombre.indexOf(" ") + 1);
      var d = {user: usr_name, commits: json[i].commits.length, issues: json[i].issues.length, comments: json[i].comments.length};
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
  });
}
