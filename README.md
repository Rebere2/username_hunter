# Username Hunter CLI

Username Hunter CLI est un outil OSINT asynchrone conçu pour vérifier l'existence d'un pseudonyme sur plus de 80 plateformes en ligne. L'outil utilise des requêtes asynchrones pour offrir des performances optimales et présente les résultats en temps réel directement dans le terminal.

## Utilisation Légale et Éthique

Cet outil a été conçu uniquement à des fins de recherche légale, de vérification de sa propre empreinte numérique, ou d'investigation OSINT basée sur des données publiques. L'utilisateur est seul responsable de l'utilisation qu'il fait de cet outil. L'utilisation à des fins de harcèlement, de scraping abusif, ou de toute activité illégale est strictement interdite.

## Fonctionnalités

- Vérification asynchrone extrêmement rapide sur de multiples plateformes.
- Affichage en direct des résultats grâce à une interface terminal interactive et esthétique.
- Export automatique des résultats au format JSON et texte brut.
- Rotation automatique des User-Agents pour éviter les blocages de sécurité.
- Filtrage par catégories de plateformes (Développement, Gaming, Réseaux sociaux, etc.).
- Mode strict disponible pour limiter les faux positifs.
- Prise en charge des connexions via proxy (par exemple Tor).

## Démonstration

![Démonstration de Username Hunter CLI](demo.gif)

## Installation

Assurez-vous d'avoir Python 3.11 ou une version supérieure installée sur votre système.

```bash
git clone https://github.com/votre-depot/username-hunter.git
cd username-hunter
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Utilisation

### Recherche basique

```bash
python -m hunter.main johndoe
```

### Options avancées

Exporter uniquement les comptes trouvés dans un dossier spécifique :
```bash
python -m hunter.main johndoe --found-only --output-dir ./resultats
```

Filtrer la recherche par catégories :
```bash
python -m hunter.main johndoe --platforms gaming,social
```

Utiliser un proxy (par exemple avec Tor) :
```bash
python -m hunter.main johndoe --proxy socks5://127.0.0.1:9050
```

Mode démonstration :
```bash
python -m hunter.main --demo
```

## Plateformes Supportées

Le tableau ci-dessous résume les catégories de plateformes actuellement prises en charge :

| Catégorie | Exemples de plateformes |
|-----------|-------------------------|
| Développement | GitHub, GitLab, Bitbucket, npm, PyPI, HackTheBox, Root-Me |
| Gaming | Steam, Xbox, Twitch, Chess.com, Roblox, Minecraft |
| Réseaux Sociaux | Reddit, Twitter, Instagram, TikTok, Mastodon |
| Forums | HackerNews, DEV.to, Medium, StackOverflow |
| Autres | Gravatar, Keybase, Patreon, Wikipedia, Blogger |

Pour ajouter une nouvelle plateforme, il suffit d'ajouter une entrée dans le fichier `data/platforms.yaml`. Aucune modification du code Python n'est nécessaire.

## Licence

Distribué sous la licence MIT. Voir le fichier `LICENSE` pour plus d'informations.
