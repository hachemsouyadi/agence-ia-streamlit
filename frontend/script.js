async function askAgent() {
  const question = document.getElementById("question").value;

  const response = await fetch("http://127.0.0.1:8000/question", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ question: question })
  });

  const data = await response.json();
  document.getElementById("reponse").innerText = data.réponse || "❌ Erreur dans la réponse.";
}
