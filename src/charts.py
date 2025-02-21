import matplotlib.pyplot as plt
import matplotlib.dates as mdates 

def line_chart(x, y, **options):
    fig, ax = plt.subplots(figsize=(10, 5))

    ax.plot(x, y, linewidth=2, color="#f39c12")  

    ax.xaxis.set_major_formatter(mdates.DateFormatter("%d %b %H:%M"))
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())

    ax.set(
        title=options.get("title"),
        xlabel=options.get("xlabel"),
        ylabel=options.get("ylabel"),
    )

    ax.tick_params(axis="x", rotation=45, colors="white")  
    ax.tick_params(axis="y", colors="white")
    ax.set_facecolor("#0e1117")  
    fig.patch.set_facecolor("#0e1117")  

    ax.title.set_color("white")
    ax.xaxis.label.set_color("white")
    ax.yaxis.label.set_color("white")

    fig.tight_layout()
    return fig
