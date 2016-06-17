/* Inicialización en español para la extensión 'UI date picker' para jQuery. */
/* Traducido por Vester (xvester@gmail.com). */
( function( factory ) {
	if ( typeof define === "function" && define.amd ) {

		// AMD. Register as an anonymous module.
		define( [ "../widgets/datepicker" ], factory );
	} else {

		// Browser globals
		factory( jQuery.datepicker );
	}
}( function( datepicker ) {

datepicker.regional.es = {
	dateFormat: "yy-mm-dd",
	firstDay: 1,
	isRTL: false,
	showMonthAfterYear: false,
	yearSuffix: "" };
datepicker.setDefaults( datepicker.regional.es );

return datepicker.regional.es;

} ) );

var init_date = new Date("March 3, 2016");
var final_date = new Date();

$("#datepicker-final").datepicker({minDate: init_date, maxDate: new Date()});
$("#datepicker-final").val(""+final_date.getFullYear()+"-"+(final_date.getMonth()+1)+"-"+final_date.getDate());
$("#datepicker-init").datepicker();
$("#datepicker-init").val(""+init_date.getFullYear()+"-"+(init_date.getMonth()+1)+"-"+init_date.getDate());

function updateDates() {
	init_date = new Date($("#datepicker-init").val());
	final_date = new Date($("#datepicker-final").val());
	$('#page-wrapper').html('');
}
