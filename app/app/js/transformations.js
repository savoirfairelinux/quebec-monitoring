$(document).ready(function(){
	if($('html').hasClass('svg')){
		$( ".switch-svg" ).each(function() {
			var targetClass = this;
		  	changeForSvg(targetClass);
		});
	}
});

function changeForSvg(oneImage){
	var srcInitial = $(oneImage).attr('src');
	var nouvelleSrc = srcInitial.replace("png","svg");
	$(oneImage).attr('src',nouvelleSrc);
}
