// app/static/script.js
document.addEventListener("DOMContentLoaded", () => {
    const userInput = document.getElementById("user-input");
    const sendBtn = document.getElementById("send-btn");
    const chatBox = document.getElementById("chat-box");
    const loader = document.getElementById("loader");

    const addMessage = (text, sender) => {
        const messageElement = document.createElement("div");
        messageElement.classList.add("message", `${sender}-message`);
        const p = document.createElement("p");
        p.innerHTML = text; // Use innerHTML to render line breaks from model
        messageElement.appendChild(p);
        chatBox.appendChild(messageElement);
        chatBox.scrollTop = chatBox.scrollHeight;
    };

    const handleSend = async () => {
        const query = userInput.value.trim();
        if (query === "") return;

        addMessage(query, "user");
        userInput.value = "";
        loader.style.display = "block"; // Show loader

        try {
            const response = await fetch("/ask", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ query: query }),
            });

            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }

            const data = await response.json();
            // Replace newlines with <br> for HTML rendering
            const formattedResponse = data.response.replace(/\n/g, '<br>');
            addMessage(formattedResponse, "bot");

        } catch (error) {
            console.error("Error:", error);
            addMessage("Sorry, something went wrong. Please check the console for details.", "bot");
        } finally {
            loader.style.display = "none"; // Hide loader
        }
    };

    sendBtn.addEventListener("click", handleSend);
    userInput.addEventListener("keypress", (e) => {
        if (e.key === "Enter") {
            handleSend();
        }
    });
});