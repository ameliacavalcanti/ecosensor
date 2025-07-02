// Simulação de dados — pode ser trocado por fetch API no futuro
document.addEventListener("DOMContentLoaded", () => {
  // Simula dados dos sensores
  const dados = {
    temperatura: "27.5",
    umidade: "62",
    luz: "830",
    ph: "6.3",
    especies: [
      "Ipê-Amarelo 🌼",
      "Pau-Brasil 🇧🇷",
      "Jequitibá-Rosa 🌳",
      "Embaúba 🌿",
      "Aroeira 🌾",
      "Jatobá 🍃"
    ]
  };

  // Atualiza dados no HTML
  document.getElementById("temperatura").textContent = `${dados.temperatura} °C`;
  document.getElementById("umidade").textContent = `${dados.umidade} %`;
  document.getElementById("luz").textContent = `${dados.luz} Lux`;
  document.getElementById("ph").textContent = dados.ph;

  
  const lista = document.getElementById("especies-lista");
  lista.innerHTML = "";
  dados.especies.forEach(especie => {
    const li = document.createElement("li");
    li.textContent = especie;
    lista.appendChild(li);
  });
});
