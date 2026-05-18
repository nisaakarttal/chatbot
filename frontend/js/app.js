const chatMessages = document.getElementById("chat-messages");
const chatInput = document.getElementById("chat-input");

async function sendQuickMessage(text) {
    appendMessage(text, "user");
    fetchResponse(text.toLowerCase());
}

async function sendMessage() {
    const text = chatInput.value.trim();

    if (!text) return;

    appendMessage(text, "user");

    chatInput.value = "";

    fetchResponse(text.toLowerCase());
}

async function fetchResponse(message) {

    try {

        const response = await fetch("/api/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                user_id: "user_123",
                message: message
            })
        });

        const data = await response.json();

        console.log(data);

        if (data.products) {

            renderProductList(data.products);

        } else {

            appendMessage(data.reply, "bot");
        }

    } catch (error) {

        console.error(error);

        appendMessage(
            "Sunucuyla bağlantı kurulamadı.",
            "bot"
        );
    }
}

function appendMessage(text, sender) {

    const msg = document.createElement("div");

    msg.className = `message ${sender}`;

    msg.innerText = text;

    chatMessages.appendChild(msg);

    chatMessages.scrollTop = chatMessages.scrollHeight;
}


function renderProductList(products) {

    appendMessage(
        "İşte senin için seçtiğim ürünler:",
        "bot"
    );

    const listContainer = document.createElement("div");
    listContainer.className = "product-list-container";

    products.forEach((p) => {

        const productCard = document.createElement("div");
        productCard.className = "product-card";

        productCard.innerHTML = `
            <img
                src="${p.image_url}"
                class="product-image"
                alt="${p.name}"
                onerror="this.src='https://via.placeholder.com/350x160?text=Resim+Yok'"
            >

            <div class="product-info">

                <h5>${p.name}</h5>

                <span class="price">${p.price} TL</span>

                <button class="opt-btn">
                    İncele
                </button>

            </div>
        `;

        const btn = productCard.querySelector("button");

        btn.addEventListener("click", () => {
            sendQuickMessage(`Ürün Detayı: ${p.name}`);
        });

        listContainer.appendChild(productCard);
    });

    chatMessages.appendChild(listContainer);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}


chatInput.addEventListener("keypress", function (e) {

    if (e.key === "Enter") {
        sendMessage();
    }
});