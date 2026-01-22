document.addEventListener("DOMContentLoaded", () => {
  const filtro = document.getElementById("filtroProfissional");
  const lista = document.getElementById("listaAgendamentos");

  function mostrarAgendamentos() {
   
    let agendamentos = [];
    try {
      agendamentos = JSON.parse(localStorage.getItem("agendamentos")) || [];
    } catch (e) {
      console.error("Erro ao ler localStorage:", e);
      agendamentos = [];
    }

    const profSelecionado = filtro.value;
    lista.innerHTML = "";

    
    const filtrados = profSelecionado
      ? agendamentos.filter(a => a.profissional === profSelecionado)
      : agendamentos;

    if (filtrados.length === 0) {
      lista.innerHTML = "<p>Nenhum agendamento encontrado.</p>";
      return;
    }

    
    filtrados.forEach(a => {
      const div = document.createElement("div");
      div.className = "agendamento";
      div.innerHTML = `
        <strong>Cliente:</strong> ${a.nome} <br>
        <strong>Profissional:</strong> ${a.profissional} <br>
        <strong>Data:</strong> ${a.data} <br>
        <strong>Hora:</strong> ${a.hora}
      `;
      lista.appendChild(div);
    });
  }

  
  filtro.addEventListener("change", mostrarAgendamentos);

  
  mostrarAgendamentos();
});
