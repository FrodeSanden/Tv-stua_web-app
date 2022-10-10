function deleteProgram(programId) {
  fetch("/delete-program", {
    method: "POST",
    body: JSON.stringify({ programId: programId }),
  }).then((_res) => {
    window.location.href = "/";
  });
}

function voteProgram(programId, dato) {
  fetch("/vote-program", {
    method: "POST",
    body: JSON.stringify({ programId: programId }),
  }).then((_res) => {
    window.location.href = "/programList?date=" + dato;
  });
}