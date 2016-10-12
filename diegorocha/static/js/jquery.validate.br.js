jQuery.extend(jQuery.validator.messages, {
	required: "Campo obrigatório.",
	remote: "Please fix this field.",
	email: "Por favor insira um endereço de e-mail válido.",
	url: "Por favor insira uma url válida.",
	date: "Por favor insira uma data válida.",
	dateISO: "Por favor insira uma data válida (Formato ISO).",
	number: "Por favor insira um número válido.",
	digits: "Por favor insira apenas digitos.",
	creditcard: "Por favor insira um número válido de cartão de crédito.",
	equalTo: "Por favor digite o mesmo valor novamente.",
	accept: "Please enter a value with a valid extension.",
	maxlength: jQuery.validator.format("Por favor não insira mais que {0} caracteres."),
	minlength: jQuery.validator.format("Por favor insira no mímino {0} caracteres."),
	rangelength: jQuery.validator.format("Por favor insira um texto entre {0} e {1} caracteres."),
	range: jQuery.validator.format("Por favor insira um valor entre {0} e {1}."),
	max: jQuery.validator.format("Por favor insira um valor menor ou igual que {0}."),
	min: jQuery.validator.format("Por favor insira um valor maior ou igual que {0}.")
});