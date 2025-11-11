import flet as ft
import flet_video as fv

def before_main(page: ft.Page):
    page.title = "Flet Video Example"

def main(page: ft.Page):
    video_player = fv.Video(
        expand=True,
        playlist=[
            fv.VideoMedia(
                "https://storage.googleapis.com/gtv-videos-bucket/sample/ForBiggerFun.mp4"
            )
        ],
        autoplay=False
    )

    page.add(
        video_player,
        ft.Button("Play/Pause", on_click=lambda _: video_player.play_or_pause())
    )

ft.run(main=main, before_main=before_main)