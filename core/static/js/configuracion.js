document.addEventListener("DOMContentLoaded", () => {
  const btnReiniciar = document.querySelector(".btn-reiniciar");
  if (!btnReiniciar) return;

  btnReiniciar.addEventListener("click", () => {
    const confirmado = confirm("¿Seguro que quieres reiniciar las ventas del mes? Esta acción no se puede deshacer.");
    if (!confirmado) return;

    fetch("/api/resetear_ventas_mes/", {
      method: "POST",
      headers: { "Content-Type": "application/json" }
    })
      .then(res => res.json())
      .then(data => {
        if (data.error) {
          alert("No se pudo reiniciar: " + data.error);
          return;
        }
        alert("Ventas del mes reiniciadas");
      })
      .catch(() => alert("No se pudo conectar con el servidor."));
  });
});
