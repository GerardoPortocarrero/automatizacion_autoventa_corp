from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

def show_df(df):
    console = Console()

    # Crear tabla de columnas y tipos
    table = Table(show_header=True, header_style="bold white on dark_red", box=box.SQUARE)
    table.title = "📊 Estructura del DataFrame"
    table.add_column("🧱 Columna", style="bold cyan", no_wrap=True)
    table.add_column("📂 Tipo de Dato", style="bold magenta")

    for col in df.columns:
        table.add_row(col, str(df[col].dtype))

    # Dimensión y memoria
    rows, cols = df.shape
    mem_kb = df.memory_usage(deep=True).sum() / 1024
    resumen = (
        f"[bold yellow]🔢 Dimensión:[/bold yellow] {rows} filas × {cols} columnas\n"
        f"[bold green]💾 Memoria usada:[/bold green] {mem_kb:.2f} KB"
    )

    # Mostrar en un panel unificado
    console.print(Panel.fit(table, title="📋 Columnas"))
    console.print(Panel.fit(resumen, title="📎 Resumen", border_style="grey50"))
