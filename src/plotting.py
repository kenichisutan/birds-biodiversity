import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os


def setup_plotting_style():
    """
    Configure global matplotlib and seaborn style settings.
    Call this once at the beginning of each notebook.
    """
    plt.style.use('seaborn-v0_8-darkgrid')
    sns.set_palette("husl")
    
    # Professional styling
    plt.rcParams['figure.dpi'] = 100
    plt.rcParams['savefig.dpi'] = 300
    plt.rcParams['savefig.bbox'] = 'tight'
    plt.rcParams['font.size'] = 11
    plt.rcParams['axes.labelsize'] = 12
    plt.rcParams['axes.titlesize'] = 14
    plt.rcParams['legend.fontsize'] = 10

# Colour palette
COLORS = {
    'primary': '#2E86AB',
    'secondary': '#A23B72',
    'accent': '#F18F01',
    'success': '#06A77D',
    'warning': '#D62246',
}

def plot_bar_chart(x, y, xlabel='', ylabel='', title='', filename=None, 
                   color=None, highlight_indices=None, highlight_color=None,
                   highlight_labels=None, horizontal=False):
    """
    Create a bar chart with optional highlighting for specific bars.
    
    Parameters
    ----------
    x : array-like
        X-axis values (categories)
    y : array-like
        Y-axis values (heights)
    xlabel, ylabel, title : str
        Axis labels and title
    filename : str, optional
        Path to save figure
    color : str, optional
        Bar color (default: primary color)
    highlight_indices : list, optional
        Indices of bars to highlight differently
    highlight_color : str, optional
        Color for highlighted bars
    highlight_labels : list, optional
        Labels to add on highlighted bars
    horizontal : bool
        If True, create horizontal bar chart
    """
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Prepare colors
    if color is None:
        color = COLORS['primary']
    
    # Create color array for each bar
    if highlight_indices is not None and highlight_color is not None:
        colors = [highlight_color if i in highlight_indices else color 
                  for i in range(len(x))]
    else:
        colors = color
    
    # Plot
    if horizontal:
        ax.barh(x, y, color=colors, edgecolor='black', alpha=0.8)
    else:
        ax.bar(x, y, color=colors, edgecolor='black', alpha=0.8)
    
    # Add labels on highlighted bars
    if highlight_labels is not None and highlight_indices is not None:
        for idx, label in zip(highlight_indices, highlight_labels):
            if horizontal:
                ax.text(y[idx] + max(y)*0.02, idx, label, 
                       ha='left', va='center', fontsize=9, 
                       color='darkred', fontweight='bold')
            else:
                ax.text(idx, y[idx] + max(y)*0.02, label, 
                       ha='center', va='bottom', fontsize=9, 
                       color='darkred', fontweight='bold')
    
    # Styling
    ax.set_xlabel(xlabel, fontweight='bold', fontsize=12)
    ax.set_ylabel(ylabel, fontweight='bold', fontsize=12)
    ax.set_title(title, fontweight='bold', fontsize=14)
    ax.grid(axis='y' if not horizontal else 'x', alpha=0.3)
    
    plt.tight_layout()
    
    if filename:
        # Support Path-like objects and guard empty parent
        filename_str = os.fspath(filename)
        parent = os.path.dirname(filename_str)
        if parent:
            os.makedirs(parent, exist_ok=True)

        # Use Agg writer for PNG to avoid Pillow _idat/fileno issues
        if filename_str.lower().endswith('.png'):
            from matplotlib.backends.backend_agg import FigureCanvasAgg
            canvas = FigureCanvasAgg(fig)
            canvas.print_png(filename_str)
        else:
            # Let matplotlib infer format for non-PNG
            fig.savefig(filename_str, dpi=300, bbox_inches='tight')
        print(f"✓ Saved: {filename_str}")
    
    return fig, ax


def plot_line_chart(x, y, xlabel='', ylabel='', title='', filename=None,
                   color=None, marker='o', highlight_points=None,
                   highlight_color=None, highlight_labels=None):
    """
    Create a line chart with optional point highlighting.
    
    Parameters
    ----------
    x : array-like
        X-axis values
    y : array-like
        Y-axis values
    xlabel, ylabel, title : str
        Axis labels and title
    filename : str, optional
        Path to save figure
    color : str, optional
        Line color (default: success color)
    marker : str
        Marker style
    highlight_points : list, optional
        X-values of points to highlight
    highlight_color : str, optional
        Color for highlighted points
    highlight_labels : list, optional
        Labels for highlighted points
    """
    fig, ax = plt.subplots(figsize=(12, 6))
    
    if color is None:
        color = COLORS['success']
    
    # Plot line
    ax.plot(x, y, marker=marker, linewidth=2, color=color, markersize=8)
    
    # Highlight specific points
    if highlight_points is not None and highlight_color is not None:
        for point in highlight_points:
            if point in x:
                idx = list(x).index(point)
                ax.scatter([point], [y[idx]], color=highlight_color, 
                          s=100, zorder=3, edgecolor='black', linewidth=1.5)
    
    # Add labels
    if highlight_labels is not None and highlight_points is not None:
        for point, label in zip(highlight_points, highlight_labels):
            if point in x:
                idx = list(x).index(point)
                ax.text(point, y[idx] + max(y)*0.03, label, 
                       ha='center', fontsize=9, color='darkred', fontweight='bold')
    
    # Styling
    ax.set_xlabel(xlabel, fontweight='bold', fontsize=12)
    ax.set_ylabel(ylabel, fontweight='bold', fontsize=12)
    ax.set_title(title, fontweight='bold', fontsize=14)
    ax.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    
    if filename:
        filename_str = os.fspath(filename)
        parent = os.path.dirname(filename_str)
        if parent:
            os.makedirs(parent, exist_ok=True)

        if filename_str.lower().endswith('.png'):
            from matplotlib.backends.backend_agg import FigureCanvasAgg
            canvas = FigureCanvasAgg(fig)
            canvas.print_png(filename_str)
        else:
            fig.savefig(filename_str, dpi=300, bbox_inches='tight')
        print(f"✓ Saved: {filename_str}")
    
    return fig, ax


def plot_dual_bars(data1, data2, labels1, labels2, 
                  title1='', title2='', xlabel1='', xlabel2='',
                  color1=None, color2=None, filename=None):
    """
    Create side-by-side horizontal bar charts.
    Used for comparing two related metrics (e.g., observer counts vs spatial coverage).
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    if color1 is None:
        color1 = COLORS['primary']
    if color2 is None:
        color2 = COLORS['accent']
    
    # Left plot
    ax1.barh(labels1, data1, color=color1, edgecolor='black', alpha=0.8)
    ax1.set_xlabel(xlabel1, fontweight='bold', fontsize=12)
    ax1.set_title(title1, fontweight='bold', fontsize=14)
    ax1.grid(axis='x', alpha=0.3)
    
    # Right plot
    ax2.barh(labels2, data2, color=color2, edgecolor='black', alpha=0.8)
    ax2.set_xlabel(xlabel2, fontweight='bold', fontsize=12)
    ax2.set_title(title2, fontweight='bold', fontsize=14)
    ax2.grid(axis='x', alpha=0.3)
    
    plt.tight_layout()
    
    if filename:
        filename_str = os.fspath(filename)
        parent = os.path.dirname(filename_str)
        if parent:
            os.makedirs(parent, exist_ok=True)

        if filename_str.lower().endswith('.png'):
            from matplotlib.backends.backend_agg import FigureCanvasAgg
            canvas = FigureCanvasAgg(fig)
            canvas.print_png(filename_str)
        else:
            fig.savefig(filename_str, dpi=300, bbox_inches='tight')
        print(f"✓ Saved: {filename_str}")
    
    return fig, (ax1, ax2)
    
# Temporal trend plot
def plot_temporal_trend(years, values, ci_lower=None, ci_upper=None,
                       ylabel='', title='', filename=None, 
                       trend_line=None, show_points=True):
    """
    Plot temporal trend with confidence intervals and optional trend line.
    Used in both indicator analysis (Task 2) and species analysis (Task 3).
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Plot data
    if show_points:
        ax.plot(years, values, 'o-', linewidth=2, markersize=8, 
               label='Observed', color=COLORS['primary'], zorder=3)
    else:
        ax.plot(years, values, '-', linewidth=2, 
               label='Observed', color=COLORS['primary'], zorder=3)
    
    # Confidence interval
    if ci_lower is not None and ci_upper is not None:
        ax.fill_between(years, ci_lower, ci_upper, 
                       alpha=0.3, color=COLORS['primary'], 
                       label='95% CI', zorder=2)
    
    # Trend line
    if trend_line is not None:
        ax.plot(trend_line['x'], trend_line['y'], '--', 
               color=COLORS['warning'], linewidth=2.5, 
               label='Trend', zorder=4)
    
    # Styling
    ax.set_xlabel('Year', fontsize=12, fontweight='bold')
    ax.set_ylabel(ylabel, fontsize=12, fontweight='bold')
    ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
    ax.legend(frameon=True, loc='best', shadow=True)
    ax.grid(True, alpha=0.3, zorder=1)
    
    plt.tight_layout()
    
    if filename:
        filename_str = os.fspath(filename)
        parent = os.path.dirname(filename_str)
        if parent:
            os.makedirs(parent, exist_ok=True)

        if filename_str.lower().endswith('.png'):
            from matplotlib.backends.backend_agg import FigureCanvasAgg
            canvas = FigureCanvasAgg(fig)
            canvas.print_png(filename_str)
        else:
            fig.savefig(filename_str, dpi=300, bbox_inches='tight')
        print(f"✓ Saved: {filename_str}")
    
    return fig, ax

# Model diagnostics
def plot_diagnostics(residuals, fitted, title='Model Diagnostics', filename=None):
    """
    Create diagnostic plots for regression models.
    Used when checking model assumptions in Tasks 2 & 3.
    """
    from scipy import stats as scipy_stats
    
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    # 1. Residuals vs Fitted
    axes[0, 0].scatter(fitted, residuals, alpha=0.6, color=COLORS['primary'])
    axes[0, 0].axhline(y=0, color=COLORS['warning'], linestyle='--', linewidth=2)
    axes[0, 0].set_xlabel('Fitted values', fontweight='bold')
    axes[0, 0].set_ylabel('Residuals', fontweight='bold')
    axes[0, 0].set_title('Residuals vs Fitted', fontweight='bold')
    axes[0, 0].grid(True, alpha=0.3)
    
    # 2. Q-Q plot
    scipy_stats.probplot(residuals, dist="norm", plot=axes[0, 1])
    axes[0, 1].set_title('Normal Q-Q Plot', fontweight='bold')
    axes[0, 1].grid(True, alpha=0.3)
    
    # 3. Scale-Location
    std_resid = residuals / np.std(residuals)
    axes[1, 0].scatter(fitted, np.sqrt(np.abs(std_resid)), 
                      alpha=0.6, color=COLORS['primary'])
    axes[1, 0].set_xlabel('Fitted values', fontweight='bold')
    axes[1, 0].set_ylabel('√|Standardized residuals|', fontweight='bold')
    axes[1, 0].set_title('Scale-Location', fontweight='bold')
    axes[1, 0].grid(True, alpha=0.3)
    
    # 4. Residuals histogram
    axes[1, 1].hist(residuals, bins=15, edgecolor='black', 
                   alpha=0.7, color=COLORS['primary'])
    axes[1, 1].set_xlabel('Residuals', fontweight='bold')
    axes[1, 1].set_ylabel('Frequency', fontweight='bold')
    axes[1, 1].set_title('Residuals Distribution', fontweight='bold')
    axes[1, 1].grid(True, alpha=0.3)
    
    fig.suptitle(title, fontsize=14, fontweight='bold', y=1.00)
    plt.tight_layout()
    
    if filename:
        filename_str = os.fspath(filename)
        parent = os.path.dirname(filename_str)
        if parent:
            os.makedirs(parent, exist_ok=True)

        if filename_str.lower().endswith('.png'):
            from matplotlib.backends.backend_agg import FigureCanvasAgg
            canvas = FigureCanvasAgg(fig)
            canvas.print_png(filename_str)
        else:
            fig.savefig(filename_str, dpi=300, bbox_inches='tight')
        print(f"✓ Saved: {filename_str}")
    
    return fig, axes
