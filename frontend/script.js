let currentVideoId = null;

const urlInput = document.getElementById('youtube-url');
const processBtn = document.getElementById('process-btn');
const loadingBar = document.getElementById('loading-bar');
const resultSection = document.getElementById('result-section');
const chatSection = document.getElementById('chat-section');
const videoTitle = document.getElementById('video-title');
const debunkText = document.getElementById('debunk-text');

const chatInput = document.getElementById('chat-input');
const chatBtn = document.getElementById('chat-btn');
const chatHistory = document.getElementById('chat-history');

processBtn.addEventListener('click', async () => {
    const url = urlInput.value.trim();
    if (!url) return;

    // Reset UI
    resultSection.classList.add('hidden');
    chatSection.classList.add('hidden');
    loadingBar.classList.remove('hidden');
    chatHistory.innerHTML = '';

    try {
        const response = await fetch('/api/process-video', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ url: url })
        });

        const data = await response.json();
        
        if (!response.ok) {
            alert("Error: " + data.detail);
            return;
        }

        currentVideoId = data.video_id;
        videoTitle.innerText = data.title;
        debunkText.innerText = data.debunk;
        
        resultSection.classList.remove('hidden');
        chatSection.classList.remove('hidden');

    } catch (error) {
        alert("Failed to connect to server: " + error);
    } finally {
        loadingBar.classList.add('hidden');
    }
});

chatBtn.addEventListener('click', async () => {
    const question = chatInput.value.trim();
    if (!question || !currentVideoId) return;

    // Add user message
    const userMsg = document.createElement('div');
    userMsg.className = 'chat-msg user';
    userMsg.innerText = question;
    chatHistory.appendChild(userMsg);
    
    chatInput.value = '';

    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ video_id: currentVideoId, question: question })
        });

        const data = await response.json();

        if (!response.ok) {
            alert("Error: " + data.detail);
            return;
        }

        const botMsg = document.createElement('div');
        botMsg.className = 'chat-msg bot';
        botMsg.innerText = data.answer;
        chatHistory.appendChild(botMsg);
        
        chatHistory.scrollTop = chatHistory.scrollHeight;

    } catch (error) {
        alert("Failed to chat: " + error);
    }
});

chatInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        chatBtn.click();
    }
});
