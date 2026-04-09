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

# =========================
# CAROUSEL HTML
# =========================
def build_carousel_html(image_paths, autoplay_ms=3500):

    slides_html = []
    dots_html = []
    thumbs_html = []

    for i, img_path in enumerate(image_paths):
        img_b64 = img_to_base64(img_path)
        mime = mime_from_suffix(img_path)

        slides_html.append(f"""
        <div class="carousel-slide {'active' if i == 0 else ''}" data-index="{i}">
            <img src="data:image/{mime};base64,{img_b64}">
        </div>
        """)

        dots_html.append(
            f'<span class="carousel-dot {"active" if i == 0 else ""}" data-index="{i}"></span>'
        )

        thumbs_html.append(f"""
        <div class="modal-thumb {'active' if i == 0 else ''}" data-index="{i}">
            <img src="data:image/{mime};base64,{img_b64}">
        </div>
        """)

    return f"""
    <html>
    <head>
    <style>
        html, body {{
            margin:0;
            padding:0;
            background:transparent;
            overflow:hidden;
        }}

        .carousel-frame {{
            background: rgba(255,255,255,0.42);
            backdrop-filter: blur(10px);
            border-radius: 28px;
            padding: 16px;
            overflow:hidden;
        }}

        .carousel-container {{
            position:relative;
            height:700px;
            border-radius:22px;
            overflow:hidden;
        }}

        .carousel-slide {{
            position:absolute;
            inset:0;
            opacity:0;
            transition:.5s;
            pointer-events:none;
            cursor:pointer;
        }}

        .carousel-slide.active {{
            opacity:1;
            pointer-events:auto;
        }}

        .carousel-slide img {{
            width:100%;
            height:100%;
            object-fit:contain;
        }}

        .carousel-btn {{
            position:absolute;
            top:50%;
            transform:translateY(-50%);
            width:58px;
            height:58px;
            border:none;
            border-radius:50%;
            background:rgba(0,0,0,.25);
            color:white;
            font-size:28px;
            cursor:pointer;
            z-index:10;
        }}

        .prev {{ left:20px; }}
        .next {{ right:20px; }}

        .carousel-dots {{
            position:absolute;
            bottom:15px;
            left:50%;
            transform:translateX(-50%);
            display:flex;
            gap:10px;
        }}

        .carousel-dot {{
            width:10px;
            height:10px;
            border-radius:50%;
            background:rgba(255,255,255,.4);
            cursor:pointer;
        }}

        .carousel-dot.active {{
            background:white;
        }}

        .modal {{
            display:none;
            position:fixed;
            inset:0;
            background:rgba(0,0,0,.9);
            z-index:9999;
            padding:20px;
        }}

        .modal.open {{
            display:flex;
            justify-content:center;
            align-items:center;
        }}

        .modal-content {{
            width:95%;
            height:90%;
            display:flex;
            flex-direction:column;
            gap:15px;
        }}

        .modal-main {{
            flex:1;
            position:relative;
        }}

        .modal-main img {{
            width:100%;
            height:100%;
            object-fit:contain;
        }}

        .modal-thumb-strip {{
            display:flex;
            gap:10px;
            overflow-x:auto;
        }}

        .modal-thumb {{
            width:100px;
            height:70px;
            cursor:pointer;
            flex-shrink:0;
        }}

        .modal-thumb img {{
            width:100%;
            height:100%;
            object-fit:cover;
        }}

        .modal-close {{
            position:absolute;
            top:10px;
            right:10px;
            background:black;
            color:white;
            border:none;
            font-size:30px;
            cursor:pointer;
            z-index:10;
        }}

        @media (max-width:768px) {{
            .carousel-container {{
                height:350px;
            }}

            .carousel-btn {{
                width:40px;
                height:40px;
                font-size:20px;
            }}
        }}

    </style>
    </head>
    <body>

    <div class="carousel-frame">
        <div class="carousel-container">

            {''.join(slides_html)}

            <button class="carousel-btn prev" id="prevBtn">&#10094;</button>
            <button class="carousel-btn next" id="nextBtn">&#10095;</button>

            <div class="carousel-dots">
                {''.join(dots_html)}
            </div>

        </div>
    </div>

    <div class="modal" id="modal">
        <div class="modal-content">

            <div class="modal-main">
                <button class="modal-close" id="closeModal">&times;</button>
                <img id="modalImg">
            </div>

            <div class="modal-thumb-strip">
                {''.join(thumbs_html)}
            </div>

        </div>
    </div>

    <script>

        const slides = document.querySelectorAll(".carousel-slide");
        const dots = document.querySelectorAll(".carousel-dot");
        const thumbs = document.querySelectorAll(".modal-thumb");

        const modal = document.getElementById("modal");
        const modalImg = document.getElementById("modalImg");

        let current = 0;
        let autoplay;

        function showSlide(index){{
            slides.forEach((s,i)=>s.classList.toggle("active",i===index));
            dots.forEach((d,i)=>d.classList.toggle("active",i===index));
            current=index;

            if(modal.classList.contains("open")){{
                modalImg.src=slides[index].querySelector("img").src;
            }}
        }}

        function nextSlide(){{
            showSlide((current+1)%slides.length);
        }}

        function prevSlide(){{
            showSlide((current-1+slides.length)%slides.length);
        }}

        function startAutoplay(){{
            autoplay=setInterval(nextSlide,{autoplay_ms});
        }}

        function stopAutoplay(){{
            clearInterval(autoplay);
        }}

        document.getElementById("nextBtn").onclick=()=>{{nextSlide();startOver();}};
        document.getElementById("prevBtn").onclick=()=>{{prevSlide();startOver();}};

        function startOver(){{
            stopAutoplay();
            startAutoplay();
        }}

        dots.forEach(dot=>{{
            dot.onclick=()=>{{
                showSlide(Number(dot.dataset.index));
                startOver();
            }};
        }});

        slides.forEach(slide=>{{
            slide.onclick=()=>{{
                stopAutoplay();
                modal.classList.add("open");
                modalImg.src=slide.querySelector("img").src;
            }};
        }});

        thumbs.forEach(thumb=>{{
            thumb.onclick=()=>{{
                const index=Number(thumb.dataset.index);
                showSlide(index);
            }};
        }});

        document.getElementById("closeModal").onclick=()=>{{
            modal.classList.remove("open");
            startAutoplay();
        }};

        showSlide(0);
        startAutoplay();

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
st.markdown(f"""
<style>

.stApp {{
    background: transparent;
}}

.stApp::before {{
    content:"";
    position:fixed;
    inset:0;
    background:url("data:image/jpg;base64,{bg_b64}") center center / cover no-repeat;
    filter:blur(6px);
    transform:scale(1.03);
    opacity:.62;
    z-index:-2;
}}

.stApp::after {{
    content:"";
    position:fixed;
    inset:0;
    background:rgba(255,255,255,.05);
    z-index:-1;
}}

[data-testid="stHeader"] {{
    background:transparent;
}}

.block-container {{
    max-width:1450px;
    padding-top:2rem;
}}

.header-wrap-main {{
    max-width:1320px;
    margin:auto auto 24px auto;
}}

.header-box-main {{
    display:flex;
    justify-content:space-between;
    align-items:center;
    background:rgba(255,255,255,.42);
    backdrop-filter:blur(10px);
    border-radius:28px;
    padding:20px 30px;
}}

.header-left-main {{
    display:flex;
    align-items:center;
    gap:20px;
}}

.left-logo-main {{
    width:90px;
}}

.right-logo-main {{
    width:220px;
}}

.title-main {{
    font-size:44px;
    font-weight:800;
    color:#20263a;
}}

.mobile-right-logo {{
    display:none;
}}

@media (max-width:768px) {{

    .header-box-main {{
        flex-direction:column;
        gap:15px;
        text-align:center;
    }}

    .desktop-right-logo {{
        display:none;
    }}

    .mobile-right-logo {{
        display:block;
        width:120px;
    }}

    .header-left-main {{
        flex-direction:row;
        justify-content:center;
    }}

    .title-main {{
        font-size:26px;
    }}

    .left-logo-main {{
        width:65px;
    }}
}}

</style>
""", unsafe_allow_html=True)

# =========================
# HEADER
# =========================
st.markdown(f"""
<div class="header-wrap-main">
    <div class="header-box-main">

        <div class="header-left-main">
            <img src="data:image/png;base64,{logo_left_b64}" class="left-logo-main">
            <div class="title-main">Galería de la expedición</div>
        </div>

        <img src="data:image/png;base64,{logo_right_b64}" class="right-logo-main desktop-right-logo">

        <img src="data:image/png;base64,{logo_right_b64}" class="mobile-right-logo">

    </div>
</div>
""", unsafe_allow_html=True)

# =========================
# CAROUSEL
# =========================
if gallery_images:
    components.html(build_carousel_html(gallery_images), height=860)
else:
    st.warning("No hay imágenes.")
