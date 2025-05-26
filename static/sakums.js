function startSpeli() {
  let ievaditsVards = document.querySelector('#vards').value.trim(); 
  if (ievaditsVards === '') {
    alert('Lūdzu ievadiet vārdu!');
  } else {

    window.location.href = 'game#' + encodeURIComponent(ievaditsVards);
  }
}
 ("click" function(){
document.getElementById("Pieteikties spēlē").add EventListener="game.html";
}
