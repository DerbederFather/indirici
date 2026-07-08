%%writefile main.py
import flet as ft
import yt_dlp
import os

def main(page: ft.Page):
    page.title = "Yusuf YILMAZ - Mobil İndirici"
    page.theme_mode = ft.ThemeMode.DARK
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.AUTO

    format_secimi = "MP3 (Ses)"
    cozunurluk_secimi = "En Yüksek"

    ust_tasarim = ft.Container(
        content=ft.Column([
            ft.Text("Yusuf YILMAZ", size=24, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_400),
            ft.Text("Advanced Mobile Downloader 2026©", size=12, color=ft.colors.GREY_500),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        margin=ft.margin.only(top=20, bottom=20)
    )

    url_input = ft.TextField(label="YouTube veya YT Music Linki", placeholder="https://...", width=340)
    sanatci_input = ft.TextField(label="Meta Veri - Sanatçı (Ebru Gündeş)", width=340)
    sarki_input = ft.TextField(label="Meta Veri - Şarkı Adı (Ne olsa dinlenir)", width=340)
    durum_text = ft.Text("Durum: Hazır", size=14, color=ft.colors.GREY_400)

    cozunurluk_dropdown = ft.Dropdown(
        label="Çözünürlük", width=340, visible=False,
        options=[ft.dropdown.Option("En Yüksek"), ft.dropdown.Option("1080p"), ft.dropdown.Option("720p"), ft.dropdown.Option("480p")],
        value="En Yüksek"
    )

    def format_ayarla(e):
        nonlocal format_secimi
        format_secimi = format_dropdown.value
        cozunurluk_dropdown.visible = (format_secimi == "MP4 (Video)")
        page.update()

    format_dropdown = ft.Dropdown(
        label="Format", width=340,
        options=[ft.dropdown.Option("MP3 (Ses)"), ft.dropdown.Option("MP4 (Video)")],
        value="MP3 (Ses)", on_change=format_ayarla
    )

    def indir_buton_click(e):
        url = url_input.value.strip()
        sanatci = sanatci_input.value.strip()
        sarki = sarki_input.value.strip()
        
        if not url or not sarki:
            durum_text.value = "Durum: Hata! Link ve Şarkı ismi boş olamaz."
            durum_text.color = ft.colors.RED_400
            page.update()
            return

        durum_text.value = "Durum: İndirme işlemi başladı..."
        durum_text.color = ft.colors.ORANGE_400
        page.update()

        klasor = "/storage/emulated/0/Download" if os.name != 'nt' else "."
        dosya_adi = f"{sanatci} - {sarki}" if sanatci else sarki
        dosya_adi_temiz = "".join(c for c in dosya_adi if c not in r'\/:*?"<>|')
        cikis_yolu = os.path.join(klasor, f"{dosya_adi_temiz}.%(ext)s")

        if format_secimi == "MP3 (Ses)":
            ydl_opts = {
                'format': 'bestaudio/best', 'outtmpl': cikis_yolu,
                'postprocessors': [
                    {'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '320'},
                    {'key': 'FFmpegMetadata', 'add_metadata': True}
                ],
            }
        else:
            ydl_opts = {'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best', 'outtmpl': cikis_yolu, 'merge_output_format': 'mp4'}

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            durum_text.value = f"Durum: Başarıyla Telefonun 'Download' Klasörüne İndirildi!"
            durum_text.color = ft.colors.GREEN_400
        except Exception as ex:
            durum_text.value = f"Durum: Hata! {str(ex)[:30]}..."
            durum_text.color = ft.colors.RED_400
        page.update()

    indir_butonu = ft.ElevatedButton(text="İNDİRMEYİ BAŞLAT", width=200, height=50, color=ft.colors.WHITE, bgcolor=ft.colors.BLUE_700, on_click=indir_buton_click)

    page.add(ust_tasarim, url_input, ft.Divider(height=10, color=ft.colors.TRANSPARENT), sanatci_input, sarki_input, ft.Divider(height=10, color=ft.colors.TRANSPARENT), format_dropdown, cozunurluk_dropdown, ft.Divider(height=20, color=ft.colors.TRANSPARENT), indir_butonu, ft.Divider(height=15, color=ft.colors.TRANSPARENT), durum_text)

if __name__ == "__main__":
    ft.app(target=main)