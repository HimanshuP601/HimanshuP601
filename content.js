// Detect page visit and send to background
chrome.runtime.sendMessage({
    type: "PAGE_VISIT",
    site: window.location.hostname,
    url: window.location.href,
    title: document.title
});
