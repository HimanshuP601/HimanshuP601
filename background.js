const allowedSites = [
  "medium.com",
  "stackoverflow.com",
  "dev.to",
  "ctftime.org"
];

chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  if (changeInfo.status === 'complete' && tab.url) {
    const url = new URL(tab.url);

    // Only track allowed sites
    if (!allowedSites.includes(url.hostname)) return;

    const activity = {
      site: url.hostname,
      url: tab.url,
      title: tab.title || "Unknown Title",
      type: "PAGE_VISIT"
    };

    // Send to local backend
    fetch("http://127.0.0.1:5000/api/update", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(activity)
    })
    .then(res => res.json())
    .then(data => console.log("Activity recorded:", data))
    .catch(err => console.error(err));
  }
});
