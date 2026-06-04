import argparse
import asyncio
import httpx
import yaml
import os
import sys
from typing import List, Dict, Any

from hunter.checker import check_platform
from hunter.display import DisplayManager
from hunter.exporter import export_results

def load_platforms(filepath: str, categories: List[str] = None) -> List[Dict[str, Any]]:
    if not os.path.exists(filepath):
        print(f"Erreur: Le fichier {filepath} est introuvable.")
        sys.exit(1)
        
    with open(filepath, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
        
    platforms = data.get("platforms", [])
    
    if categories:
        cats = [c.lower().strip() for c in categories]
        platforms = [p for p in platforms if p.get("category", "").lower() in cats]
        
    return platforms

async def main_async(args):
    platforms = load_platforms("data/platforms.yaml", args.platforms.split(",") if args.platforms else None)
    
    if not platforms:
        print("Aucune plateforme trouvée avec ces critères.")
        return

    username = "johndoe" if args.demo else args.username
    if not username:
        print("Erreur: Vous devez spécifier un pseudo ou utiliser --demo.")
        sys.exit(1)

    display = DisplayManager(total_platforms=len(platforms))
    
    # Configuration du client HTTP
    timeout = httpx.Timeout(args.timeout)
    proxies = {"all://": args.proxy} if args.proxy else None
    limits = httpx.Limits(max_connections=50, max_keepalive_connections=10)
    
    display.start()
    try:
        async with httpx.AsyncClient(timeout=timeout, proxy=args.proxy if args.proxy else None, limits=limits) as client:
            tasks = []
            for plat in platforms:
                task = check_platform(username, plat, client, args.strict)
                tasks.append(task)
            
            # Utilisation de asyncio.as_completed pour affichage en temps réel
            for future in asyncio.as_completed(tasks):
                result = await future
                display.add_result(result)
                
    except Exception as e:
        display.stop()
        print(f"Erreur fatale: {e}")
        return
        
    display.stop()
    display.show_final_summary(found_only=args.found_only)
    
    json_path, txt_path = export_results(username, display.results, args.output_dir)
    print(f"\nRésultats exportés vers:\n- {json_path}\n- {txt_path}")

def main():
    parser = argparse.ArgumentParser(description="Username Hunter CLI - Outil OSINT")
    parser.add_argument("username", nargs="?", help="Le pseudo à rechercher")
    parser.add_argument("--demo", action="store_true", help="Lancer en mode démo avec le pseudo 'johndoe'")
    parser.add_argument("--output-dir", default="results", help="Dossier d'export (défaut: results)")
    parser.add_argument("--found-only", action="store_true", help="N'afficher que les comptes trouvés")
    parser.add_argument("--platforms", help="Filtrer par catégories, ex: gaming,social")
    parser.add_argument("--proxy", help="URL du proxy, ex: socks5://127.0.0.1:9050")
    parser.add_argument("--strict", action="store_true", help="Mode strict pour éviter les faux positifs")
    parser.add_argument("--timeout", type=float, default=8.0, help="Timeout par requête en secondes (défaut: 8s)")
    
    args = parser.parse_args()
    
    if not args.username and not args.demo:
        parser.print_help()
        sys.exit(1)
        
    asyncio.run(main_async(args))

if __name__ == "__main__":
    main()
