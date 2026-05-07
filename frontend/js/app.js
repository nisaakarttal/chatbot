const chatMessages = document.getElementById("chat-messages");
const chatInput = document.getElementById("chat-input");

chatInput.addEventListener("keydown", function (e) {
    if (e.key === "Enter") {
        sendMessage();
    }
});


async function sendQuickMessage(text) {
    chatInput.value = text;
    await sendMessage();
}


async function sendMessage() {
    const text = chatInput.value.trim();

    if (!text) return;

    appendMessage(text, "user");
    chatInput.value = "";

    try {
        const response = await fetch("/api/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                user_id: "1",
                message: text
            })
        });

        const data = await response.json();

        if (data.products) {
            renderProductList(data.products);
        } else {
            appendMessage(data.response, "bot");
        }

    } catch {
        appendMessage("Bağlantı hatası oluştu.", "bot");
    }
}


function appendMessage(text, sender) {
    const msgDiv = document.createElement("div");
    msgDiv.className = `message ${sender}`;
    msgDiv.innerText = text;

    chatMessages.appendChild(msgDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}


function renderProductList(products) {
    appendMessage("İşte seçtiğim ürünler:", "bot");

    const grid = document.createElement("div");
    grid.className = "product-grid";

    products.forEach((p) => {
        grid.innerHTML += `
            <div class="product-card">
                <h4>${p.name}</h4>
                <p>${p.price} TL</p>
                <button onclick="sendQuickMessage('${p.name}')">
                    İncele
                </button>
            </div>
        `;
    });

    chatMessages.appendChild(grid);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}