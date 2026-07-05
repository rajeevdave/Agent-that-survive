"""
Example Application: Customer Support Agent

A complete, deployable customer support system using all 12 patterns.
Wraps the ProductionSupportAgent with a simple CLI interface.

Run:
    python examples/customer-support/main.py
"""
from __future__ import annotations
import os, sys, uuid
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../src"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../chapters/12-production-agent"))

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich import print as rprint

console = Console()


def run_support_session(customer_email: str) -> None:
    try:
        from production.main import ProductionSupportAgent
    except ImportError:
        console.print("[red]Import error — run from repo root with: python examples/customer-support/main.py[/red]")
        return

    session_id = str(uuid.uuid4())[:8]
    agent = ProductionSupportAgent(customer_email=customer_email)

    console.print(Panel(
        f"[bold blue]Customer Support Agent[/bold blue]\n"
        f"Session: {session_id} | Customer: {customer_email}\n"
        "Type 'quit' to exit",
        title="🤖 Agentic Design Patterns — Chapter 12"
    ))

    while True:
        try:
            user_input = Prompt.ask("\n[bold green]You[/bold green]")
        except (EOFError, KeyboardInterrupt):
            break

        if user_input.lower() in ("quit", "exit", "q"):
            break

        with console.status("Processing..."):
            try:
                result = agent.respond(user_input, session_id=session_id)
            except Exception as exc:
                console.print(f"[red]Error: {exc}[/red]")
                console.print("[yellow]Tip: Configure API keys in .env[/yellow]")
                break

        console.print(f"\n[bold blue]Agent[/bold blue]: {result['response']}")
        console.print(
            f"[dim]Intent: {result['intent']} | "
            f"Tools: {result.get('tool_calls', [])} | "
            f"Action: {result['action']}[/dim]"
        )

        if result["action"] == "escalate":
            console.print("\n[yellow]⚠️  Escalated to human agent[/yellow]")
            break

    console.print("\n[dim]Session ended[/dim]")


if __name__ == "__main__":
    email = sys.argv[1] if len(sys.argv) > 1 else "jane@example.com"
    run_support_session(email)
