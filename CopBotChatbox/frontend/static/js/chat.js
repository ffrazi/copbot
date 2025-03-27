document.addEventListener("DOMContentLoaded", function () {
    const chatForm = document.getElementById("chat-form");
    const chatInput = document.getElementById("chat-input");
    const chatMessages = document.getElementById("chat-messages");

    chatForm.addEventListener("submit", function (event) {
        event.preventDefault();
        const userMessage = chatInput.value.trim();

        if (userMessage === "") return;

        addMessage("You", userMessage, "user-message");
        chatInput.value = "";

        fetch("/chatbot", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ message: userMessage }),
        })
        .then(response => response.json())
        .then(data => {
            addMessage("CopBot", data.response, "bot-message");
        })
        .catch(error => {
            console.error("Error:", error);
            addMessage("CopBot", "Sorry, something went wrong.", "bot-message");
        });
    });

    function addMessage(sender, message, className) {
        const messageElement = document.createElement("div");
        messageElement.classList.add("message", className);
        messageElement.innerHTML = `<strong>${sender}:</strong> ${message}`;
        chatMessages.appendChild(messageElement);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
});