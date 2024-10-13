function setCourses() {
  var coursesInput = document.getElementById("courses-input").value.trim();

  fetch("http://127.0.0.1:5000/set_courses", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ courses: coursesInput }),
  })
    .then((response) => response.json())
    .then((data) => {
      console.log("Courses set:", data);
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}

function setYear() {
  var yearInput = document.getElementById("year-input").value.trim();

  fetch("http://127.0.0.1:5000/set_year", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ year: yearInput }),
  })
    .then((response) => response.json())
    .then((data) => {
      console.log("Year set:", data);
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}

function sendMessage() {
  var messageInput = document.getElementById("message-input");
  var messageText = messageInput.value.trim();
  //   var coursesInput = document.getElementById("courses-input")
  //     ? document.getElementById("courses-input").value.trim()
  //     : "";
  //   var yearInput = document.getElementById("year-input")
  //     ? document.getElementById("year-input").value.trim()
  //     : "";

  if (messageText !== "") {
    var chatBox = document.getElementById("chat-box");

    // display user's message
    var userMessageElement = document.createElement("div");
    userMessageElement.className = "message user-message";
    userMessageElement.textContent = messageText;
    chatBox.appendChild(userMessageElement);

    // Prepare the data to be sent to the backend
    var postData = {
      message: messageText,
      //   courses: coursesInput,
      //   year: yearInput,
    };

    fetch("http://127.0.0.1:5000/send_message", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ message: messageText /* postData */ }),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.error) {
          console.error("Error:", data.error);
          return;
        }

        // create a new element for AI response
        var responseMessageElement = document.createElement("div");
        responseMessageElement.className = "message response-message";

        // render AI message as Markdown
        responseMessageElement.textContent = data.response;
        chatBox.appendChild(responseMessageElement);
        chatBox.scrollTop = chatBox.scrollHeight;

        responseMessageElement.innerHTML = marked.parse(data.response);
        chatBox.appendChild(responseMessageElement);
        chatBox.scrollTop = chatBox.scrollHeight;
      })
      .catch((error) => {
        console.error("Error:", error);
      });
    // Reset height after sending message
    messageInput.value = "";
    adjustTextareaHeight(messageInput);
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
