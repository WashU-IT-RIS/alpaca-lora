// JavaScript function to get cookie by name; retrieved from https://docs.djangoproject.com/en/3.1/ref/csrf/
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
// Function to get reply
function getReply(message) {
    $.ajax({

        type: "POST",  // or "GET" if applicable
        headers: {
            "X-CSRFToken": getCookie("csrftoken")
        },
        url: "/getResponse/",  // Replace with the actual URL of your Django view
        data: {
          message: message,
        },
        success: function(response) {
          // Handle the response from the Django view
          addBotMessage(response);
        },
        error: function(xhr, errmsg, err) {
          // Handle any errors that occur during the AJAX request
          console.log(xhr.status + ": " + xhr.responseText);
        }
      });
    
}

// Function to add a user message to the chat log
function addUserMessage(message) {
    const chatLog = document.getElementById('chatLog');
    const userMessage = document.createElement('div');
    userMessage.classList.add('chat-message', 'user');
    userMessage.innerHTML = `<p>${message}</p>`;
    chatLog.appendChild(userMessage);
    chatLog.appendChild(document.createElement('br'))
    chatLog.scrollTop = chatLog.scrollHeight;
}

// Function to add a bot message to the chat log
function addBotMessage(message) {
    const chatLog = document.getElementById('chatLog');
    const botMessage = document.createElement('div');
    botMessage.classList.add('chat-message', 'bot');
    botMessage.innerHTML = `<p>${message}</p>`;
    chatLog.appendChild(botMessage);
    chatLog.appendChild(document.createElement('br'))
    chatLog.scrollTop = chatLog.scrollHeight;
}

// Function to handle user input
function handleUserInput() {
    const userInput = document.getElementById('userInput');
    const message = userInput.value.trim();

    if (message !== '') {
        addUserMessage(message);
        userInput.value = '';

        const reply = getReply(message);
        

        userInput.focus();
    }
}

// Event listener for send button click
document.getElementById('sendBtn').addEventListener('click', handleUserInput);

// Event listener for enter key press
document.addEventListener('keypress', (event) => {
    if (event.keyCode === 13 || event.which === 13) {
        handleUserInput();
    }
});
