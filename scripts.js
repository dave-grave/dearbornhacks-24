function sendMessage() {
  var messageInput = document.getElementById("message-input");
  var messageText = messageInput.value.trim();

  if (messageText !== "") {
    var chatBox = document.getElementById("chat-box");

    var userMessageElement = document.createElement("div");
    userMessageElement.className = "message user-message";
    userMessageElement.textContent = messageText;
    chatBox.appendChild(userMessageElement);

    fetch("http://127.0.0.1:5000/send_message", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ message: messageText }),
    })
      .then((response) => response.json())
      .then((data) => {
        var responseMessageElement = document.createElement("div");
        responseMessageElement.className = "message response-message";
        responseMessageElement.textContent = data.response;
        chatBox.appendChild(responseMessageElement);
        chatBox.scrollTop = chatBox.scrollHeight;
      })
      .catch((error) => {
        console.error("Error:", error);
      });

    messageInput.value = "";
    adjustTextareaHeight(messageInput); // Reset height after sending message
  }
}

// Adjust the height of the textarea dynamically as user types
function adjustTextareaHeight(textarea) {
  textarea.style.height = "auto"; // Reset height to auto to calculate new scroll height
  textarea.style.height = textarea.scrollHeight + "px";
}

// Event listener for textarea input to adjust height dynamically
document.getElementById("message-input").addEventListener("input", function () {
  adjustTextareaHeight(this);
});

// Optionally, send message on Enter key press without shift
document
  .getElementById("message-input")
  .addEventListener("keypress", function (e) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault(); // Prevents creating a new line
      sendMessage();
    }
  });
