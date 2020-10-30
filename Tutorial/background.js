// background.js

// Called when the user clicks on the browser action.
chrome.browserAction.onClicked.addListener(function(tab) {
  // Send a message to the active tab
  chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
    var activeTab = tabs[0];
    chrome.tabs.sendMessage(activeTab.id, {"message": "clicked_browser_action"});
  });
});

// This block is new!
chrome.runtime.onMessage.addListener(
  function(request, sender, sendResponse) {``
    if( request.message === "open_new_tab" ) {
      chrome.tabs.create({"url": request.url});
    }
  }
);

let seltext = null;

chrome.extension.onRequest.addListener(function(request, sender, sendResponse)
{
    /*switch(request.message)
    {
        case 'setText':
            window.seltext = request.data
        break;
         
        default:
            sendResponse({data: 'Invalid arguments'});
        break;
    }*/
    window.seltext = request.data;
    alert("Highlighted Text: " + window.seltext);
});
 