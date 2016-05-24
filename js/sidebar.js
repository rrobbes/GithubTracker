for (var i in projects_json.semester) {
  $('#side-menu').append('<ul class="nav" id="side-menu"> <li> <a href="#" onclick="general_view(\''+projects_json.semester[i]+'\')"><i class="fa"></i>'+projects_json.semester[i]+'<span class="fa arrow"></span></a> <ul class="nav nav-second-level"> <li> <a href="#" onclick="show_commits(\''+projects_json.semester[i]+'\')"><i class="fa fa-clock-o"></i> Commits</a> </li><li> <a href="flot.html"><i class="fa fa-exclamation-circle"></i> Issues</a> </li><li> <a href="flot.html"><i class="fa fa-comments"></i> Comments</a> </li></ul> </li></ul>')
}
