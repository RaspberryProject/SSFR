$(document).ready(function(){
	$('#mealSuggestForm').ajaxForm({
		dataType: 'json',
		success: function(formData){
			if(formData.result){
				$(".successMsg").html("");
				$(".successMsg").append(formData.msg);
				$(".successMsg").removeClass('hide');
				$(".errorMsg").addClass('hide');
				$(".mealTable").addClass("hide");
			}
			else{
				$(".errorMsg").html("");
				$(".errorMsg").append(formData.msg);
				$(".errorMsg").removeClass('hide');
				$(".successMsg").addClass('hide');
				if(formData.needs.length > 0){
					console.log(formData.needs);
					$("#mealTableBody").html("");
					var html = "";
					for(var i = 0; i < formData.needs.length; i++){
						html += "<tr><td>"+ formData.needs[i].product +"</td><td>"
								+ formData.needs[i].amount_need + "</td><td>" 
								+ formData.needs[i].count_need + "</td></tr>";
					}
					$("#mealTableBody").html(html);
					$(".mealTable").removeClass("hide");
				}
			}
		}
	});
});