// Šis skripts ielādē top rezultātus no servera un parāda tos tabulā

window.onload = function() {
  // Iegūstam tabulas ķermeni, kurā liksim rezultātus
  const tabula = document.getElementById("rezultati");

  // Izsauc fetch, lai dabūtu datus no Flask servera (no /topData)
  fetch("/topData")
      .then(response => response.json()) // Pārvēršam atbildi JSON objektā
      .then(data => {
          // Katrā datu ierakstā izveidojam jaunu rindu tabulā
          data.forEach((speleris) => {
              const rinda = document.createElement("tr");

              rinda.innerHTML = `
                  <td>${speleris.vards}</td>
                  <td>${speleris.meģinajumi}</td>
                  <td>${speleris.laiks}</td>
                  <td>${speleris.limenis}</td>
              `;

              tabula.appendChild(rinda);
          });
      })
      .catch(err => {
          console.error("Kļūda ielādējot rezultātus:", err);
          tabula.innerHTML = `
              <tr><td colspan="4">Kļūda ielādējot rezultātus!</td></tr>
          `;
      });
};
