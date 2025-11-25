// Event listener DEBE estar fuera de la función sendMessage
document.getElementById("userMessage").addEventListener("keypress", function (e) {
  if (e.key === "Enter") {
    sendMessage();
  }
});

async function sendMessage() {
  const userMessage = document.getElementById("userMessage").value.trim();
  
  // Validar que el mensaje no esté vacío
  if (!userMessage) {
    return;
  }

  const responseBox = document.getElementById("response");

  // Mostrar mensaje del usuario inmediatamente
  const userMessageDiv = document.createElement("div")
  userMessageDiv.className = "user-message block py-[0.125rem] px-[0.25rem] rounded-tl-md rounded-bl-md rounded-br-md relative ml-auto mr-[10px] mb-[.5rem] mb-2 w-auto max-w-[70%] min-w-[5rem] bg-amber-600 before:absolute before:top-0 before:right-[-9px] before:content-[''] before:w-[10px] before:h-[10px] before:bg-amber-600";
  userMessageDiv.innerHTML = `<strong class="text-xs">Tú:</strong><br />  ${userMessage}`;
  responseBox.appendChild(userMessageDiv);

  // Hacer scroll después de añadir el mensaje del usuario
  setTimeout(() => {
    responseBox.scrollTop = responseBox.scrollHeight;
  }, 0);

  // Mostrar escribiendo, mientras esperamos la respuesta
  const typingDiv = document.createElement("div")
  typingDiv.className = "bot-typing";
  typingDiv.id = "typing";
  typingDiv.innerHTML = `<em>Bot está escribiendo...</em>`;
  responseBox.appendChild(typingDiv);

  // Hacer scroll después de añadir "escribiendo"
  setTimeout(() => {
    responseBox.scrollTop = responseBox.scrollHeight;
  }, 0);

  // Limpiar el input inmediatmente despues de enviar el mensaje
  document.getElementById("userMessage").value = "";

  try {
    const res = await fetch("http://127.0.0.1:8000/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ message: userMessage })
    });

    // Verificar si la respuesta fue exitosa
    if (!res.ok) {
      throw new Error(`Error HTTP: ${res.status}`);
    }

    const data = await res.json();
    
    // Remover el "escribiendo" y mostrar la respuesta real
    const typingElement = document.getElementById("typing");
    if (typingElement) {
      responseBox.removeChild(typingElement);
    }

    // Agregar mensaje del bot
    const botMessageDiv = document.createElement("div");
    botMessageDiv.className = "bot-message block py-[0.125rem] px-[0.25rem] rounded-tr-md rounded-bl-md rounded-br-md relative mr-auto ml-[10px] mb-[.5rem] mb-2 w-auto max-w-[70%] min-w-[5rem] bg-white before:absolute before:top-0 before:left-[-9px] before:content-[''] before:w-[10px] before:h-[10px] before:bg-white";
    botMessageDiv.innerHTML = `<strong class="text-xs">Bot:</strong><br /> ${data.response}`;
    responseBox.appendChild(botMessageDiv);

    // Hacer scroll DESPUÉS de añadir el mensaje del bot
    setTimeout(() => {
      responseBox.scrollTop = responseBox.scrollHeight;
    }, 0);

  } catch (err) {
    // remover el "escribiendo" en caso de error
    const typingElement = document.getElementById("typing");
    if (typingElement) {
      responseBox.removeChild(typingElement);
    }

    // Mostrar mensaje de error
    const errorDiv = document.createElement("div");
    errorDiv.innerHTML = "<strong>Error al enviar el mensaje.</strong>";
    errorDiv.style.color = "red";
    responseBox.appendChild(errorDiv);

    // Hacer scroll después del mensaje de error
    setTimeout(() => {
      responseBox.scrollTop = responseBox.scrollHeight;
    }, 0);

    console.error("Error al enviar el mensaje:", err);    
  }
}