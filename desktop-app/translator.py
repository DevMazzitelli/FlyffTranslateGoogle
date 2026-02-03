"""
Flyff Translate Desktop - Traduction système-wide avec DeepL
Appuyez sur Alt Gauche pour traduire le texte sélectionné
"""

import keyboard
import pyperclip
import pyautogui
import requests
import time
import sys
from threading import Thread

# Rendre pyautogui ultra rapide (quasi invisible)
pyautogui.PAUSE = 0.005  # Délai minimal entre les actions
pyautogui.FAILSAFE = False  # Désactiver le failsafe pour plus de vitesse

# Configuration
DEEPL_API_KEY = "4029f8a1-ac73-440e-ab3b-64c2ce0464d6:fx"
SOURCE_LANG = "FR"  # Langue source (FR, EN, DE, etc.)
TARGET_LANG = "EN"  # Langue cible
HOTKEY = "alt"  # Touche de raccourci

# URL de l'API DeepL (version gratuite)
DEEPL_API_URL = "https://api-free.deepl.com/v2/translate"

# Protection contre les doubles appels
is_translating = False
last_translate_time = 0


def translate_text(text: str) -> str:
    """Traduit le texte via l'API DeepL"""
    if not DEEPL_API_KEY:
        print("[ERREUR] Clé API DeepL non configurée!")
        print("Obtenez une clé gratuite sur: https://www.deepl.com/pro-api")
        return None

    if not text or not text.strip():
        return None

    try:
        response = requests.post(
            DEEPL_API_URL,
            headers={
                "Authorization": f"DeepL-Auth-Key {DEEPL_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "text": [text],
                "source_lang": SOURCE_LANG,
                "target_lang": TARGET_LANG
            },
            timeout=10
        )

        if response.status_code == 200:
            result = response.json()
            translated = result["translations"][0]["text"]
            return translated
        else:
            print(f"[ERREUR] API DeepL: {response.status_code} - {response.text}")
            return None

    except requests.exceptions.Timeout:
        print("[ERREUR] Timeout - L'API DeepL ne répond pas")
        return None
    except Exception as e:
        print(f"[ERREUR] {e}")
        return None


def get_selected_text() -> str:
    """Copie le texte sélectionné dans le presse-papier et le retourne"""
    # Sauvegarder le contenu actuel du presse-papier
    old_clipboard = ""
    try:
        old_clipboard = pyperclip.paste()
    except:
        pass

    # Vider le presse-papier
    pyperclip.copy("")

    # Relâcher toutes les touches modificatrices
    keyboard.release('alt')
    keyboard.release('ctrl')
    keyboard.release('shift')

    # Sélectionner tout + Copier + Supprimer (ultra rapide)
    pyautogui.hotkey("ctrl", "a", interval=0.01)
    pyautogui.hotkey("ctrl", "c", interval=0.01)
    time.sleep(0.02)  # Délai minimal pour le presse-papier
    pyautogui.press("delete")

    # Récupérer le texte copié
    selected_text = pyperclip.paste()

    # Si rien n'a été copié, restaurer l'ancien contenu
    if not selected_text:
        pyperclip.copy(old_clipboard)
        return None

    return selected_text


def paste_text(text: str):
    """Colle le texte traduit"""
    pyperclip.copy(text)
    pyautogui.hotkey("ctrl", "v", interval=0.01)


def on_translate():
    """Fonction appelée lors de l'appui sur la touche de traduction"""
    global is_translating, last_translate_time

    # Protection contre les doubles appels
    current_time = time.time()
    if is_translating or (current_time - last_translate_time) < 0.5:
        return

    is_translating = True
    last_translate_time = current_time

    try:
        print("\n[...] Traduction en cours...")

        # Récupérer le texte sélectionné
        selected_text = get_selected_text()

        if not selected_text:
            print("[INFO] Aucun texte sélectionné")
            return

        print(f"[ORIGINAL] {selected_text[:50]}{'...' if len(selected_text) > 50 else ''}")

        # Traduire
        translated = translate_text(selected_text)

        if translated:
            print(f"[TRADUIT] {translated[:50]}{'...' if len(translated) > 50 else ''}")
            # Coller le texte traduit
            paste_text(translated)
            print("[OK] Texte traduit et collé!")
        else:
            print("[ERREUR] Échec de la traduction")
    finally:
        is_translating = False


def main():
    print("=" * 50)
    print("  FLYFF TRANSLATE DESKTOP")
    print("  Traduction système-wide avec DeepL")
    print("=" * 50)
    print()

    if not DEEPL_API_KEY:
        print("[!] ATTENTION: Clé API DeepL non configurée!")
        print("    Modifiez DEEPL_API_KEY dans le fichier translator.py")
        print("    Obtenez une clé gratuite: https://www.deepl.com/pro-api")
        print()

    print(f"[CONFIG] {SOURCE_LANG} -> {TARGET_LANG}")
    print(f"[HOTKEY] Appuyez sur '{HOTKEY.upper()}' pour traduire")
    print(f"[QUIT]   Appuyez sur 'Ctrl+Q' pour quitter")
    print()
    print("En attente de traduction...")
    print("-" * 50)

    # Enregistrer le raccourci clavier (Alt seul)
    keyboard.on_release_key(HOTKEY, lambda e: on_translate(), suppress=False)

    # Raccourci pour quitter
    keyboard.add_hotkey("ctrl+q", lambda: sys.exit(0))

    # Garder le programme en cours d'exécution
    keyboard.wait()


if __name__ == "__main__":
    main()
