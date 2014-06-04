$(document).ready(function(){

	$(".btn-collapse-sidebar-right").click(function(){
		$(".sidebar-right").toggleClass("toggle-left");
		$(".sidebar-right-heading").toggleClass("toggle-left");
		$(".page-content").toggleClass("toggle-left");
	});
	
});