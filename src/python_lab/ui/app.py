import flet as ft
import asyncio
import time


async def main(page: ft.Page) -> None:
    page.title = "Carrusel profesional"
    page.bgcolor = ft.Colors.GREY_100
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    images = [
        "https://picsum.photos/400/250?1",
        "https://picsum.photos/400/250?2",
        "https://picsum.photos/400/250?3",
    ]

    index = 0
    autoplay_enabled = True
    last_interaction = time.time()

    # Imagen
    image = ft.Image(
        src=images[index],
        fit=ft.BoxFit.COVER,
        width=400,
        height=250,
        border_radius=12,
    )

    # Tarjeta con sombra + fade
    container = ft.Container(
        content=image,
        opacity=1.0,
        animate_opacity=300,
        padding=6,
        bgcolor=ft.Colors.WHITE,
        border_radius=16,
        shadow=ft.BoxShadow(
            blur_radius=15,
            color=ft.Colors.BLACK12,
            offset=ft.Offset(0, 6),
        ),
    )

    dots = ft.Row(alignment=ft.MainAxisAlignment.CENTER)

    def register_interaction():
        nonlocal autoplay_enabled, last_interaction
        autoplay_enabled = False
        last_interaction = time.time()

    def build_dots():
        dots.controls.clear()
        for i in range(len(images)):
            dots.controls.append(
                ft.Container(
                    width=12 if i == index else 10,
                    height=12 if i == index else 10,
                    border_radius=10,
                    bgcolor=ft.Colors.BLUE if i == index else ft.Colors.GREY_400,
                    on_click=lambda e, idx=i: asyncio.create_task(fade_to(idx, True)),
                )
            )

    async def fade_to(new_index: int, user_action: bool = False):
        nonlocal index
        if new_index == index:
            return

        if user_action:
            register_interaction()

        container.opacity = 0.0
        page.update()
        await asyncio.sleep(0.3)

        index = new_index
        image.src = images[index]

        container.opacity = 1.0
        build_dots()
        page.update()

    build_dots()

    async def autoplay():
        nonlocal autoplay_enabled
        while True:
            await asyncio.sleep(1)

            # Reactivar autoplay tras 5s sin interacción
            if not autoplay_enabled and time.time() - last_interaction > 5:
                autoplay_enabled = True

            if autoplay_enabled:
                await fade_to((index + 1) % len(images))

                await asyncio.sleep(2)

    asyncio.create_task(autoplay())

    page.add(
        ft.Column(
            controls=[
                ft.Row(
                    controls=[container],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Row(
                    controls=[
                        ft.IconButton(
                            icon=ft.Icons.KEYBOARD_ARROW_LEFT,
                            on_click=lambda e: asyncio.create_task(
                                fade_to((index - 1) % len(images), True)
                            ),
                        ),
                        ft.IconButton(
                            icon=ft.Icons.KEYBOARD_ARROW_RIGHT,
                            on_click=lambda e: asyncio.create_task(
                                fade_to((index + 1) % len(images), True)
                            ),
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                dots,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=14,
        )
    )


ft.app(target=main)
