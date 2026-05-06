// 1. DOM Elementlerini Seçme
const chatMessages = document.getElementById('chat-messages');
const chatOptions = document.getElementById('chat-options');

// 2. Ürün Verilerini Backend'den Çekme
async function getProducts() {
    try {
        // FastAPI üzerinden sunduğumuz ürün listesine istek atar
        const response = await fetch('/api/products');
        if (!response.ok) throw new Error("Ürünler yüklenemedi");
        return await response.json();
    } catch (error) {
        console.error("Hata:", error);
        return [];
    }
}

// 3. Ana Kontrol Fonksiyonu: Buton Tıklamaları
async function handleOption(optionText) {
    // Kullanıcı mesajını ekrana ekle
    appendMessage(optionText, 'user');

    // Butonları işlem bitene kadar kilitle
    toggleButtons(false);

    if (optionText === 'Ürün Öner') {
        // --- ÜRÜN ÖNERİ SENARYOSU ---
        const products = await getProducts();
        if (products.length > 0) {
            renderProductList(products);
        } else {
            appendMessage("Şu an önerilecek ürün bulunamadı.", 'bot');
        }
        toggleButtons(true);

    } else if (optionText === 'Siparişim Nerede?') {
        // --- SİPARİŞ SORGULAMA SENARYOSU (order.py bağlantısı) ---
        const orderId = prompt("Lütfen 4 haneli sipariş numaranızı girin (Örn: 1001):");

        if (!orderId) {
            appendMessage("İşlem iptal edildi. Sipariş numarası girmediniz.", 'bot');
            toggleButtons(true);
            return;
        }

        try {
            const response = await fetch(`/api/order-status/${orderId}`);
            const data = await response.json();

            if (data.status === "Sipariş bulunamadı") {
                appendMessage(`❌ ${orderId} numaralı bir sipariş kaydı bulunamadı.`, 'bot');
            } else {
                appendMessage(`📦 Sipariş Durumu: ${data.status}`, 'bot');
            }
        } catch (error) {
            appendMessage("Sipariş sistemine şu an ulaşılamıyor.", 'bot');
        }
        toggleButtons(true);

    } else {
        // --- DİĞER DURUMLAR (AI Mesajlaşma) ---
        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: optionText })
            });
            const data = await response.json();
            appendMessage(data.reply, 'bot');
        } catch (error) {
            appendMessage("Üzgünüm, şu an bağlantı kuramıyorum.", 'bot');
        } finally {
            toggleButtons(true);
        }
    }
}

// 4. Mesaj Balonlarını Oluşturma
function appendMessage(text, sender) {
    const msgDiv = document.createElement('div');
    msgDiv.className = `message ${sender}`;
    msgDiv.innerText = text;
    chatMessages.appendChild(msgDiv);

    // Otomatik aşağı kaydır
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// 5. Ürün Kartlarını Ekrana Basma
function renderProductList(products) {
    appendMessage("İşte size özel seçtiğimiz ürünler:", 'bot');

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

// 6. Yardımcı Fonksiyon: Buton Kilidi
function toggleButtons(enable) {
    if (enable) {
        chatOptions.style.pointerEvents = "auto";
        chatOptions.style.opacity = "1";
    } else {
        chatOptions.style.pointerEvents = "none";
        chatOptions.style.opacity = "0.5";
    }
}