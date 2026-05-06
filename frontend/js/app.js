// 1. Değişken Tanımlamaları
const chatMessages = document.getElementById('chat-messages');
const chatOptions = document.getElementById('chat-options');

// 2. Kişi 3'ün Hazırladığı JSON Verilerini Çekme (Ürün Bilgileri)
async function getProducts() {
    try {
        // Dosya yolunu klasör yapınıza göre kontrol edin (Örn: '../backend/data/products.json')
        const response = await fetch('backend/data/products.json');
        const products = await response.json();
        return products;
    } catch (error) {
        console.error("Ürün verileri yüklenemedi:", error);
        return [];
    }
}

// 3. Ana Kontrol Fonksiyonu: Butonlara Tıklandığında Çalışır
async function handleOption(optionText) {
    // Kullanıcının seçtiği butonu ekrana mesaj olarak bas
    appendMessage(optionText, 'user');

    // Butonları geçici olarak kilitle (üst üste tıklamayı önlemek için)
    chatOptions.style.pointerEvents = "none";
    chatOptions.style.opacity = "0.5";

    if (optionText === 'Ürün Öner') {
        // Ürün Öner senaryosu: Verileri JSON'dan al ve kart olarak bas
        const products = await getProducts();
        renderProductList(products);

        // İşlem bitince butonları tekrar aç
        chatOptions.style.pointerEvents = "auto";
        chatOptions.style.opacity = "1";
    } else {
        // Diğer senaryolar (Sipariş Takibi vb.): Kişi 1'in Backend'ine (AI) sor
        try {
            const response = await fetch('http://localhost:8000/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: optionText })
            });
            const data = await response.json();
            appendMessage(data.response, 'bot');
        } catch (error) {
            appendMessage("Şu an sisteme bağlanılamıyor.", 'bot');
        } finally {
            // Butonları tekrar aktif et
            chatOptions.style.pointerEvents = "auto";
            chatOptions.style.opacity = "1";
        }
    }
}

// 4. Mesaj Balonlarını Ekrana Basan Fonksiyon (Ekran görüntündeki fonksiyonun günceli)
function appendMessage(text, sender) {
    const msgDiv = document.createElement('div');
    msgDiv.className = `message ${sender}`;
    msgDiv.innerText = text;
    chatMessages.appendChild(msgDiv);

    // Otomatik aşağı kaydırma
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// 5. Ürünleri Şık Kartlar Halinde Gösteren Fonksiyon
function renderProductList(products) {
    // Botun giriş cümlesi
    appendMessage("İşte sizin için seçtiğimiz bazı ürünler:", 'bot');

    // Kartların içinde duracağı grid yapısı
    const productGrid = document.createElement('div');
    productGrid.className = 'product-grid';

    products.forEach(product => {
        const card = document.createElement('div');
        card.className = 'product-card';
        card.innerHTML = `
            <h4>${product.name}</h4>
            <p><strong>${product.price} TL</strong></p>
            <button onclick="handleOption('${product.name} hakkında detay ver')">İncele</button>
        `;
        productGrid.appendChild(card);
    });

    chatMessages.appendChild(productGrid);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}