"""Gerador de banner ASCII art para o Mission Control AI."""
import argparse
import pyfiglet
from rich.console import Console
from rich.align import Align
from rich.text import Text
from rich.rule import Rule

console = Console()


def show_banner(font: str = "ansi_shadow") -> None:
    """Exibe o banner principal do projeto."""
    try:
        linha1 = pyfiglet.figlet_format("Global Solution", font=font)
        linha2 = pyfiglet.figlet_format("Mission Control AI", font=font)
    except pyfiglet.FontNotFound:
        linha1 = pyfiglet.figlet_format("Global Solution", font="standard")
        linha2 = pyfiglet.figlet_format("Mission Control AI", font="standard")

    console.print(Align.center(Text(linha1, style="bold #A855F7")))
    console.print(Align.center(Text(linha2, style="bold #06B6D4")))
    console.print(Align.center(
        Text("── 2026.1 · Prompt Engineering and AI · FIAP ──",
             style="italic #8484A0")
    ))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Gerador de banner ASCII para Mission Control AI")
    parser.add_argument("--fonts", action="store_true", help="Listar fontes disponíveis")
    parser.add_argument("--font", default="ansi_shadow", help="Fonte a usar no banner")
    parser.add_argument("--text", default="Mission Control AI", help="Texto personalizado")
    parser.add_argument("--demo", action="store_true", help="Demonstrar 8 fontes lado a lado")
    args = parser.parse_args()

    if args.fonts:
        fontes = pyfiglet.FigletFont.getFonts()
        console.print(f"[bold cyan]{len(fontes)} fontes disponíveis:[/bold cyan]")
        for i, f in enumerate(fontes):
            print(f"  {f}", end="\n" if (i + 1) % 4 == 0 else "\t")
    elif args.demo:
        demo_fonts = ["ansi_shadow", "slant", "banner3-D", "doom", "epic", "graffiti", "larry3d", "standard"]
        for font in demo_fonts:
            try:
                console.print(Rule(f"[dim]{font}[/dim]"))
                console.print(Text(pyfiglet.figlet_format(args.text, font=font), style="bold #06B6D4"))
            except Exception:
                pass
    else:
        show_banner(args.font)
