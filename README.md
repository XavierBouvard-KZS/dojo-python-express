# Encryption script dojo

## 📄 Sommaire

- [Encryption script dojo](#encryption-script-dojo)
  - [📄 Sommaire](#-sommaire)
  - [Présentation](#présentation)
  - [Déroulé du dojo](#déroulé-du-dojo)
  - [Corrections](#corrections)
  - [🛡️ Documentation Technique – Script de Chiffrement/Déchiffrement AES-256 CBC](#️-documentation-technique--script-de-chiffrementdéchiffrement-aes-256-cbc)
    - [🔍 Vue d'ensemble](#-vue-densemble)
    - [🔐 Processus de chiffrement](#-processus-de-chiffrement)
    - [🔓 Processus de déchiffrement](#-processus-de-déchiffrement)
    - [📚 Protocoles et algorithmes utilisés](#-protocoles-et-algorithmes-utilisés)
    - [⚠️ Pourquoi ce processus est-il sécurisé mais non réversible sans mot de passe ?](#️-pourquoi-ce-processus-est-il-sécurisé-mais-non-réversible-sans-mot-de-passe-)
    - [💻 Utilisation du script en ligne de commande](#-utilisation-du-script-en-ligne-de-commande)
    - [📎 Exemple d'utilisation](#-exemple-dutilisation)
      - [🔒 Chiffrement d'un fichier](#-chiffrement-dun-fichier)
      - [🔒 Chiffrement d'un fichier (avec suppression de l'original)](#-chiffrement-dun-fichier-avec-suppression-de-loriginal)
      - [🔓 Déchiffrement d'un fichier](#-déchiffrement-dun-fichier)
      - [🔓 Déchiffrement d'un fichier (avec suppression du chiffré)](#-déchiffrement-dun-fichier-avec-suppression-du-chiffré)
    - [⚙️ Test du script](#️-test-du-script)
      - [🔍 Fonctionnement du fichier de test](#-fonctionnement-du-fichier-de-test)
        - [Étapes réalisées](#étapes-réalisées)
      - [🧪 Ajouter de nouveaux tests](#-ajouter-de-nouveaux-tests)

---

## Présentation

L'objectif de ce dojo est de faire un exercice d'industrialisation de code python en utilisant les outils recents (2024 / 2025) apparu dans l'ecosystème.

L'arrivée de `uv`, `ruff` et confrère a révolutionné l'usage de python pour lui permettre d'arriver à un niveau d'industrialisation équivalent aux autres langages (TS / C# / Java / Rust / go / etc.).

Ce dojo reprend le code source in situ développé par un stagiaire permettant de prendre un cas concret et d'en faire l'industrialisation.

Excepté pour ce readme (dont la réalisation originel est encore présente), le code n'a pas été modifié pour en préserver les actions.

## Déroulé du dojo

Ce Dojo se déroule en 6 étapes dont voici le contenu et les branches contenant les corrections:

| Etape                      | Technologie             | Branche                             |
|----------------------------|-------------------------|-------------------------------------|
| 1. uv                      | uv                      | steps/1-add-uv                      |
| 2. ruff                    | ruff                    | steps/2-add-ruff                    |
| 3. ty & mypy               | ty & mypy               | steps/3-add-ty-mypy                 |
| 4. pytest                  | pytest                  | steps/4-add-pytest                  |
| 5. python-semantic-release | python-semantic-release | steps/5-add-python-semantic-release |
| 6. gitlab                  | gitlab                  | steps/6-add-gitlab                  |
| 7. github                  | github                  | steps/7-add-github                  |

## Corrections

Cette section contient les corrections pour chacune des étapes.

## 🛡️ Documentation Technique – Script de Chiffrement/Déchiffrement AES-256 CBC

### 🔍 Vue d'ensemble

Ce script permet de **chiffrer et déchiffrer des fichiers** à l’aide de l’algorithme **AES-256 en mode CBC** (Cipher Block Chaining). Il s’appuie sur une **clé dérivée d’un mot de passe utilisateur** via PBKDF2 (Password-Based Key Derivation Function 2) avec SHA-256.

Le script assure :

- La **confidentialité** via AES
- La **résistance aux attaques par force brute** grâce à l’usage d’un sel et d’une fonction de dérivation lente (100 000 itérations)

---

### 🔐 Processus de chiffrement

1. L'utilisateur fournit un mot de passe.
2. Un **sel aléatoire de 16 octets** est généré.
3. Une **clé AES-256 (32 octets)** est dérivée du mot de passe via PBKDF2 + SHA-256.
4. Un **IV aléatoire de 16 octets** (initialisation vector) est généré.
5. Le fichier est lu puis **rempli via PKCS7** pour correspondre à un multiple de la taille de bloc AES (128 bits).
6. Le contenu est chiffré avec AES en mode CBC.
7. Le fichier final est sauvegardé avec l’extension `.enc`, en concaténant : `[SEL (16B)] + [IV (16B)] + [Données chiffrées]`

---

### 🔓 Processus de déchiffrement

1. L'utilisateur fournit un mot de passe.
2. Le script lit :
   - les 16 premiers octets → **sel**
   - les 16 suivants → **IV**
   - le reste → **données chiffrées**
3. La **clé AES est dérivée** à nouveau à partir du mot de passe et du sel.
4. Les données sont **déchiffrées** avec la clé et l'IV.
5. Le padding PKCS7 est **retiré**.
6. Le fichier déchiffré est écrit sans l’extension `.enc`.

---

### 📚 Protocoles et algorithmes utilisés

| Composant                       | Description                                                                                                                        |
| ------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| **PBKDF2 + SHA-256**            | Dérivation de clé lente pour transformer un mot de passe en clé robuste. Protège contre les attaques par dictionnaire/brute force. |
| **AES-256**                     | Algorithme de chiffrement symétrique par blocs – robuste et largement utilisé.                                                     |
| **CBC (Cipher Block Chaining)** | Mode de chiffrement nécessitant un vecteur d'initialisation (IV). Permet d’éviter les motifs dans le texte chiffré.                |
| **PKCS7 Padding**               | Ajoute des octets pour que les données s’alignent sur des blocs de 128 bits requis par AES.                                        |
| **SHA-256**                     | Utilisé pour l’empreinte du fichier original (non stockée), à des fins d'intégrité manuelle ou de comparaison.                     |

---

### ⚠️ Pourquoi ce processus est-il sécurisé mais non réversible sans mot de passe ?

Le chiffrement **n'est réversible que si le mot de passe exact est fourni**.

- Le **sel** garantit que deux fichiers chiffrés avec le même mot de passe donneront des clés différentes.
- Le **mot de passe seul ne suffit pas** à retrouver la clé exacte sans connaître le sel.
- Si le mot de passe est incorrect, le **déchiffrement produit une sortie corrompue**, et le padding échoue → erreur contrôlée dans le script.

Cela empêche toute tentative de déchiffrement sans le mot de passe approprié.

---

### 💻 Utilisation du script en ligne de commande

- Installation de `cryptography` avec : `pip install cryptography`

- Le script propose plusieurs options :

| Commande                      | Fonction                                                               |
| ----------------------------- | ---------------------------------------------------------------------- |
| `-e <chemin\vers\le\fichier>` | Chiffre le fichier spécifié                                            |
| `-d <chemin\vers\le\fichier>` | Déchiffre le fichier spécifié                                          |
| `--delete`                    | (optionnel) Supprime le fichier source après chiffrement/déchiffrement |

> 💡 Le mot de passe est demandé en ligne de commande via `getpass` (non affiché à l’écran).

---

### 📎 Exemple d'utilisation

#### 🔒 Chiffrement d'un fichier

```bash
python main.py -e secret.txt
Mot de passe pour chiffrer :
[OK] Fichier chiffré : secret.txt.enc
```

#### 🔒 Chiffrement d'un fichier (avec suppression de l'original)

```bash
python main.py -e secret.txt --delete
Mot de passe pour chiffrer :
[INFO] Fichier source supprimé : secret.txt
[OK] Fichier chiffré : secret.txt.enc
```

#### 🔓 Déchiffrement d'un fichier

```bash
python main.py -d secret.txt.enc
Mot de passe pour déchiffrer :
[OK] Fichier déchiffré : secret.txt
```

#### 🔓 Déchiffrement d'un fichier (avec suppression du chiffré)

```bash
python main.py -d secret.txt.enc --delete
Mot de passe pour déchiffrer :
[INFO] Fichier chiffré supprimé : secret.txt.enc
[OK] Fichier déchiffré : secret.txt
```

---

### ⚙️ Test du script

#### 🔍 Fonctionnement du fichier de test

Le script de test automatise la vérification du chiffrement et du déchiffrement de fichiers à l’aide des fonctions encrypt_file, decrypt_file et sha256sum importées depuis main.py.

##### Étapes réalisées

1. 📂 Recherche tous les fichiers dans le dossier nommé test_fichiers.
2. Pour chaque fichier :
    - 📄 Crée une copie temporaire (.tmp) du fichier à tester
    - 🔐 Chiffre cette copie avec un mot de passe fixe (MotDePasseTest123).
    - 🔓 Déchiffre le fichier chiffré.
    - ✅ Compare les empreintes SHA-256 entre le fichier original et le fichier déchiffré :
        - Si elles sont identiques → test réussi.
        - Sinon → échec.
    - 🧹 Nettoie les fichiers temporaires générés (.tmp, .enc) après chaque test.

Le script affiche les résultats pour chaque fichier avec des ✅ ou ❌ selon l'intégrité.

#### 🧪 Ajouter de nouveaux tests

Pour ajouter de nouveaux fichiers à tester :

- Placer dans le dossier nommé test_fichiers les fichiers à tester :
- Exécuter le script : `python test_chiffrement.py`
- Chaque fichier sera copié, chiffré, déchiffré, puis pour valider le bon fonctionnement.
