// Flyff Translate - Content Script
// Appuyez sur Alt gauche pour traduire le texte du champ actif (FR → EN)

(function() {
  'use strict';

  let isTranslating = false;

  document.addEventListener('keydown', async (event) => {
    if (event.code === 'AltLeft' && !event.repeat && !isTranslating) {
      const textInfo = getTextToTranslate();

      if (textInfo && textInfo.text.trim().length > 0) {
        event.preventDefault();
        await translateAndReplace(textInfo);
      }
    }
  });

  function getTextToTranslate() {
    const activeElement = document.activeElement;

    if (activeElement && (activeElement.tagName === 'INPUT' || activeElement.tagName === 'TEXTAREA')) {
      const start = activeElement.selectionStart;
      const end = activeElement.selectionEnd;

      // Si du texte est sélectionné, traduire la sélection
      if (start !== end) {
        return {
          text: activeElement.value.substring(start, end),
          isFullField: false,
          element: activeElement
        };
      }

      // Sinon, traduire tout le contenu du champ
      if (activeElement.value.trim().length > 0) {
        return {
          text: activeElement.value,
          isFullField: true,
          element: activeElement
        };
      }
    }

    const selection = window.getSelection();
    if (selection && selection.toString().trim().length > 0) {
      return {
        text: selection.toString(),
        isFullField: false,
        element: null
      };
    }

    return null;
  }

  async function translateAndReplace(textInfo) {
    isTranslating = true;

    try {
      const response = await chrome.runtime.sendMessage({
        action: 'translate',
        text: textInfo.text,
        sourceLang: 'FR',
        targetLang: 'EN'
      });

      if (response.translatedText) {
        replaceText(response.translatedText, textInfo);
      }
    } catch (error) {
      console.error('Flyff Translate - Erreur:', error);
    } finally {
      isTranslating = false;
    }
  }

  function replaceText(newText, textInfo) {
    // Si c'est un champ input/textarea
    if (textInfo.element && (textInfo.element.tagName === 'INPUT' || textInfo.element.tagName === 'TEXTAREA')) {
      if (textInfo.isFullField) {
        // Remplacer tout le contenu du champ
        textInfo.element.value = newText;
        textInfo.element.selectionStart = newText.length;
        textInfo.element.selectionEnd = newText.length;
      } else {
        // Remplacer seulement la sélection
        const start = textInfo.element.selectionStart;
        const end = textInfo.element.selectionEnd;
        const value = textInfo.element.value;

        textInfo.element.value = value.substring(0, start) + newText + value.substring(end);
        textInfo.element.selectionStart = start + newText.length;
        textInfo.element.selectionEnd = start + newText.length;
      }

      textInfo.element.dispatchEvent(new Event('input', { bubbles: true }));
      textInfo.element.dispatchEvent(new Event('change', { bubbles: true }));
      return;
    }

    // Pour les éléments contenteditable
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
