window.onload = function() {
  const tabula = document.getElementById("rezultati");

  fetch("/topData")
      .then(response => response.json())
      .then(data => {
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
