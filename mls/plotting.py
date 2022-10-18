import imageio
from typing import List
from pathlib import Path
from plotly.graph_objects import Figure

IMAGE_WIDTH, IMAGE_HEIGHT = 900, 400
SCALE = 2


def clean_fig(fig: Figure) -> Figure:
    fig.update_layout(
        width=IMAGE_WIDTH, height=IMAGE_HEIGHT,
        plot_bgcolor='#FFF', title={'x': .5}, 
        font_family='Arial', title_font_family="Arial"
    )
    fig.update_coloraxes(showscale=False)
    return fig

def add_culmen_axes(fig: Figure) -> Figure:
    fig.update_yaxes(title='Culmen Depth (mm)', range=[12, 22.5], dtick=2.5)
    fig.update_xaxes(title='Culmen Length (mm)')
    return clean_fig(fig)

def write_image(fig: Figure, image_path: str, width=IMAGE_WIDTH, height=IMAGE_HEIGHT, scale=SCALE):
    fig.write_image(image_path, width=width, height=height, scale=scale)

def write_gif(
    figures: List[Figure], 
    gif_name: str, 
    folder: str, 
    time_per_frame: float=.5, 
    delay_start=2, delay_end=None,
    width=IMAGE_WIDTH, height=IMAGE_HEIGHT,
    scale=SCALE,
    ):
    folder = Path(folder)
    folder.mkdir(exist_ok=True)
    image_paths = []
    if delay_start:
        figures = [figures[0]] * delay_start + figures[1:]
    if delay_end:
        figures = figures[:-1] + [figures[-1]] * delay_end
    for i, f in enumerate(figures):
        image_path = folder / f'{gif_name}--{i}.png'
        image_paths.append(image_path)
        write_image(f, image_path, width=width, height=height, scale=scale)

    imageio.mimsave(
        f'{folder}/{gif_name}.gif', 
        [imageio.imread_v2(x) for x in image_paths], 
        duration=time_per_frame
    )
    for im in image_paths:
        im.unlink()