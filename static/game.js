let meginajumi = 0;
let startLaiks;


window.onload = function() {
    const vards = sessionStorage.getItem("playerName");
    const limenis = sessionStorage.getItem("playerLevel");

   
    document.getElementById("speleris").textContent = vards;
    document.getElementById("limenis").textContent = limenis;

   
    fetch("/start_game", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            level: parseInt(limenis),
            vards: vards
        })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("message").textContent = data.message;
        startLaiks = Date.now(); // Saglabā spēles sākuma laiku
    })
    .catch(err => {
        console.error("Kļūda startējot spēli:", err);
    });
};


function makeGuess() {
    const guess = parseInt(document.getElementById("guessInput").value);

   
    if (isNaN(guess)) {
        alert("Lūdzu, ievadiet derīgu skaitli!");
        return;
    }

    fetch("/guess", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ guess: guess })
    })
    .then(response => response.json())
    .then(data => {
        meginajumi++;
        document.getElementById("meginajumi").textContent = meginajumi;
        document.getElementById("message").textContent = data.message;

     
        if (data.result === "pareizi") {
            const beiguLaiks = Date.now();
            const laiksSekundes = Math.floor((beiguLaiks - startLaiks) / 1000);

           
            const rezultats = {
                vards: sessionStorage.getItem("playerName"),
                klikskki: meginajumi,
                laiks: laiksSekundes,
                limenis: sessionStorage.getItem("playerLevel")
            };

            // Nosūtām rezultātu uz serveri
            fetch("/pievienot-rezultatu", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(rezultats)
            })
            .then(() => {
                setTimeout(() => {
                    alert(`Apsveicu! Tu uzminēji ar ${meginajumi} mēģinājumiem ${laiksSekundes} sekundēs!`);
                    // Automātiski pāriet uz rezultātu lapu
                    window.location.href = "top.html";
                }, 300);
            })
            .catch(err => {
                console.error("Kļūda saglabājot rezultātu:", err);
            });
        }
    })
    .catch(err => {
        console.error("Kļūda minēšanas laikā:", err);
    });
}
