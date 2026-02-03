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
import os
from threading import Thread

# System tray
import pystray
from PIL import Image, ImageDraw

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

# Référence globale pour le tray icon
tray_icon = None


def create_icon_image():
    """Crée une icône simple pour le system tray"""
    # Créer une image 64x64 avec un fond bleu et un T blanc
    size = 64
    image = Image.new('RGB', (size, size), color=(41, 128, 185))  # Bleu
    draw = ImageDraw.Draw(image)

    # Dessiner un "T" blanc pour "Translate"
    draw.rectangle([20, 15, 44, 22], fill='white')  # Barre horizontale du T
    draw.rectangle([28, 15, 36, 50], fill='white')  # Barre verticale du T

    return image


def on_quit(icon, item):
    """Quitter l'application"""
    icon.stop()
    os._exit(0)


def translate_text(text: str) -> str:
    """Traduit le texte via l'API DeepL"""
    if not DEEPL_API_KEY:
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
            return None

    except:
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
        # Récupérer le texte sélectionné
        selected_text = get_selected_text()

        if not selected_text:
            return

        # Traduire
        translated = translate_text(selected_text)

        if translated:
            # Coller le texte traduit
            paste_text(translated)
    finally:
        is_translating = False


def setup_keyboard():
    """Configure les raccourcis clavier"""
    # Enregistrer le raccourci clavier (Alt seul)
    keyboard.on_release_key(HOTKEY, lambda e: on_translate(), suppress=False)

    # Raccourci pour quitter
    keyboard.add_hotkey("ctrl+q", lambda: os._exit(0))

    # Garder le thread actif
    keyboard.wait()


def main():
    global tray_icon

    # Lancer les raccourcis clavier dans un thread séparé
    keyboard_thread = Thread(target=setup_keyboard, daemon=True)
    keyboard_thread.start()

    # Créer le menu du system tray
    menu = pystray.Menu(
        pystray.MenuItem(f"Flyff Translate ({SOURCE_LANG} → {TARGET_LANG})", lambda: None, enabled=False),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem("Quitter", on_quit)
    )

    # Créer l'icône du system tray
    tray_icon = pystray.Icon(
        "FlyffTranslate",
        create_icon_image(),
        "Flyff Translate - Appuyez sur Alt pour traduire",
        menu
    )

    # Lancer le system tray (bloquant)
    tray_icon.run()


if __name__ == "__main__":
    main()
