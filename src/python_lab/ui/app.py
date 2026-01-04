import flet as ft
import asyncio


async def main(page: ft.Page) -> None:
    page.title = "Carrusel con dots clickeables"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    images = [
        "https://picsum.photos/400/250?1",
        "https://picsum.photos/400/250?2",
        "https://picsum.photos/400/250?3",
    ]

    index = 0

    # Imagen
    image = ft.Image(
        src=images[index],
        fit=ft.BoxFit.COVER,
        width=400,
        height=250,
        border_radius=12,
    )

    # Contenedor con fade
    container = ft.Container(
        content=image,
        opacity=1.0,
        animate_opacity=300,
    )

    # Dots
    dots = ft.Row(alignment=ft.MainAxisAlignment.CENTER)

    async def fade_to(new_index: int):
        nonlocal index

        if new_index == index:
            return

        container.opacity = 0.0
        page.update()
        await asyncio.sleep(0.3)

        index = new_index
        image.src = images[index]

        container.opacity = 1.0
        build_dots()
        page.update()

    def build_dots():
        dots.controls.clear()
        for i in range(len(images)):
            dots.controls.append(
                ft.Container(
                    width=12 if i == index else 10,
                    height=12 if i == index else 10,
                    border_radius=10,
                    bgcolor=ft.Colors.BLUE if i == index else ft.Colors.GREY_400,
                    animate_scale=200,
                    on_click=lambda e, idx=i: asyncio.create_task(fade_to(idx)),
                )
            )

    build_dots()

    async def autoplay():
        while True:
            await asyncio.sleep(3)
            await fade_to((index + 1) % len(images))

    asyncio.create_task(autoplay())

    page.add(
        ft.Column(
            controls=[
                # Imagen centrada
                ft.Row(
                    controls=[container],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                # Flechas
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
                # Dots clickeables
                dots,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10,
        )
    )


ft.app(target=main)
