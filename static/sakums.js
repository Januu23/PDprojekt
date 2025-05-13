function startSpeli() {
  let ievaditsVards = document.querySelector('#vards').value.trim(); // .trim() entfernt führende und nachfolgende Leerzeichen
  if (ievaditsVards === '') {
    alert('Lūdzu ievadiet vārdu!');
  } else {
    // Verwende encodeURIComponent, um sicherzustellen, dass der Name korrekt in der URL codiert wird
    window.location.href = 'game#' + encodeURIComponent(ievaditsVards);
  }
}
// überleitung:{
document.getElementById("Pieteikties spēlē").add EventListener="game.html";
}
