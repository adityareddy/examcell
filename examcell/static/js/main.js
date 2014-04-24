$(function(){
	$("#apply-menu").click(function(){
		$("#content").load("apply.php");
	});
	
	$("#edit-subjects-menuitem").click(function(){
		$("#edit-subjects-menuitem-content").load("editsubjects.html");
	});
	$("#condonation-menuitem").click(function(){
		$("#condonation-menuitem-content").load("condonation.html");
	});
	$("#detained-menuitem").click(function(){
		$("#detained-menuitem-content").load("detained.html");
	});
});
