function setCourses() {
  var coursesInput = document.getElementById("courses-input").value.trim();
  var coursesButton = document.querySelector("[onclick='setCourses()']");

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

      // clear input after user submits
      document.getElementById("courses-input").value = "";

      // Change the button text to "Done!" temporarily
      var originalText = coursesButton.textContent;
      coursesButton.textContent = "Done!";
      setTimeout(() => {
        coursesButton.textContent = originalText;
      }, 2000); // change back after 2 seconds
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}

function setYear() {
  var yearInput = document.getElementById("year-input").value.trim();
  var yearButton = document.querySelector("[onclick='setYear()']");

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

      // clear input field after setting the year
      document.getElementById("year-input").value = "";

      // Change the button text to "Done!" temporarily
      var originalText = yearButton.textContent;
      yearButton.textContent = "Done!";
      setTimeout(() => {
        yearButton.textContent = originalText;
      }, 2000); // change back after 2 seconds
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}

// function sendMessage() {
//   var messageInput = document.getElementById("message-input");
//   var messageText = messageInput.value.trim();
//   //   var coursesInput = document.getElementById("courses-input")
//   //     ? document.getElementById("courses-input").value.trim()
//   //     : "";
//   //   var yearInput = document.getElementById("year-input")
//   //     ? document.getElementById("year-input").value.trim()
//   //     : "";

//   if (messageText !== "") {
//     var chatBox = document.getElementById("chat-box");

//     // display user's message
//     var userMessageElement = document.createElement("div");
//     userMessageElement.className = "message user-message";
//     userMessageElement.textContent = messageText;
//     chatBox.appendChild(userMessageElement);

//     // Prepare the data to be sent to the backend
//     var postData = {
//       message: messageText,
//       //   courses: coursesInput,
//       //   year: yearInput,
//     };

//     fetch("http://127.0.0.1:5000/send_message", {
//       method: "POST",
//       headers: {
//         "Content-Type": "application/json",
//       },
//       body: JSON.stringify({ message: messageText /* postData */ }),
//     })
//       .then((response) => response.json())
//       .then((data) => {
//         if (data.error) {
//           console.error("Error:", data.error);
//           return;
//         }

//         // create a new element for AI response
//         var responseMessageElement = document.createElement("div");
//         responseMessageElement.className = "message response-message";

//         // render AI message as Markdown
//         responseMessageElement.textContent = data.response;
//         chatBox.appendChild(responseMessageElement);
//         chatBox.scrollTop = chatBox.scrollHeight;

//         responseMessageElement.innerHTML = marked.parse(data.response);
//         chatBox.appendChild(responseMessageElement);
//         chatBox.scrollTop = chatBox.scrollHeight;
//       })
//       .catch((error) => {
//         console.error("Error:", error);
//       });
//     // Reset height after sending message
//     messageInput.value = "";
//     adjustTextareaHeight(messageInput);
//   }
// }

function sendMessage() {
  var messageInput = document.getElementById("message-input");
  var messageText = messageInput.value.trim();

  if (messageText !== "") {
    var chatBox = document.getElementById("chat-box");

    // Display user's message
    var userMessageElement = document.createElement("div");
    userMessageElement.className = "message user-message";
    userMessageElement.textContent = messageText;
    chatBox.appendChild(userMessageElement);

    // Prepare the data to be sent to the backend
    var postData = {
      message: messageText,
    };

    fetch("http://127.0.0.1:5000/send_message", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(postData),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.error) {
          console.error("Error:", data.error);
          return;
        }

        // Create a new element for the AI response
        var responseMessageElement = document.createElement("div");
        responseMessageElement.className = "message response-message";

        // Render the AI response as Markdown
        responseMessageElement.innerHTML = marked.parse(data.response);
        chatBox.appendChild(responseMessageElement);

        // Check if there's Mermaid code to render
        if (data.mermaid) {
          var mermaidDiv = document.createElement("div");
          mermaidDiv.className = "mermaid";
          mermaidDiv.textContent = data.mermaid;
          chatBox.appendChild(mermaidDiv);

          // Reinitialize Mermaid to parse newly added Mermaid code
          mermaid.init(undefined, mermaidDiv);
        }

        chatBox.scrollTop = chatBox.scrollHeight;

        // Reset the message input field
        messageInput.value = "";
        adjustTextareaHeight(messageInput);
      })
      .catch((error) => {
        console.error("Error:", error);
      });

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
