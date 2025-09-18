chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  if (changeInfo.status === 'complete' && tab.url) {
    const url = new URL(tab.url);

    // List of sites to ignore
    const blockedSites = [
      "github.com",
      "linkedin.com",
      "www.linkedin.com",
      "web.whatsapp.com",
      "mail.google.com",
      "drive.google.com",
      "telegram.org",
	"chatgpt.com" ,
	    "search.brave.com",
	    "login.live.com",
	    "onedrive.live.com",
	    "newtab"
    ];

    if (blockedSites.includes(url.hostname)) {
      console.log("Activity tracking disabled for:", url.hostname);
      return; // Skip sending activity
    }

    const activity = {
      site: url.hostname,
      url: tab.url,
      title: tab.title || "Unknown Title",
      type: "PAGE_VISIT"
    };

    console.log("Detected activity:", activity);

    // Send to backend
    fetch("http://127.0.0.1:5000/api/update", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(activity)
    })
    .then(res => res.json())
    .then(data => console.log("Success:", data))
    .catch(err => console.error("Error sending activity:", err));
  }
});
