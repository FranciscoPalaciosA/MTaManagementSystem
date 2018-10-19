function showContactFields(id){
  //console.log('value = ' + document.getElementById(id).value);

  document.getElementById('fields_for_volunteers').hidden = true;

  var select = document.getElementById(id);
  var program = select.options[select.selectedIndex].text;



  switch (program) {

    case "Voluntario":
      document.getElementById('fields_for_volunteers').hidden = false;
      break;

  }
}
