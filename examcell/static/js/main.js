$(function(){
	$("#apply-menu").click(function(event){
		event.preventDefault();
		$("#content").load("/apply");
	});
});
