# Flyff Translate Desktop

Application de traduction système-wide utilisant l'API DeepL. Fonctionne partout sur votre PC (jeux, navigateurs, Discord, etc.).

## Installation

### 1. Installer Python
Téléchargez Python 3.8+ depuis [python.org](https://www.python.org/downloads/)

### 2. Installer les dépendances
```bash
cd desktop-app
pip install -r requirements.txt
```

### 3. Configurer la clé API DeepL
1. Créez un compte gratuit sur [DeepL API](https://www.deepl.com/pro-api)
2. Récupérez votre clé API
3. Ouvrez `translator.py` et modifiez la ligne :
```python
DEEPL_API_KEY = "votre-clé-api-ici"
```

### 4. (Optionnel) Configurer les langues
```python
SOURCE_LANG = "FR"  # Langue source
TARGET_LANG = "EN"  # Langue cible
```

## Utilisation

### Lancer l'application
```bash
python translator.py
```

### Traduire du texte
1. Sélectionnez du texte n'importe où sur votre PC
2. Appuyez sur **Alt** (gauche)
3. Le texte est automatiquement traduit et remplacé

### Raccourcis
- `Alt` : Traduire le texte sélectionné
- `Ctrl+Q` : Quitter l'application

## Codes de langues DeepL

| Code | Langue |
|------|--------|
| FR | Français |
| EN | Anglais |
| DE | Allemand |
| ES | Espagnol |
| IT | Italien |
| PT | Portugais |
| NL | Néerlandais |
| PL | Polonais |
| RU | Russe |
| JA | Japonais |
| ZH | Chinois |
| KO | Coréen |

## Créer un exécutable (.exe)

Pour créer un fichier .exe standalone :

```bash
pip install pyinstaller
pyinstaller --onefile --noconsole translator.py
```

L'exécutable sera dans le dossier `dist/`.

## Notes

- L'API DeepL gratuite a une limite de 500 000 caractères/mois
- L'application nécessite les droits administrateur pour les raccourcis globaux
- Fonctionne sur Windows (testé sur Windows 10/11)
