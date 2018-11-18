document.addEventListener("DOMContentLoaded",function(){
  let communitiesContainer = document.getElementById("communitiesContainer");
  let select = communitiesContainer.getElementsByTagName("select")[0];
  let input = communitiesContainer.getElementsByClassName('select-dropdown')[0];

  communitiesFilter(select, input, communitiesContainer);

  select.addEventListener("change", function(e){
    communitiesFilter(e.target, input, communitiesContainer);
  });
});

function communitiesFilter(select, input, communitiesContainer){
  if(select.selectedIndex == -1){
    input.classList.add("not-selected-community");
    select.insertAdjacentHTML("afterend", "<p>Seleccione las comunidades</p>");
  }
  else{
    input.classList.remove("not-selected-community");
    let message = communitiesContainer.getElementsByTagName("p")[0];
    if(message){
        message.parentNode.removeChild(message);
    }
  }
}
