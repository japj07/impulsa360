import base64
from pathlib import Path
import streamlit as st
import streamlit.components.v1 as components

# =========================
# CONFIG
# =========================
PHOTO_FOLDER = Path("photos")
LOGO_RIGHT_PATH = Path("assets/logo_farmaenlace.png")
LOGO_LEFT_PATH = Path("assets/logo_galeria.png")
BACKGROUND_PATH = Path("assets/background.jpg")

st.set_page_config(
    page_title="Galería de la expedición",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================
# HELPERS
# =========================
def img_to_base64(path: Path) -> str:
    if not path.exists():
        return ""
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

def get_images(folder: Path):
    valid_ext = {".jpg", ".jpeg", ".png", ".webp"}
    if not folder.exists():
        return []
    return sorted(
        [f for f in folder.iterdir() if f.is_file() and f.suffix.lower() in valid_ext],
        key=lambda x: x.name.lower()
    )

def mime_from_suffix(path: Path) -> str:
    ext = path.suffix.lower()
    if ext == ".png":
        return "png"
    if ext == ".webp":
        return "webp"
    return "jpeg"

def build_header_html(left_logo_b64: str, right_logo_b64: str) -> str:
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="utf-8">
    <style>
        html, body {{
            margin: 0;
            padding: 0;
            background: transparent;
            overflow: hidden;
            font-family: Arial, sans-serif;
        }}

        .header-wrap {{
            width: 100%;
            max-width: 1320px;
            margin: 0 auto;
            box-sizing: border-box;
        }}

        .header-box {{
            width: 100%;
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 24px;

            background: rgba(255,255,255,0.42);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);

            border: 1px solid rgba(255,255,255,0.18);
            border-radius: 28px;
            padding: 20px 28px;
            box-sizing: border-box;
        }}

        .header-left {{
            display: flex;
            align-items: center;
            gap: 22px;
            min-width: 0;
        }}

        .left-logo {{
            width: 95px;
            height: auto;
            display: block;
            flex-shrink: 0;
        }}

        .right-logo {{
            width: 220px;
            height: auto;
            display: block;
            flex-shrink: 0;
        }}

        .title {{
            font-size: 44px;
            font-weight: 800;
            line-height: 1.05;
            color: #20263a;
            white-space: nowrap;
        }}

        @media (max-width: 1100px) {{
            .title {{
                font-size: 34px;
                white-space: normal;
            }}

            .right-logo {{
                width: 180px;
            }}
        }}
    </style>
    </head>
    <body>
        <div class="header-wrap">
            <div class="header-box">
                <div class="header-left">
                    <img class="left-logo" src="data:image/png;base64,{left_logo_b64}" alt="Logo galería">
                    <div class="title">Galería de la expedición</div>
                </div>
                <img class="right-logo" src="data:image/png;base64,{right_logo_b64}" alt="Logo Farmaenlace">
            </div>
        </div>
    </body>
    </html>
    """

def build_carousel_html(image_paths, autoplay_ms: int = 3500) -> str:
    slides_html = []
    dots_html = []

    for i, img_path in enumerate(image_paths):
        img_b64 = img_to_base64(img_path)
        mime = mime_from_suffix(img_path)
        active = "active" if i == 0 else ""
        slides_html.append(
            f'''
            <div class="carousel-slide {active}">
                <img src="data:image/{mime};base64,{img_b64}" alt="slide-{i}">
            </div>
            '''
        )
        dots_html.append(
            f'<span class="carousel-dot {"active" if i == 0 else ""}" data-index="{i}"></span>'
        )

    slides_str = "\n".join(slides_html)
    dots_str = "\n".join(dots_html)

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="utf-8">
    <style>
        html, body {{
            margin: 0;
            padding: 0;
            background: transparent;
            overflow: hidden;
        }}

        .carousel-shell {{
            width: 100%;
            max-width: 1320px;
            margin: 0 auto;
            box-sizing: border-box;
        }}

        .carousel-frame {{
            width: 100%;
            background: rgba(255,255,255,0.42);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.18);
            border-radius: 28px;
            padding: 16px;
            box-sizing: border-box;
        }}

        .carousel-container {{
            position: relative;
            width: 100%;
            height: 700px;
            overflow: hidden;
            border-radius: 22px;
            background: transparent;
        }}

        .carousel-slide {{
            position: absolute;
            inset: 0;
            opacity: 0;
            transition: opacity 0.65s ease;
            pointer-events: none;
        }}

        .carousel-slide.active {{
            opacity: 1;
            pointer-events: auto;
        }}

        .carousel-slide img {{
            width: 100%;
            height: 100%;
            object-fit: contain;
            display: block;
        }}

        .carousel-btn {{
            position: absolute;
            top: 50%;
            transform: translateY(-50%);
            width: 58px;
            height: 58px;
            border-radius: 50%;
            border: none;
            cursor: pointer;
            font-size: 28px;
            color: white;
            background: rgba(0,0,0,0.22);
            z-index: 10;
        }}

        .carousel-btn.prev {{
            left: 20px;
        }}

        .carousel-btn.next {{
            right: 20px;
        }}

        .carousel-dots {{
            position: absolute;
            bottom: 18px;
            left: 50%;
            transform: translateX(-50%);
            display: flex;
            gap: 10px;
            z-index: 11;
        }}

        .carousel-dot {{
            width: 10px;
            height: 10px;
            border-radius: 50%;
            background: rgba(255,255,255,0.45);
            cursor: pointer;
        }}

        .carousel-dot.active {{
            background: white;
        }}

        @media (max-width: 1100px) {{
            .carousel-container {{
                height: 560px;
            }}
        }}
    </style>
    </head>
    <body>
        <div class="carousel-shell">
            <div class="carousel-frame">
                <div class="carousel-container">
                    {slides_str}

                    <button class="carousel-btn prev" id="prevBtn">&#10094;</button>
                    <button class="carousel-btn next" id="nextBtn">&#10095;</button>

                    <div class="carousel-dots">
                        {dots_str}
                    </div>
                </div>
            </div>
        </div>

        <script>
            const slides = document.querySelectorAll(".carousel-slide");
            const dots = document.querySelectorAll(".carousel-dot");
            const prevBtn = document.getElementById("prevBtn");
            const nextBtn = document.getElementById("nextBtn");

            let current = 0;
            let autoplay = null;

            function showSlide(index) {{
                slides.forEach((slide, i) => {{
                    slide.classList.toggle("active", i === index);
                }});
                dots.forEach((dot, i) => {{
                    dot.classList.toggle("active", i === index);
                }});
                current = index;
            }}

            function nextSlide() {{
                showSlide((current + 1) % slides.length);
            }}

            function prevSlide() {{
                showSlide((current - 1 + slides.length) % slides.length);
            }}

            function restartAutoplay() {{
                if (autoplay) clearInterval(autoplay);
                autoplay = setInterval(nextSlide, {autoplay_ms});
            }}

            nextBtn.onclick = () => {{
                nextSlide();
                restartAutoplay();
            }};

            prevBtn.onclick = () => {{
                prevSlide();
                restartAutoplay();
            }};

            dots.forEach(dot => {{
                dot.onclick = () => {{
                    showSlide(Number(dot.dataset.index));
                    restartAutoplay();
                }};
            }});

            restartAutoplay();
        </script>
    </body>
    </html>
    """

# =========================
# LOAD ASSETS
# =========================
logo_right_b64 = img_to_base64(LOGO_RIGHT_PATH)
logo_left_b64 = img_to_base64(LOGO_LEFT_PATH)
bg_b64 = img_to_base64(BACKGROUND_PATH)
gallery_images = get_images(PHOTO_FOLDER)

# =========================
# PAGE CSS
# =========================
st.markdown(
    f"""
    <style>
    .stApp {{
        background: transparent;
    }}

    .stApp::before {{
        content: "";
        position: fixed;
        inset: 0;
        background: url("data:image/jpg;base64,{bg_b64}") center center / cover no-repeat;
        filter: blur(6px);
        transform: scale(1.03);
        opacity: 0.62;
        z-index: -2;
    }}

    .stApp::after {{
        content: "";
        position: fixed;
        inset: 0;
        background: rgba(255,255,255,0.05);
        z-index: -1;
    }}

    [data-testid="stHeader"] {{
        background: transparent;
    }}

    .block-container {{
        max-width: 1450px;
        padding-top: 2rem;
        padding-bottom: 1rem;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# =========================
# HEADER
# =========================
header_html = build_header_html(logo_left_b64, logo_right_b64)
components.html(header_html, height=120, scrolling=False)

# =========================
# CAROUSEL
# =========================
if gallery_images:
    carousel_html = build_carousel_html(gallery_images, autoplay_ms=3500)
    components.html(carousel_html, height=760, scrolling=False)
else:
    st.warning("No hay imágenes en la carpeta photos.")