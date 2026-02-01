// Flyff Translate - Content Script
// Appuyez sur Alt gauche pour traduire le texte sélectionné (FR → EN)

(function() {
  'use strict';

  let isTranslating = false;

  document.addEventListener('keydown', async (event) => {
    if (event.code === 'AltLeft' && !event.repeat && !isTranslating) {
      const selectedText = getSelectedText();

      if (selectedText && selectedText.trim().length > 0) {
        event.preventDefault();
        await translateAndReplace(selectedText);
      }
    }
  });

  function getSelectedText() {
    const activeElement = document.activeElement;

    if (activeElement && (activeElement.tagName === 'INPUT' || activeElement.tagName === 'TEXTAREA')) {
      const start = activeElement.selectionStart;
      const end = activeElement.selectionEnd;
      if (start !== end) {
        return activeElement.value.substring(start, end);
      }
    }

    const selection = window.getSelection();
    if (selection && selection.toString().trim().length > 0) {
      return selection.toString();
    }

    return null;
  }

  async function translateAndReplace(text) {
    isTranslating = true;

    try {
      const response = await chrome.runtime.sendMessage({
        action: 'translate',
        text: text,
        sourceLang: 'FR',
        targetLang: 'EN'
      });

      if (response.translatedText) {
        replaceSelectedText(response.translatedText);
      }
    } catch (error) {
      console.error('Flyff Translate - Erreur:', error);
    } finally {
      isTranslating = false;
    }
  }

  function replaceSelectedText(newText) {
    const activeElement = document.activeElement;

    if (activeElement && (activeElement.tagName === 'INPUT' || activeElement.tagName === 'TEXTAREA')) {
      const start = activeElement.selectionStart;
      const end = activeElement.selectionEnd;
      const value = activeElement.value;

      activeElement.value = value.substring(0, start) + newText + value.substring(end);
      activeElement.selectionStart = start + newText.length;
      activeElement.selectionEnd = start + newText.length;

      activeElement.dispatchEvent(new Event('input', { bubbles: true }));
      activeElement.dispatchEvent(new Event('change', { bubbles: true }));
      return;
    }

    const selection = window.getSelection();
    if (selection && selection.rangeCount > 0) {
      const range = selection.getRangeAt(0);
      const container = range.commonAncestorContainer;
      const editableParent = container.nodeType === 3 ? container.parentElement : container;

      if (editableParent && (editableParent.isContentEditable || editableParent.closest('[contenteditable="true"]'))) {
        range.deleteContents();
        range.insertNode(document.createTextNode(newText));
        selection.collapseToEnd();
        editableParent.dispatchEvent(new Event('input', { bubbles: true }));
      }
    }
  }

  console.log('Flyff Translate: Extension chargée. Alt gauche pour traduire.');
})();
