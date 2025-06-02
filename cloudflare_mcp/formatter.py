"""Rich formatting utilities for MCP results"""

import re
from typing import List, Dict
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.text import Text
from rich.rule import Rule


class MCPResultFormatter:
    """Formats MCP server results with rich formatting"""

    def __init__(self):
        self.console = Console()

    def parse_results(self, raw_result: str) -> List[Dict[str, str]]:
        """Parse the raw MCP result string into structured data"""
        results = []

        # Find all <result> blocks
        result_pattern = r"<result>\s*<url>(.*?)</url>\s*<text>(.*?)</text>\s*</result>"
        matches = re.findall(result_pattern, raw_result, re.DOTALL)

        for url, text in matches:
            results.append({"url": url.strip(), "text": text.strip()})

        return results

    def format_markdown_content(self, text: str) -> Markdown:
        """Format text content as markdown with rich"""
        # Clean up the text content
        cleaned_text = self._clean_markdown_text(text)
        return Markdown(cleaned_text)

    def _clean_markdown_text(self, text: str) -> str:
        """Clean up markdown text for better rendering"""
        # Remove HTML-like tags that aren't standard markdown
        text = re.sub(r"<DirectoryListing />", "*(Directory listing)*", text)
        text = re.sub(r"<Glossary.*?/>", "*(Glossary)*", text)
        text = re.sub(r"<ListTutorials />", "*(Tutorial list)*", text)
        text = re.sub(r"<YouTubeVideos.*?/>", "*(YouTube videos)*", text)
        text = re.sub(r"<GlossaryTooltip.*?>(.*?)</GlossaryTooltip>", r"\1", text)
        text = re.sub(r"<LinkButton.*?>(.*?)</LinkButton>", r"**\1**", text)
        text = re.sub(r"<Description>(.*?)</Description>", r"\1", text)
        text = re.sub(r"<TabItem.*?>", "", text)
        text = re.sub(r"</TabItem>", "", text)
        text = re.sub(r"<Tabs.*?>", "", text)
        text = re.sub(r"</Tabs>", "", text)
        text = re.sub(r":::note(.*?):::", r"> **Note:** \1", text, flags=re.DOTALL)

        return text.strip()

    def format_single_result(self, result: Dict[str, str]) -> Panel:
        """Format a single result with URL and content"""
        url = result["url"]
        text = result["text"]

        # Create the title with the URL
        title_text = Text()
        title_text.append("📄 ", style="bold blue")
        title_text.append(url, style="bold cyan underline")

        # Format the content as markdown
        content = self.format_markdown_content(text)

        # Create a panel with the formatted content
        panel = Panel(
            content,
            title=title_text,
            title_align="left",
            border_style="blue",
            padding=(1, 2),
        )

        return panel

    def format_and_display_results(self, raw_result: str, query: str = None):
        """Parse and display formatted results"""
        results = self.parse_results(raw_result)

        if not results:
            self.console.print("[yellow]No results found in the response.[/yellow]")
            return

        # Display header
        if query:
            self.console.print()
            self.console.print(
                Panel(
                    Text(f"Search Results for: {query}", style="bold white"),
                    style="bold green",
                )
            )
            self.console.print()

        # Display each result
        for i, result in enumerate(results, 1):
            if i > 1:
                self.console.print()  # Add spacing between results

            panel = self.format_single_result(result)
            self.console.print(panel)

        # Display summary
        self.console.print()
        self.console.print(Rule(style="dim"))
        self.console.print(
            f"[dim]Found {len(results)} result{'s' if len(results) != 1 else ''}[/dim]"
        )

    def format_error(self, error_msg: str):
        """Format error messages"""
        self.console.print()
        self.console.print(
            Panel(
                f"[red]Error: {error_msg}[/red]", title="❌ Error", border_style="red"
            )
        )

    def format_info(self, message: str, title: str = "ℹ️  Info"):
        """Format informational messages"""
        self.console.print()
        self.console.print(
            Panel(f"[blue]{message}[/blue]", title=title, border_style="blue")
        )

    def format_success(self, message: str, title: str = "✅ Success"):
        """Format success messages"""
        self.console.print()
        self.console.print(
            Panel(f"[green]{message}[/green]", title=title, border_style="green")
        )
