
var inputs = document.querySelectorAll('.input-file');
var importButton = document.getElementById('import');

Array.prototype.forEach.call(inputs, function(input)
{
    var label = input.nextElementSibling;
    var labelVal = label.innerHTML;
    var span = label.nextElementSibling;
    var spanVal = span.innerHTML;

	input.addEventListener('change', function(e)
	{
		var fileName = '';
		if(this.files && this.files.length > 1) {
            fileName = ( this.getAttribute( 'data-multiple-caption' ) || '' ).replace( '{count}', this.files.length );
		}
		else {
          fileName = e.target.value.split( '\\' ).pop();
        }

		if(fileName) {
			span.innerHTML = fileName;
			importButton.disabled = false;
        }

	});
});

