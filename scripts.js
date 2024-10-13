function sendMessage() {
  var messageInput = document.getElementById("message-input");
  var messageText = messageInput.value.trim();

  if (messageText !== "") {
    var chatBox = document.getElementById("chat-box");

    var messageElement = document.createElement("div");
    messageElement.className = "message";
    messageElement.textContent = messageText;

    chatBox.appendChild(messageElement);
    chatBox.scrollTop = chatBox.scrollHeight;

    messageInput.value = "";
  }
}

// Optionally, send message on Enter key press
document
  .getElementById("message-input")
  .addEventListener("keypress", function (e) {
    if (e.key === "Enter") {
      sendMessage();
    }
  });
