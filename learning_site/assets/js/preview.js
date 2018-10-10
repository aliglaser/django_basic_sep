function Editor(input, preview){
	console.log(input);
	this.update = function(){
		preview.innerHTML = markdown.toHTML(input.value);
	};
	input.editor = this;
	this.update();
}

django.jQuery(document).ready(fundtion(){
	new Editor(django.jQuery("#id_description")[0],
django.jQuery("#preview")[0]);
});
