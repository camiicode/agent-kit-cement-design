async function sendMessage() {
  const userMessage = document.getElementById("userMessage").value;

  const responseBox = document.getElementById("response");
  responseBox.innerHTML = "Enviando...";

  try {
    const res = await fetch("http://127.0.0.1:8000/chat", {
      method: "POST",
      headers: {
        "content-type": "application/json"
      },
      body: JSON.stringify({ message: userMessage })
    });

    const data = await res.json();
    responseBox.innerHTML = "Respuesta del Backend: " + data.response;
    
  } catch (err) {
    responseBox.innerHTML = "Error al enviar el mensaje.";
    console.error(err);
  }
}