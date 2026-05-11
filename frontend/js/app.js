const chatMessages = document.getElementById("chat-messages");
/*HTML'DE ID'Yİ ARA VE DEĞİŞKENE ATA, MESAJ NEREYE EKLENECEK*/
const chatInput = document.getElementById("chat-input");
/*KULLANICININ YAZDIĞINI OKUR*/

// Hızlı cevap butonları
async function sendQuickMessage(text) {
    appendMessage(text, "user");
    fetchResponse(text.toLowerCase());
    /*KULLANICININ MESAJINI YAKALAR*/
}

// Inputtan mesaj gönderme
async function sendMessage() {
    /*KULLANICININ MESAJINI YAKALAR*/
    const text = chatInput.value.trim();

    if (!text) return;

    appendMessage(text, "user");
    /*KULLANICININ YAZDIĞINI EKRANA BASAR*/

    chatInput.value = "";

    fetchResponse(text.toLowerCase());
    /*ARKAPLANA İŞ GÖNDERİR VE CEVABI GETİRİR*/
}

// Backend API çağrısı
async function fetchResponse(message) {

    try {

        const response = await fetch("/api/chat", {
            /*SUNUCUYA İSTEK GÖNDERİR*/
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                user_id: "user_123",
                message: message
            })
            /*VERİLER GÜVENLİ ŞEKİLDE SUNUCUYA PAKETLENİR*/
        });

        const data = await response.json();

        console.log(data);

        // Ürün listesi varsa render et
        if (data.products) {

            renderProductList(data.products);

        } else {

            // Normal bot mesajı
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

// Mesaj ekleme
function appendMessage(text, sender) {

    const msg = document.createElement("div");

    msg.className = `message ${sender}`;

    msg.innerText = text;

    chatMessages.appendChild(msg);

    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Ürün listeleme
function renderProductList(products) {
    /*SUNUCUDAN GELEN ÜRÜN LİSTESİNİ ALIR*/

    appendMessage(
        "İşte senin için seçtiğim ürünler:",
        "bot"
    );

    const listContainer = document.createElement("div");
    listContainer.className = "product-list-container";

    products.forEach((p) => {
        /*HER ÜRÜN İÇİN HTML KARTI OLUŞTURUR*/

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

        // 🔥 KRİTİK FIX: onclick HTML içine gömmüyoruz
        const btn = productCard.querySelector("button");

        btn.addEventListener("click", () => {
            sendQuickMessage(`Ürün Detayı: ${p.name}`);
        });

        listContainer.appendChild(productCard);
    });

    chatMessages.appendChild(listContainer);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}


// ENTER ile gönderme
chatInput.addEventListener("keypress", function (e) {

    if (e.key === "Enter") {
        sendMessage();
    }
});