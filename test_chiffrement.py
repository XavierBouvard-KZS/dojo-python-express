import os
import shutil
from main import encrypt_file, decrypt_file, sha256sum

# === PARAMÈTRES DE TEST ===
DOSSIER_TEST = "test_fichiers"
MOT_DE_PASSE = "MotDePasseTest123"

def fichiers_identiques(file1, file2):
    return sha256sum(file1) == sha256sum(file2)

def tester_chiffrement_dossier(dossier):
    fichiers = [f for f in os.listdir(dossier) if os.path.isfile(os.path.join(dossier, f))]
    print(f"🔍 Test de {len(fichiers)} fichiers dans le dossier '{dossier}'...\n")

    for fichier in fichiers:
        chemin = os.path.join(dossier, fichier)
        chemin_temp = chemin + ".tmp"  # Copie temporaire

        print(f"🗂️ Fichier : {fichier}")

        # Créer une copie du fichier
        shutil.copyfile(chemin, chemin_temp)

        # Chiffrement
        encrypt_file(chemin_temp, MOT_DE_PASSE)

        fichier_chiffre = chemin_temp + ".enc"

        # Déchiffrement (produira le fichier temp original)
        decrypt_file(fichier_chiffre, MOT_DE_PASSE)

        # Vérification : fichier déchiffré doit correspondre au fichier initial
        if fichiers_identiques(chemin, chemin_temp):
            print(f"✅ {fichier} : original et déchiffré identiques.")
        else:
            print(f"❌ {fichier} : ⚠️ original ≠ déchiffré !")

        # Nettoyage
        os.remove(chemin_temp)
        os.remove(fichier_chiffre)

        print("----")

if __name__ == "__main__":
    if not os.path.isdir(DOSSIER_TEST):
        print(f"❌ Dossier '{DOSSIER_TEST}' introuvable.")
    else:
        tester_chiffrement_dossier(DOSSIER_TEST)
