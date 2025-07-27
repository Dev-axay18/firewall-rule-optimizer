"""
Color utilities and constants for CLI output.
Provides VS Code-like color scheme for terminal interface.
"""

try:
    from colorama import init, Fore, Back, Style
    init(autoreset=True)  # Initialize colorama for Windows
    COLORAMA_AVAILABLE = True
except ImportError:
    # Fallback if colorama is not available
    COLORAMA_AVAILABLE = False
    class Fore:
        RED = GREEN = YELLOW = BLUE = MAGENTA = CYAN = WHITE = RESET = ''
    class Back:
        RED = GREEN = YELLOW = BLUE = MAGENTA = CYAN = WHITE = RESET = ''  
    class Style:
        BRIGHT = DIM = RESET_ALL = ''


class Colors:
    """Color constants and utility methods for CLI output"""
    
    # VS Code-like color scheme
    if COLORAMA_AVAILABLE:
        # Primary colors
        ERROR = Fore.RED + Style.BRIGHT
        SUCCESS = Fore.GREEN + Style.BRIGHT
        WARNING = Fore.YELLOW + Style.BRIGHT
        INFO = Fore.CYAN + Style.BRIGHT
        HEADER = Fore.BLUE + Style.BRIGHT
        HIGHLIGHT = Fore.MAGENTA + Style.BRIGHT
        
        # Secondary colors
        MUTED = Fore.WHITE + Style.DIM
        BOLD = Style.BRIGHT
        RESET = Style.RESET_ALL
        
        # Semantic colors
        CRITICAL = Fore.RED + Back.WHITE + Style.BRIGHT
        HIGH = Fore.RED + Style.BRIGHT
        MEDIUM = Fore.YELLOW + Style.BRIGHT
        LOW = Fore.GREEN + Style.BRIGHT
        
        # Technical colors
        CHAIN = Fore.BLUE + Style.BRIGHT
        PROTOCOL = Fore.CYAN
        ACTION = Fore.MAGENTA + Style.BRIGHT
        PORT = Fore.YELLOW
        IP = Fore.CYAN
        
        # Additional color constants
        BRIGHT_GREEN = Fore.GREEN + Style.BRIGHT
        BRIGHT_RED = Fore.RED + Style.BRIGHT
        BRIGHT_YELLOW = Fore.YELLOW + Style.BRIGHT
        DIM = Style.DIM
        CYAN = Fore.CYAN
        
        # Progress indicators
        PROGRESS_FILL = Fore.GREEN + '█'
        PROGRESS_EMPTY = Fore.WHITE + Style.DIM + '░'
    else:
        # Fallback - no colors
        ERROR = SUCCESS = WARNING = INFO = HEADER = HIGHLIGHT = ''
        MUTED = BOLD = RESET = ''
        CRITICAL = HIGH = MEDIUM = LOW = ''
        CHAIN = PROTOCOL = ACTION = PORT = IP = ''
        BRIGHT_GREEN = BRIGHT_RED = BRIGHT_YELLOW = DIM = CYAN = ''
        PROGRESS_FILL = '█'
        PROGRESS_EMPTY = '░'
    
    @classmethod
    def error(cls, text):
        """Format text as error (red)"""
        return f"{cls.ERROR}{text}{cls.RESET}"
    
    @classmethod
    def success(cls, text):
        """Format text as success (green)"""
        return f"{cls.SUCCESS}{text}{cls.RESET}"
    
    @classmethod
    def warning(cls, text):
        """Format text as warning (yellow)"""
        return f"{cls.WARNING}{text}{cls.RESET}"
    
    @classmethod
    def info(cls, text):
        """Format text as info (cyan)"""
        return f"{cls.INFO}{text}{cls.RESET}"
    
    @classmethod
    def header(cls, text):
        """Format text as header (blue)"""
        return f"{cls.HEADER}{text}{cls.RESET}"
    
    @classmethod
    def highlight(cls, text):
        """Format text as highlight (magenta)"""
        return f"{cls.HIGHLIGHT}{text}{cls.RESET}"
    
    @classmethod
    def muted(cls, text):
        """Format text as muted (dim white)"""
        return f"{cls.MUTED}{text}{cls.RESET}"
    
    @classmethod
    def bold(cls, text):
        """Format text as bold"""
        return f"{cls.BOLD}{text}{cls.RESET}"
    
    @classmethod
    def critical(cls, text):
        """Format text as critical priority"""
        return f"{cls.CRITICAL}{text}{cls.RESET}"
    
    @classmethod
    def high(cls, text):
        """Format text as high priority"""
        return f"{cls.HIGH}{text}{cls.RESET}"
    
    @classmethod
    def medium(cls, text):
        """Format text as medium priority"""
        return f"{cls.MEDIUM}{text}{cls.RESET}"
    
    @classmethod
    def low(cls, text):
        """Format text as low priority"""
        return f"{cls.LOW}{text}{cls.RESET}"
    
    @classmethod
    def subheader(cls, text):
        """Format text as subheader (less prominent than header)"""
        return f"{cls.INFO}{text}{cls.RESET}"
    
    @classmethod
    def count(cls, number, noun="items"):
        """Format count with appropriate pluralization"""
        plural_noun = noun if number == 1 else f"{noun}s" if not noun.endswith('s') else noun
        return f"{cls.HIGHLIGHT}{number} {plural_noun}{cls.RESET}"
    
    @classmethod
    def rule_number(cls, number):
        """Format rule number for display"""
        return f"{cls.HIGHLIGHT}#{number}{cls.RESET}"
    
    @classmethod
    def percentage(cls, value, total=100):
        """Format percentage with appropriate color"""
        percent = (value / total) * 100 if total > 0 else 0
        if percent >= 80:
            return cls.success(f"{percent:.1f}%")
        elif percent >= 60:
            return cls.warning(f"{percent:.1f}%")
        else:
            return cls.error(f"{percent:.1f}%")


def print_banner():
    """Print the application banner with ASCII art"""
    banner = f"""
{Colors.HEADER}    ╔══════════════════════════════════════════════════════════╗
    ║                                                          ║
    ║        🔥 AI-Powered Firewall Rule Optimizer 🔥         ║
    ║                                                          ║
    ║     Analyze • Optimize • Visualize • Secure            ║
    ║                                                          ║
    ╚══════════════════════════════════════════════════════════╝{Colors.RESET}
"""
    print(banner)


def print_separator(title="", char="─", width=60):
    """Print a decorative separator line"""
    if title:
        padding = (width - len(title) - 2) // 2
        separator = f"{char * padding} {Colors.header(title)} {char * padding}"
        if len(separator.replace(Colors.HEADER, '').replace(Colors.RESET, '')) < width:
            separator += char
    else:
        separator = char * width
    
    print(f"{Colors.INFO}{separator}{Colors.RESET}")


def get_priority_color(priority):
    """Get color for priority level"""
    priority_colors = {
        'CRITICAL': Colors.critical,
        'HIGH': Colors.high, 
        'MEDIUM': Colors.medium,
        'LOW': Colors.low
    }
    return priority_colors.get(priority.upper(), Colors.info)


def get_severity_emoji(severity):
    """Get emoji for severity level"""
    severity_emojis = {
        'CRITICAL': '🔥',
        'HIGH': '🚨', 
        'MEDIUM': '⚠️',
        'LOW': '💡'
    }
    return severity_emojis.get(severity.upper(), 'ℹ️')


def format_progress_bar(value, total, width=30, show_percentage=True):
    """Create a colored progress bar"""
    if total == 0:
        filled = 0
        percentage = 0
    else:
        filled = int((value / total) * width)
        percentage = (value / total) * 100
    
    bar = (Colors.PROGRESS_FILL * filled) + (Colors.PROGRESS_EMPTY * (width - filled))
    
    if show_percentage:
        return f"{bar} {Colors.percentage(value, total)}"
    else:
        return bar


# Color palette for visualizations (hex colors)
VISUALIZATION_COLORS = {
    'critical': '#FF4444',
    'high': '#FF6B35', 
    'medium': '#F7931E',
    'low': '#4CAF50',
    'accept': '#4CAF50',
    'drop': '#F44336',
    'reject': '#FF9800',
    'log': '#2196F3',
    'chain': '#9C27B0',
    'default': '#607D8B'
}
