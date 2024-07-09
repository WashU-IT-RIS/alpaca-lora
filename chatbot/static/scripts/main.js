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

// Function to get reply
function updateRating(id, rating) {
    $.ajax({

        type: "POST",  // or "GET" if applicable
        headers: {
            "X-CSRFToken": getCookie("csrftoken")
        },
        url: "/updateRating/",  // Replace with the actual URL of your Django view
        data: {
		interactionId : id,
		rating: rating
        },
        success: function(response) {
          // Handle the response from the Django view
          console.log(response);
	  successfulVote(id, rating);
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
    patt = /`(.*?)`/ig
    messageFormatted = message.replace(patt, "<span class='code-box'>$1</span>")
    userMessage.innerHTML = `<p>${messageFormatted}</p>`;
    chatLog.appendChild(userMessage);
    chatLog.appendChild(document.createElement('br'))
    chatLog.scrollTop = chatLog.scrollHeight;
}


function successfulVote(id, rating) {
	const goodButton = document.getElementById('voteGood' + id);
	const badButton = document.getElementById('voteBad' + id);
	goodButton.classList.remove('highlighted-votebutton');
	badButton.classList.remove('highlighted-votebutton');
	if (rating > 0) {
		goodButton.classList.add('highlighted-votebutton');
	} else if (rating < 0) {
		badButton.classList.add('highlighted-votebutton');
	}

}

// Function to add a bot message to the chat log
function addBotMessage(message) {
    const chatLog = document.getElementById('chatLog');
    const botMessage = document.createElement('div');
    
    botMessage.classList.add('chat-message', 'bot');
    patt = /`(.*?)`/ig;
    messageFormatted = message.message.replace(patt, "<span class='code-box'>$1</span>");

    const voteMenu = document.createElement('div');
    const voteGood = document.createElement('button');
    const voteBad = document.createElement('button');
	
    voteMenu.classList.add('vote-menu');
    voteGood.classList.add('vote-button');
    voteBad.classList.add('vote-button');
    voteGood.id = "voteGood" + message.interactionId;
    voteBad.id = "voteBad" + message.interactionId;

    voteGood.textContent = "↑";
    voteBad.textContent = "↓";
    voteMenu.appendChild(voteGood);
    voteMenu.appendChild(voteBad);
    
    voteGood.addEventListener("click", () => {updateRating(message.interactionId, 50);});
    voteBad.addEventListener("click", () => {updateRating(message.interactionId, -50);});
    botMessage.innerHTML = `<p>${messageFormatted}</p><p style='color:#ccc;font-size:10px;'>Interaction #${message.interactionId}</p>`;
    botMessage.appendChild(voteMenu);
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
