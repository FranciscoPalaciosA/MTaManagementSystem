function toFillFullForm(){
  var inputs = document.getElementById('full_form').getElementsByTagName('input');
  for(var i = 0; i < inputs.length; i++){
    inputs[i].className += " to_fill";
  }
}

function clearToFill(){
  var totalInputs = document.getElementsByClassName("change_req");
  console.log(totalInputs);
  for(var i = 0; i < totalInputs.length; i++){
    //console.log(totalInputs[i].className);
    var newClassName = totalInputs[i].className.replace("to_fill", "");
    totalInputs[i].className = newClassName;
    //console.log(totalInputs[i].className);
  }
}

function showProgramFields(id){
  //console.log('value = ' + document.getElementById(id).value);
  document.getElementById('fields_for_productor').hidden = true;
  document.getElementById('fields_for_cisterna').hidden = true;
  document.getElementById('fields_for_saving_account').hidden = true;
  document.getElementById('fields_for_breakfast').hidden = true;
  document.getElementById('field_school').hidden = true;

  clearToFill();

  var select = document.getElementById(id);
  var program = select.options[select.selectedIndex].text;
  var inputs = [];
  var oInputs = null;

  switch (program) {
    case "Productores":
      document.getElementById('fields_for_productor').hidden = false;
      inputs = document.getElementById('fields_for_productor').getElementsByTagName('input');
      //totalInputs += document.getElementById('fields_for_productor').getElementsByTagName('input').length;
      break;
    case "Cisternas":
      document.getElementById('fields_for_cisterna').hidden = false;
      inputs = document.getElementById('fields_for_cisterna').getElementsByTagName('input');
      break;
    case "Cajas de ahorro":
      document.getElementById('fields_for_saving_account').hidden = false;
      inputs = document.getElementById('fields_for_saving_account').getElementsByTagName('input');
      break;
    case "Desayunos con amaranto":
      document.getElementById('fields_for_breakfast').hidden = false;
      document.getElementById('field_school').hidden = false;
      inputs = document.getElementById('fields_for_breakfast').getElementsByTagName('input');
      oInputs = document.getElementById('field_school').getElementsByTagName('input');
      break;
    case "Ecónomas":
      document.getElementById('field_school').hidden = false;
      inputs = document.getElementById('field_school').getElementsByTagName('input');
      break;
    default:
  }
  document.getElementById('full_form').hidden = false;

  for(var i = 0; i < inputs.length; i++){
    inputs[i].className += " to_fill";
  }
  if(oInputs != null){
    for(var i = 0; i < oInputs.length; i++){
      oInputs[i].className += " to_fill";
    }
  }
  setOnBlur();
}

function setOnBlur(){
  var inputs = document.getElementsByClassName("to_fill");
  for(var i = 0; i < inputs.length; i++){
    inputs[i].addEventListener("blur", calculatePercentage);
  }
}

function calculatePercentage(){
  var totalInputs = document.getElementsByClassName("to_fill");
  var filledInputs = 0;
  //console.log("totalInputs", totalInputs);
  for(var i = 0; i < totalInputs.length; i++){
    if(totalInputs[i].value != ""){
      filledInputs++;
    }
  }
  var percentage = Math.ceil((filledInputs/totalInputs.length)*100) + "%";
  var percentageBar = document.getElementById("percentage_bar");
  percentageBar.style.width = percentage;
  percentageBar.innerHTML = percentage;
}

//inputs[i].addEventListener("blur", calculatePercentage, false);
