from rich.live import Live
from rich.table import Table
from rich.console import Console
from typing import List, Dict, Any

class DisplayManager:
    def __init__(self, total_platforms: int):
        self.total = total_platforms
        self.checked = 0
        self.found = 0
        self.results: List[Dict[str, Any]] = []
        self.console = Console()
        self.table = Table(show_header=True, header_style="bold magenta")
        self.table.add_column("Plateforme", style="cyan", width=20)
        self.table.add_column("Statut", width=15)
        self.table.add_column("URL", style="blue")
        self.table.add_column("Temps", justify="right")
        
        self.live = Live(self.table, console=self.console, refresh_per_second=4)
        
    def start(self):
        self.update_title()
        self.live.start()
        
    def stop(self):
        self.live.stop()
        
    def update_title(self):
        self.table.title = f"Recherche en cours... ({self.checked}/{self.total}) [green]Trouvés: {self.found}[/green]"
        
    def add_result(self, result: dict):
        self.checked += 1
        self.results.append(result)
        
        status = result["status"]
        if status == "FOUND":
            self.found += 1
            status_str = "[green]✓ Trouvé[/green]"
        elif status == "NOT_FOUND":
            status_str = "[dim]· Absent[/dim]"
        else:
            status_str = f"[yellow]? Erreur[/yellow]"
            
        time_str = f"{result['response_time']:.2f}s" if result['response_time'] else "-"
        
        self.table.add_row(
            result["platform"],
            status_str,
            result["url"],
            time_str
        )
        self.update_title()
        
    def show_final_summary(self, found_only: bool = False):
        self.console.print("\n[bold magenta]Résumé Final[/bold magenta]")
        
        summary = Table(show_header=True, header_style="bold magenta")
        summary.add_column("Plateforme", style="cyan")
        summary.add_column("Statut")
        summary.add_column("URL", style="blue")
        summary.add_column("Temps", justify="right")
        
        # Tri : FOUND en premier, puis ordre alphabétique
        sorted_results = sorted(
            self.results, 
            key=lambda x: (0 if x["status"] == "FOUND" else 1, x["platform"])
        )
        
        for r in sorted_results:
            if found_only and r["status"] != "FOUND":
                continue
                
            status_str = "[green]✓ Trouvé[/green]" if r["status"] == "FOUND" else (
                "[dim]· Absent[/dim]" if r["status"] == "NOT_FOUND" else "[yellow]? Erreur[/yellow]"
            )
            time_str = f"{r['response_time']:.2f}s" if r['response_time'] else "-"
            
            summary.add_row(r["platform"], status_str, r["url"], time_str)
            
        self.console.print(summary)
