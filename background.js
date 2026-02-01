// Flyff Translate - Background Script

const DEFAULT_API_KEY = '4029f8a1-ac73-440e-ab3b-64c2ce0464d6:fx';

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'translate') {
    translateText(request.text, request.sourceLang, request.targetLang)
      .then(result => sendResponse(result))
      .catch(error => sendResponse({ error: error.message }));
    return true;
  }
});

async function translateText(text, sourceLang, targetLang) {
  const storage = await chrome.storage.sync.get(['deeplApiKey']);
  const apiKey = storage.deeplApiKey || DEFAULT_API_KEY;

  try {
    const response = await fetch('https://api-free.deepl.com/v2/translate', {
      method: 'POST',
      headers: {
        'Authorization': `DeepL-Auth-Key ${apiKey}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        text: [text],
        source_lang: sourceLang,
        target_lang: targetLang
      })
    });

    if (!response.ok) {
      return { error: `Erreur API: ${response.status}` };
    }

    const data = await response.json();

    if (data.translations && data.translations.length > 0) {
      return { translatedText: data.translations[0].text };
    }

    return { error: 'Aucune traduction' };
  } catch (error) {
    return { error: 'Erreur de connexion' };
  }
}
