import flet as ft
import asyncio


async def main(page: ft.Page) -> None:
    page.title = "Carrusel con fade (compatible)"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    images = [
        "https://picsum.photos/400/250?1",
        "https://picsum.photos/400/250?2",
        "https://picsum.photos/400/250?3",
    ]

    index = 0

    image = ft.Image(
        src=images[index],
        fit=ft.BoxFit.COVER,
        width=400,
        height=250,
        border_radius=12,
    )

    container = ft.Container(
        content=image,
        opacity=1.0,
        animate_opacity=300,  # 👈 animación real
    )

    async def fade_to(new_index: int):
        nonlocal index

        container.opacity = 0.0
        page.update()
        await asyncio.sleep(0.3)

        index = new_index
        image.src = images[index]

        container.opacity = 1.0
        page.update()

    async def autoplay():
        while True:
            await asyncio.sleep(3)
            await fade_to((index + 1) % len(images))

    asyncio.create_task(autoplay())

    page.add(
        ft.Column(
            controls=[
                container,
                ft.Row(
                    controls=[
                        ft.IconButton(
                            icon=ft.Icons.KEYBOARD_ARROW_LEFT,
                            on_click=lambda e: asyncio.create_task(
                                fade_to((index - 1) % len(images))
                            ),
                        ),
                        ft.IconButton(
                            icon=ft.Icons.KEYBOARD_ARROW_RIGHT,
                            on_click=lambda e: asyncio.create_task(
                                fade_to((index + 1) % len(images))
                            ),
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
    )


ft.app(target=main)
