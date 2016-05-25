for (var i in projects_json.semester) {
  $('#side-menu').append('<ul class="nav" id="side-menu"> <li> <a href="#" onclick="general_view(\''+projects_json.semester[i]+'\')"><i class="fa"></i>'+projects_json.semester[i]+'<span class="fa arrow"></span></a> </li></ul>')
}
