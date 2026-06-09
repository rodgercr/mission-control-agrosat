"""Interface CLI estilo Claude Code — usa Rich + prompt-toolkit.

Banner ASCII + painéis Rich + input editável com prompt-toolkit.
"""
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from prompt_toolkit import PromptSession
from prompt_toolkit.styles import Style
import pyfiglet
from datetime import datetime

console = Console()
_session = None


def _get_session() -> PromptSession:
    global _session
    if _session is None:
        _session = PromptSession(style=Style.from_dict({"prompt": "#06B6D4 bold"}))
    return _session


# ---------------------------------------------------------------------------
# Componentes visuais
# ---------------------------------------------------------------------------

def show_banner() -> None:
    """Exibe o banner ASCII colorido e o card de boas-vindas."""
    try:
        banner = pyfiglet.figlet_format("Mission Control", font="ansi_shadow")
        console.print(Text(banner, style="bold #06B6D4"))
    except Exception:
        console.print(Text("MISSION CONTROL AI", style="bold #06B6D4"))

    console.print(Panel.fit(
        "[bold cyan]AgroSat-1[/bold cyan] · Satélite de sensoriamento multiespectral · LEO 620km\n"
        "Sistema de monitoramento e análise por [bold]IA generativa[/bold] (gpt-oss:120b via Ollama Cloud)\n\n"
        "  [cyan]/help[/cyan]    comandos disponíveis     [cyan]/status[/cyan]   telemetria atual\n"
        "  [cyan]/critico[/cyan] simula crise             [cyan]/normal[/cyan]   simula operação nominal\n"
        "  [cyan]/about[/cyan]   sobre o projeto          [cyan]/exit[/cyan]     encerrar",
        title="◆ MISSION CONTROL AI · Trilha AgroSat",
        border_style="#06B6D4",
    ))


def show_response(text: str, title: str = "◆ Mission Control") -> None:
    """Exibe a resposta da IA em painel com timestamp."""
    now = datetime.now().strftime("%H:%M")
    console.print(Panel(text, title=title, subtitle=now, border_style="#06B6D4"))


def show_help() -> None:
    """Exibe tabela de comandos disponíveis."""
    tabela = Table(title="Comandos disponíveis", border_style="#06B6D4", show_header=True)
    tabela.add_column("Comando", style="cyan bold", width=12)
    tabela.add_column("Descrição")
    tabela.add_row("/help",    "Exibe esta tabela de comandos")
    tabela.add_row("/status",  "Snapshot da telemetria atual em tempo real")
    tabela.add_row("/critico", "Simula cenário de crise (múltiplos alertas críticos)")
    tabela.add_row("/normal",  "Simula operação 100% nominal")
    tabela.add_row("/about",   "Sobre o projeto — AgroSat e impacto no agronegócio")
    tabela.add_row("/clear",   "Limpa o terminal e reexibe o banner")
    tabela.add_row("/exit",    "Encerra o Mission Control AI")
    tabela.add_row("[dim]<texto>[/dim]", "[dim]Qualquer pergunta livre → analisada pela IA com telemetria em tempo real[/dim]")
    console.print(tabela)


# ---------------------------------------------------------------------------
# Loop principal
# ---------------------------------------------------------------------------

def run_cli(engine) -> None:
    """Loop principal da CLI — recebe input, despacha para o motor de análise."""
    show_banner()

    if not engine.is_ready():
        console.print("  ⚠ Engine status: AGUARDANDO IMPLEMENTAÇÃO ✗\n", style="yellow")

    while True:
        try:
            user_input = _get_session().prompt("❯ ").strip()
        except (KeyboardInterrupt, EOFError):
            console.print("\n[dim]Encerrando Mission Control AI. Até logo![/dim]")
            break

        if not user_input:
            continue

        # --- Comandos de sistema ---
        if user_input == "/exit":
            console.print("[dim]Encerrando Mission Control AI. Até logo![/dim]")
            break

        if user_input == "/help":
            show_help()
            continue

        if user_input == "/clear":
            console.clear()
            show_banner()
            continue

        if user_input == "/about":
            show_response(
                "[bold]Mission Control AI — Trilha AgroSat[/bold]\n"
                "Global Solution 2026.1 · FIAP · Ciência da Computação\n"
                "Disciplina: Prompt Engineering and Artificial Intelligence\n\n"
                "[bold cyan]O que monitora:[/bold cyan]\n"
                "  Satélite AgroSat-1 — sensoriamento multiespectral LEO ~620km\n"
                "  Parâmetros: NDVI, temperatura, armazenamento, downlink, atitude, energia, sinal\n\n"
                "[bold cyan]Impacto terrestre:[/bold cyan]\n"
                "  Produtores rurais do Brasil Central dependem de índices NDVI via satélite\n"
                "  para decisões de irrigação, aplicação de insumos e acionamento de seguro rural.\n"
                "  Uma falha no sensor NDVI impacta diretamente a gestão de milhões de hectares.",
                title="◆ Sobre o Projeto"
            )
            continue

        if user_input == "/status":
            with console.status("[bold cyan]Coletando telemetria do AgroSat-1...[/bold cyan]"):
                snapshot = engine.status_snapshot()
            show_response(snapshot, title="◆ Telemetria AgroSat-1")
            continue

        if user_input == "/critico":
            console.print("[bold red]⚠ Simulando cenário crítico...[/bold red]")
            with console.status("[bold red]Analisando situação de emergência...[/bold red]"):
                resposta = engine.analyze_critico(
                    "Analise o estado crítico atual da missão. "
                    "Quais são os riscos imediatos para as operações e para os produtores rurais que dependem dos dados?"
                )
            show_response(resposta, title="◆ Análise — Cenário Crítico 🔴")
            continue

        if user_input == "/normal":
            console.print("[bold green]✓ Simulando operação nominal...[/bold green]")
            with console.status("[bold green]Confirmando status nominal...[/bold green]"):
                resposta = engine.analyze_normal(
                    "Confirme o status nominal da missão e descreva o impacto positivo "
                    "que a operação saudável do AgroSat-1 gera no campo hoje."
                )
            show_response(resposta, title="◆ Análise — Operação Normal ✅")
            continue

        # --- Pergunta livre → IA ---
        with console.status("[bold cyan]Consultando Mission Control AI...[/bold cyan]"):
            resposta = engine.analyze(user_input)
        show_response(resposta)
