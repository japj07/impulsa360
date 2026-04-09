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

def build_carousel_html(image_paths, autoplay_ms: int = 3500) -> str:
    slides_html = []
    dots_html = []
    modal_thumbs_html = []

    for i, img_path in enumerate(image_paths):
        img_b64 = img_to_base64(img_path)
        mime = mime_from_suffix(img_path)
        active = "active" if i == 0 else ""

        slides_html.append(
            f'''
            <div class="carousel-slide {active}" data-index="{i}">
                <img src="data:image/{mime};base64,{img_b64}" alt="slide-{i}">
            </div>
            '''
        )

        dots_html.append(
            f'<span class="carousel-dot {"active" if i == 0 else ""}" data-index="{i}"></span>'
        )

        modal_thumbs_html.append(
            f'''
            <div class="modal-thumb {"active" if i == 0 else ""}" data-index="{i}">
                <img src="data:image/{mime};base64,{img_b64}" alt="modal-thumb-{i}">
            </div>
            '''
        )

    slides_str = "\n".join(slides_html)
    dots_str = "\n".join(dots_html)
    modal_thumbs_str = "\n".join(modal_thumbs_html)

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="utf-8">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Source+Sans+3:wght@600;700;800&display=swap');

        html, body {{
            margin: 0;
            padding: 0;
            background: transparent;
            overflow: hidden;
            font-family: "Source Sans 3", Arial, sans-serif;
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
            overflow: hidden;
            padding: 16px;
            box-sizing: border-box;
            box-shadow: 0 8px 24px rgba(0,0,0,0.08);
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
            cursor: zoom-in;
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

        .modal {{
            display: none;
            position: fixed;
            inset: 0;
            background: rgba(12,16,28,0.88);
            z-index: 9999;
            padding: 28px;
            box-sizing: border-box;
        }}

        .modal.open {{
            display: flex;
            align-items: center;
            justify-content: center;
        }}

        .modal-content {{
            width: min(1200px, 95vw);
            height: min(90vh, 900px);
            display: flex;
            flex-direction: column;
            gap: 16px;
        }}

        .modal-main {{
            position: relative;
            flex: 1;
            border-radius: 22px;
            overflow: hidden;
            background: rgba(255,255,255,0.06);
        }}

        .modal-main img {{
            width: 100%;
            height: 100%;
            object-fit: contain;
            display: block;
        }}

        .modal-close {{
            position: absolute;
            top: 18px;
            right: 18px;
            width: 44px;
            height: 44px;
            border-radius: 50%;
            border: none;
            font-size: 24px;
            color: white;
            background: rgba(0,0,0,0.28);
            cursor: pointer;
            z-index: 20;
        }}

        .modal-btn {{
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
            z-index: 20;
        }}

        .modal-btn.prev {{
            left: 18px;
        }}

        .modal-btn.next {{
            right: 18px;
        }}

        .modal-thumb-strip {{
            display: flex;
            gap: 10px;
            overflow-x: auto;
            padding-bottom: 4px;
            scrollbar-width: thin;
        }}

        .modal-thumb {{
            width: 110px;
            height: 78px;
            border-radius: 12px;
            overflow: hidden;
            flex: 0 0 auto;
            cursor: pointer;
            border: 2px solid transparent;
            background: rgba(255,255,255,0.16);
        }}

        .modal-thumb.active {{
            border-color: white;
        }}

        .modal-thumb img {{
            width: 100%;
            height: 100%;
            object-fit: cover;
            display: block;
        }}

        @media (max-width: 1100px) {{
            .carousel-container {{
                height: 560px;
            }}

            .modal-thumb {{
                width: 92px;
                height: 68px;
            }}
        }}

        @media (max-width: 768px) {{
            .carousel-frame {{
                padding: 10px;
                border-radius: 24px;
            }}

            .carousel-container {{
                height: 360px;
                border-radius: 18px;
            }}

            .carousel-btn {{
                width: 44px;
                height: 44px;
                font-size: 22px;
            }}

            .carousel-btn.prev {{
                left: 10px;
            }}

            .carousel-btn.next {{
                right: 10px;
            }}

            .carousel-dots {{
                bottom: 10px;
                gap: 8px;
            }}

            .carousel-dot {{
                width: 8px;
                height: 8px;
            }}

            .modal {{
                padding: 14px;
            }}

            .modal-content {{
                width: 100%;
                height: 92vh;
                gap: 12px;
            }}

            .modal-main {{
                border-radius: 16px;
            }}

            .modal-btn {{
                width: 44px;
                height: 44px;
                font-size: 22px;
            }}

            .modal-btn.prev {{
                left: 10px;
            }}

            .modal-btn.next {{
                right: 10px;
            }}

            .modal-close {{
                top: 10px;
                right: 10px;
                width: 38px;
                height: 38px;
                font-size: 20px;
            }}

            .modal-thumb {{
                width: 78px;
                height: 58px;
            }}
        }}

        @media (max-width: 480px) {{
            .carousel-frame {{
                padding: 8px;
                border-radius: 22px;
            }}

            .carousel-container {{
                height: 300px;
                border-radius: 16px;
            }}

            .carousel-btn {{
                width: 38px;
                height: 38px;
                font-size: 20px;
            }}

            .modal-thumb {{
                width: 68px;
                height: 52px;
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

        <div class="modal" id="imageModal">
            <div class="modal-content">
                <div class="modal-main">
                    <button class="modal-close" id="closeModal">&times;</button>
                    <button class="modal-btn prev" id="modalPrevBtn">&#10094;</button>
                    <button class="modal-btn next" id="modalNextBtn">&#10095;</button>
                    <img id="modalMainImage" src="" alt="Expanded image">
                </div>

                <div class="modal-thumb-strip" id="modalThumbStrip">
                    {modal_thumbs_str}
                </div>
            </div>
        </div>

        <script>
            const slides = document.querySelectorAll(".carousel-slide");
            const dots = document.querySelectorAll(".carousel-dot");
            const modalThumbs = document.querySelectorAll(".modal-thumb");

            const prevBtn = document.getElementById("prevBtn");
            const nextBtn = document.getElementById("nextBtn");

            const modal = document.getElementById("imageModal");
            const modalMainImage = document.getElementById("modalMainImage");
            const closeModal = document.getElementById("closeModal");
            const modalPrevBtn = document.getElementById("modalPrevBtn");
            const modalNextBtn = document.getElementById("modalNextBtn");

            let current = 0;
            let autoplay = null;

            function stopAutoplay() {{
                if (autoplay) {{
                    clearInterval(autoplay);
                    autoplay = null;
                }}
            }}

            function restartAutoplay() {{
                stopAutoplay();
                autoplay = setInterval(nextSlide, {autoplay_ms});
            }}

            function updateModalThumbs(index) {{
                modalThumbs.forEach((thumb, i) => {{
                    thumb.classList.toggle("active", i === index);
                }});
            }}

            function updateModalImage(index) {{
                const activeImg = slides[index].querySelector("img");
                modalMainImage.src = activeImg.src;
                updateModalThumbs(index);
            }}

            function showSlide(index) {{
                slides.forEach((slide, i) => {{
                    slide.classList.toggle("active", i === index);
                }});
                dots.forEach((dot, i) => {{
                    dot.classList.toggle("active", i === index);
                }});
                current = index;

                if (modal.classList.contains("open")) {{
                    updateModalImage(index);
                }}
            }}

            function nextSlide() {{
                showSlide((current + 1) % slides.length);
            }}

            function prevSlide() {{
                showSlide((current - 1 + slides.length) % slides.length);
            }}

            function openModal(index) {{
                stopAutoplay();
                current = index;
                updateModalImage(index);
                modal.classList.add("open");
            }}

            function closeModalFn() {{
                modal.classList.remove("open");
                restartAutoplay();
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

            slides.forEach(slide => {{
                slide.onclick = () => {{
                    const index = Number(slide.dataset.index);
                    openModal(index);
                }};
            }});

            modalThumbs.forEach(thumb => {{
                thumb.onclick = () => {{
                    const index = Number(thumb.dataset.index);
                    showSlide(index);
                }};
            }});

            modalNextBtn.onclick = () => nextSlide();
            modalPrevBtn.onclick = () => prevSlide();
            closeModal.onclick = closeModalFn;

            modal.onclick = (e) => {{
                if (e.target === modal) {{
                    closeModalFn();
                }}
            }};

            document.addEventListener("keydown", (e) => {{
                if (!modal.classList.contains("open")) return;

                if (e.key === "Escape") closeModalFn();
                if (e.key === "ArrowRight") nextSlide();
                if (e.key === "ArrowLeft") prevSlide();
            }});

            showSlide(0);
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
    @import url('https://fonts.googleapis.com/css2?family=Source+Sans+3:wght@600;700;800&display=swap');

    .stApp {{
        background: transparent;
        font-family: "Source Sans 3", Arial, sans-serif;
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
        padding-left: 1rem;
        padding-right: 1rem;
    }}

    .header-wrap-main {{
        width: 100%;
        max-width: 1320px;
        margin: 0 auto 24px auto;
        box-sizing: border-box;
    }}

    .header-box-main {{
        width: 100%;
        min-height: 136px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 24px;

        background: rgba(255,255,255,0.42);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);

        border: 1px solid rgba(255,255,255,0.18);
        border-radius: 28px;
        padding: 18px 28px;
        box-sizing: border-box;
        overflow: hidden;
        box-shadow: 0 8px 24px rgba(0,0,0,0.08);
    }}

    .header-left-main {{
        display: flex;
        align-items: center;
        gap: 22px;
        min-width: 0;
        height: 100%;
        flex: 1 1 auto;
    }}

    .left-logo-main {{
        width: 95px;
        height: auto;
        display: block;
        position: relative;
        top: -3px;
        flex-shrink: 0;
    }}

    .right-logo-main {{
        width: 220px;
        height: auto;
        display: block;
        flex-shrink: 0;
    }}

    .title-main {{
        display: flex;
        align-items: center;
        font-size: 44px;
        font-weight: 800;
        line-height: 1.02;
        color: #20263a;
        white-space: nowrap;
        margin: 0;
        padding: 0;
        font-family: "Source Sans 3", Arial, sans-serif;
    }}

    .mobile-logos-row {{
        display: none;
    }}

    .desktop-logo {{
        display: block;
    }}

    @media (max-width: 1100px) {{
        .title-main {{
            font-size: 34px;
            white-space: normal;
        }}

        .right-logo-main {{
            width: 180px;
        }}

        .header-box-main {{
            min-height: 120px;
        }}
    }}

    @media (max-width: 768px) {{
        .block-container {{
            padding-top: 1rem;
            padding-left: 0.7rem;
            padding-right: 0.7rem;
            padding-bottom: 0.7rem;
        }}

        .header-wrap-main {{
            margin: 0 auto 16px auto;
        }}

        .header-box-main {{
            flex-direction: column;
            align-items: center;
            gap: 12px;
            padding: 16px 18px;
            min-height: auto;
        }}

        .header-left-main {{
            width: 100%;
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 14px;
        }}

        .left-logo-main {{
            width: 64px;
            top: 0;
        }}

        .title-main {{
            font-size: 24px;
            line-height: 1.08;
            white-space: normal;
            text-align: center;
            justify-content: center;
        }}

        .desktop-logo {{
            display: none;
        }}

        .mobile-logos-row {{
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 14px;
            width: 100%;
        }}

        .mobile-logos-row .left-logo-main {{
            width: 64px;
            display: block;
        }}

        .mobile-logos-row .right-logo-main {{
            width: 130px;
            display: block;
        }}
    }}

    @media (max-width: 480px) {{
        .header-box-main {{
            padding: 14px 14px;
            border-radius: 24px;
        }}

        .left-logo-main {{
            width: 58px;
        }}

        .title-main {{
            font-size: 22px;
        }}

        .mobile-logos-row .left-logo-main {{
            width: 58px;
        }}

        .mobile-logos-row .right-logo-main {{
            width: 120px;
        }}
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# =========================
# HEADER
# =========================
st.markdown(
    f"""
    <div class="header-wrap-main">
        <div class="header-box-main">
            <div class="header-left-main">
                <img src="data:image/png;base64,{logo_left_b64}" class="left-logo-main" alt="Logo galería">
                <div class="title-main">Galería de la expedición</div>
            </div>

            <img src="data:image/png;base64,{logo_right_b64}" class="right-logo-main desktop-logo" alt="Logo Farmaenlace">

            <div class="mobile-logos-row">
                <img src="data:image/png;base64,{logo_left_b64}" class="left-logo-main" alt="Logo galería">
                <img src="data:image/png;base64,{logo_right_b64}" class="right-logo-main" alt="Logo Farmaenlace">
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# =========================
# CAROUSEL
# =========================
if gallery_images:
    carousel_html = build_carousel_html(gallery_images, autoplay_ms=3500)
    components.html(carousel_html, height=860, scrolling=False)
else:
    st.warning("No hay imágenes en la carpeta photos.")
