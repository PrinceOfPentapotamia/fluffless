document.getElementById('debunk-btn').addEventListener('click', async () => {
    // 1. Get the current active tab
    chrome.tabs.query({active: true, currentWindow: true}, async (tabs) => {
        let currentTab = tabs[0];
        let url = currentTab.url;

        // Check if it's a youtube video
        if (!url.includes("youtube.com/watch")) {
            document.getElementById('status-text').innerText = "ERROR: NOT A YOUTUBE VIDEO.";
            document.getElementById('status-text').style.color = "red";
            return;
        }

        // 2. Update UI
        document.getElementById('debunk-btn').classList.add('hidden');
        document.getElementById('loading').classList.remove('hidden');
        document.getElementById('status-text').innerText = "EXTRACTING SUMMARY...";

        try {
            // 3. Ping local API
            const response = await fetch('http://127.0.0.1:8000/api/process-video', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ url: url })
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.detail || "Server error");
            }

            // 4. Show Result
            document.getElementById('loading').classList.add('hidden');
            document.getElementById('status-text').innerText = "SUMMARIZED.";
            document.getElementById('result').classList.remove('hidden');
            
            document.getElementById('video-title').innerText = data.title;
            document.getElementById('debunk-text').innerText = data.debunk;

        } catch (error) {
            document.getElementById('loading').classList.add('hidden');
            document.getElementById('debunk-btn').classList.remove('hidden');
            document.getElementById('status-text').innerText = "ERROR: " + error.message;
            document.getElementById('status-text').style.color = "red";
        }
    });
});
