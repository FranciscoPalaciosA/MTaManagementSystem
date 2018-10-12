function showProgramFields(id){
  //console.log('value = ' + document.getElementById(id).value);

  document.getElementById('fields_for_productor').hidden = true;
  document.getElementById('fields_for_cisterna').hidden = true;
  document.getElementById('fields_for_saving_account').hidden = true;
  document.getElementById('fields_for_breakfast').hidden = true;
  document.getElementById('field_school').hidden = true;

  var select = document.getElementById(id);
  var program = select.options[select.selectedIndex].text;
  switch (program) {
    case "Productores":
      document.getElementById('fields_for_productor').hidden = false;
      break;
    case "Cisternas":
      document.getElementById('fields_for_cisterna').hidden = false;
      break;
    case "Cajas de ahorro":
      document.getElementById('fields_for_saving_account').hidden = false;
      break;
    case "Desayunos con amaranto":
      document.getElementById('fields_for_breakfast').hidden = false;
      document.getElementById('field_school').hidden = false;
      break;
    case "Ecónomas":
      document.getElementById('field_school').hidden = false;
      break;
    default:
  }
  document.getElementById('full_form').hidden = false;
}
