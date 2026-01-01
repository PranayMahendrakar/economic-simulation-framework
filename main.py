#!/usr/bin/env python3
"""
Integrated Economic Simulation Framework
Author: Pranay M.

Comprehensive economic model that can predict emergent properties
of policy changes across global markets.
"""

import ollama
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.markdown import Markdown
from rich.prompt import Prompt
import json
import sys

console = Console()

BANNER = """
╔═══════════════════════════════════════════════════════════════════════════════╗
║            📊 INTEGRATED ECONOMIC SIMULATION FRAMEWORK 📊                      ║
║                    Global Economic Policy Modeling                             ║
║                           Author: Pranay M.                                    ║
╚═══════════════════════════════════════════════════════════════════════════════╝
"""

MODULES = {
    "1": ("Policy Analyzer", "policy", "Analyze economic policy impacts"),
    "2": ("Market Simulator", "market", "Simulate market dynamics"),
    "3": ("Trade Flow Modeler", "trade", "Model international trade flows"),
    "4": ("Monetary Policy Engine", "monetary", "Analyze monetary policy effects"),
    "5": ("Fiscal Impact Assessor", "fiscal", "Assess fiscal policy impacts"),
    "6": ("Labor Market Modeler", "labor", "Model labor market dynamics"),
    "7": ("Financial System Analyzer", "financial", "Analyze financial system stability"),
    "8": ("Emergent Property Detector", "emergent", "Detect emergent economic properties"),
    "9": ("Scenario Comparator", "scenario", "Compare economic scenarios"),
    "10": ("Economic Dashboard", "dashboard", "View economic simulation dashboard")
}

SYSTEM_PROMPTS = {
    "policy": """You are an expert economist specializing in policy analysis.

For each policy analysis, evaluate:

1. **Policy Description**: What the policy does
2. **Direct Effects**: Immediate economic impacts
3. **Indirect Effects**: Secondary and tertiary effects
4. **Sector Impacts**: Effects on different sectors
5. **Distributional Effects**: Who wins, who loses
6. **Long-term Dynamics**: Evolution over time

Analyze economic policy impacts comprehensively.""",

    "market": """You are an expert in market dynamics and simulation.

For each market simulation, model:

1. **Market Structure**: Players, rules, mechanisms
2. **Supply Dynamics**: Production, capacity, costs
3. **Demand Dynamics**: Consumer behavior, preferences
4. **Price Formation**: How prices are determined
5. **Equilibrium Analysis**: Market equilibrium conditions
6. **Shock Response**: How market responds to changes

Simulate market dynamics under various conditions.""",

    "trade": """You are an expert in international trade and economics.

For each trade flow model, analyze:

1. **Trade Patterns**: Current flows, partners, commodities
2. **Comparative Advantage**: What drives trade patterns
3. **Trade Policy Effects**: Tariffs, agreements, barriers
4. **Exchange Rate Impacts**: Currency effects on trade
5. **Supply Chain Dynamics**: Global value chain effects
6. **Trade Balance Projections**: Import/export forecasts

Model international trade flows and impacts.""",

    "monetary": """You are an expert in monetary policy and central banking.

For each monetary policy analysis, evaluate:

1. **Policy Instruments**: Interest rates, QE, reserve requirements
2. **Transmission Mechanisms**: How policy affects economy
3. **Inflation Dynamics**: Price level effects
4. **Growth Effects**: Output and employment impacts
5. **Exchange Rate Effects**: Currency value changes
6. **Financial Stability**: Banking and market impacts

Analyze monetary policy effects on the economy.""",

    "fiscal": """You are an expert in fiscal policy and public finance.

For each fiscal impact assessment, analyze:

1. **Revenue Effects**: Tax revenue changes
2. **Spending Effects**: Government expenditure impacts
3. **Deficit/Debt Dynamics**: Budget balance evolution
4. **Multiplier Effects**: Fiscal multiplier analysis
5. **Crowding Effects**: Private sector interactions
6. **Sustainability**: Long-term fiscal sustainability

Assess fiscal policy impacts comprehensively.""",

    "labor": """You are an expert in labor economics and market dynamics.

For each labor market model, analyze:

1. **Employment Dynamics**: Job creation/destruction
2. **Wage Determination**: Wage setting mechanisms
3. **Unemployment Types**: Cyclical, structural, frictional
4. **Labor Supply**: Workforce participation, skills
5. **Policy Effects**: Minimum wage, benefits, regulations
6. **Future Trends**: Automation, demographic changes

Model labor market dynamics and trends.""",

    "financial": """You are an expert in financial system stability and risk.

For each financial system analysis, evaluate:

1. **System Structure**: Banks, markets, institutions
2. **Risk Assessment**: Credit, market, liquidity risks
3. **Interconnections**: Systemic linkages
4. **Stress Testing**: Response to shocks
5. **Regulatory Effects**: Policy impact on stability
6. **Crisis Indicators**: Early warning signals

Analyze financial system stability and risks.""",

    "emergent": """You are an expert in complex systems and emergent properties.

For each emergent property detection, identify:

1. **System Interactions**: How components interact
2. **Non-linear Effects**: Threshold behaviors, tipping points
3. **Feedback Loops**: Reinforcing and balancing dynamics
4. **Emergent Patterns**: Properties arising from interactions
5. **Cascade Potential**: How changes propagate
6. **Prediction Challenges**: What's hard to foresee

Detect emergent properties in economic systems.""",

    "scenario": """You are an expert in economic scenario analysis.

For each scenario comparison, provide:

1. **Scenario Definitions**: Alternative futures modeled
2. **Key Assumptions**: What differs between scenarios
3. **Outcome Comparison**: Results across scenarios
4. **Sensitivity Analysis**: What drives differences
5. **Probability Assessment**: Likelihood of scenarios
6. **Strategic Implications**: What scenarios mean for decisions

Compare economic scenarios and their implications.""",

    "dashboard": """You are an expert in economic analytics and visualization.

For each dashboard, generate:

1. **Economic Overview**: Key indicators, current state
2. **Policy Simulations**: Active scenarios being modeled
3. **Market Status**: Major market conditions
4. **Risk Indicators**: Economic risk metrics
5. **Forecast Summary**: Projections and confidence
6. **Alert Items**: Issues requiring attention

View economic simulation dashboard."""
}

def get_multiline_input(prompt_text):
    console.print(f"\n[cyan]{prompt_text}[/cyan]")
    console.print("[dim](Type 'END' on a new line when finished)[/dim]\n")
    lines = []
    while True:
        try:
            line = input()
            if line.strip().upper() == 'END':
                break
            lines.append(line)
        except EOFError:
            break
    return '\n'.join(lines)

def query_llama(system_prompt, user_input):
    try:
        response = ollama.chat(model='llama3.2', messages=[
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': user_input}
        ])
        return response['message']['content']
    except Exception as e:
        return f"Error: {str(e)}\n\nMake sure Ollama is running."

def display_menu():
    console.print(BANNER, style="bold blue")
    table = Table(title="📊 Economic Simulation Modules", show_header=True, header_style="bold magenta")
    table.add_column("Option", style="cyan", width=8)
    table.add_column("Module", style="green", width=28)
    table.add_column("Description", style="white", width=42)
    for key, (name, _, desc) in MODULES.items():
        table.add_row(key, name, desc)
    table.add_row("0", "Exit", "Exit the application")
    console.print(table)

def run_module(module_key):
    name, key, desc = MODULES[module_key]
    console.print(Panel(f"📊 {name}", style="bold green"))
    user_input = get_multiline_input(f"Describe your {name.lower()} request:")
    with console.status(f"[bold green]Processing {name}..."):
        response = query_llama(SYSTEM_PROMPTS[key], user_input)
    console.print(Panel(Markdown(response), title=f"📊 {name} Results", border_style="green"))

def main():
    while True:
        display_menu()
        choice = Prompt.ask("\nSelect a module", choices=["0","1","2","3","4","5","6","7","8","9","10"])
        if choice == "0":
            console.print("\n[yellow]Thank you for using the Economic Simulation Framework![/yellow]")
            console.print("[dim]Author: Pranay M.[/dim]\n")
            break
        try:
            run_module(choice)
        except KeyboardInterrupt:
            console.print("\n[yellow]Operation cancelled.[/yellow]")
        except Exception as e:
            console.print(f"\n[red]Error: {str(e)}[/red]")
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
