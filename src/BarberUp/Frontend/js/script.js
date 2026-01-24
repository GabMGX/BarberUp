document.addEventListener("DOMContentLoaded", () => {
  const calendario = document.getElementById("calendario");
  const inputData = document.getElementById("data");
  const selectProfissional = document.getElementById("profissional");
  const form = document.getElementById("formAgendamento");
  const btnAbrirCalendario = document.getElementById("btnAbrirCalendario");
  const horariosDiv = document.getElementById("horariosDisponiveis");


  btnAbrirCalendario.addEventListener("click", () => {
    calendario.style.display = "grid"; 
  });

  function gerarCalendario() {
    if (!calendario) return;
    calendario.innerHTML = "";
    const hoje = new Date();
    const ano = hoje.getFullYear();
    const mes = hoje.getMonth();
    const primeiroDia = new Date(ano, mes, 1).getDay();
    const ultimoDia = new Date(ano, mes + 1, 0).getDate();

    for (let i = 0; i < primeiroDia; i++) calendario.appendChild(document.createElement("div"));

    for (let dia = 1; dia <= ultimoDia; dia++) {
      const dataAtual = new Date(ano, mes, dia);
      const div = document.createElement("div");
      div.className = "dia";
      div.textContent = dia;

      const hojeSemHora = new Date();
      hojeSemHora.setHours(0,0,0,0);

      if (dataAtual < hojeSemHora) div.classList.add("inativo");
      else div.addEventListener("click", () => {
        document.querySelectorAll(".dia").forEach(d => d.classList.remove("selecionado"));
        div.classList.add("selecionado");

        const mesFmt = String(mes + 1).padStart(2, "0");
        const diaFmt = String(dia).padStart(2, "0");
        inputData.value = `${ano}-${mesFmt}-${diaFmt}`;

        atualizarHorarios();
      });

      calendario.appendChild(div);
    }
  }

  function gerarHorarios() {
    const horarios = [];
    let minutos = 8*60; 
    const fim = 18*60;  
    while(minutos < fim) {
      const h = String(Math.floor(minutos/60)).padStart(2,"0");
      const m = String(minutos%60).padStart(2,"0");
      horarios.push(`${h}:${m}`);
      minutos += 15;
    }
    return horarios;
  }

  function horarioPassado(data,hora) {
    const agora = new Date();
    const dataHora = new Date(`${data}T${hora}`);
    return dataHora < agora;
  }


  function atualizarHorarios() {
    horariosDiv.innerHTML = ""; 
    const data = inputData.value;
    const profissional = selectProfissional.value;
    if(!data || !profissional) return;
    const horarios = gerarHorarios();
    let encontrou = false;

    function render(agendamentos) {
      horarios.forEach(hora => {
        const ocupado = agendamentos.some(a => (a.date === data || a.data === data) && (a.time === hora || a.hora === hora) && (a.barber === profissional || a.professional === profissional || a.profissional === profissional));
        if(!ocupado && !horarioPassado(data,hora)) {
          const btn = document.createElement("button");
          btn.type = "button";
          btn.textContent = hora;
          btn.className = "btnHorario";
          btn.addEventListener("click", () => {
            document.querySelectorAll(".btnHorario").forEach(b => b.classList.remove("selecionado"));
            btn.classList.add("selecionado");
            inputData.dataset.horaSelecionada = hora; 
          });
          horariosDiv.appendChild(btn);
          encontrou = true;
        }
      });

      if(!encontrou){
        const span = document.createElement("span");
        span.textContent = "Nenhum horário disponível";
        horariosDiv.appendChild(span);
      }
    }

    // If running inside pywebview, call the Python API; otherwise fallback to localStorage
    if (window.pywebview && window.pywebview.api && typeof window.pywebview.api.getAppointments === "function") {
      window.pywebview.api.getAppointments(profissional, data).then((serverAgendamentos) => {
        // serverAgendamentos expected: [{id, client, date, time}, ...]
        const agendamentos = (serverAgendamentos || []).map(a => ({data: a.date, hora: a.time, profissional: profissional}));
        render(agendamentos);
      }).catch(() => {
        const agendamentos = JSON.parse(localStorage.getItem("agendamentos")) || [];
        render(agendamentos);
      });
    } else {
      const agendamentos = JSON.parse(localStorage.getItem("agendamentos")) || [];
      render(agendamentos);
    }
  }

  if(selectProfissional) selectProfissional.addEventListener("change", atualizarHorarios);

  if(form) form.addEventListener("submit", e=>{
    e.preventDefault();
    const profissional = selectProfissional.value;
    const data = inputData.value;
    const hora = inputData.dataset.horaSelecionada;

    if(!data || !hora){
      alert("Selecione dia e horário!");
      return;
    }

    const agendamentos = JSON.parse(localStorage.getItem("agendamentos")) || [];
    const conflito = agendamentos.some(a => a.data===data && a.hora===hora && a.profissional===profissional);

    if(conflito){
      alert("Horário já ocupado!");
      return;
    }

    agendamentos.push({nome,profissional,data,hora});
    localStorage.setItem("agendamentos", JSON.stringify(agendamentos));
    alert("Agendamento realizado!");

    form.reset();
    horariosDiv.innerHTML = "";
    document.querySelectorAll(".dia").forEach(d => d.classList.remove("selecionado"));
    calendario.style.display = "none";
    delete inputData.dataset.horaSelecionada;
  });

  gerarCalendario();
});
