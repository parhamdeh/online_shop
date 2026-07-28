from django.templatetags.static import static
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.utils.translation import get_language_info

UNFOLD = {
    "LOGIN": {
        
        # "image": lambda request: static("sample/login-bg.jpg"),
        "redirect_after": lambda request: reverse_lazy("admin:index"),
        # Inherits from `unfold.forms.AuthenticationForm`
        # "form": "users.forms.user_form.LoginForm",
    },

    # ==========================
    # General
    # ==========================

    "SITE_TITLE": "Programming Shop",
    "SITE_HEADER": "Programming Shop",
    "SITE_SYMBOL": "code",
    "SITE_URL": "/",

    # ==========================
    # Logo
    # ==========================

    "LOGO": {
        "light": lambda request: static("sample/login-bg.svg"),
        "dark": lambda request: static("sample/login-bg.svg"),
    },

    "FAVICONS": [
        {
            "rel": "icon",
            "href": lambda request: static("sample/login-bg.svg"),
        },
    ],

    # ==========================
    # Custom css/js
    # ==========================

    # "STYLES": [
    #     lambda request: static("css/custom.css"),
    # ],

    # "SCRIPTS": [
    #     lambda request: static("js/admin.js"),
    # ],
    "COLORS": {
    "primary": {
        "light": "59 130 246",   # Blue-500
        "dark": "96 165 250",    # Blue-400
    },
    "accent": {
        "light": "107 114 128",  # Gray-500
        "dark": "156 163 175",   # Gray-400
    },
},

    # ==========================
    # Sidebar
    # ==========================

    "SIDEBAR": {

        "show_search": True,
        "show_all_applications": False,
    },

    # ==========================
    # Header Dropdown
    # ==========================
    # Language selector - left empty so Unfold auto-detects both
    # languages ("fa" and "en") from the LANGUAGES setting below.
    # If you want custom local names/flags instead of auto-detection,
    # see the commented block further down.
    

    # Uncomment this instead of the block above if you want explicit
    # control over how each language is labeled in the switcher:
    "LANGUAGES" : {
        "navigation": [
            {
                "bidi": False,
                "code": "fa",
                "name": "Persian",
                "name_local": "فارسی",
                "name_translated": "Farsi",
            },
            {
                "bidi": False,
                "code": "en",
                "name": "English",
                "name_local": "English",
                "name_translated": "English",
            },
        ],
        },

    "SITE_DROPDOWN": [

        {
            "title": "🏠 سایت",
            "link": "/",
        },

        {
            "title": "📚 Swagger",
            "link": "/api/docs/",
        },
        

    ],

    # ==========================
    # Admin
    # ==========================

    "SHOW_HISTORY": False,
    "SHOW_BACK_BUTTON": True,
    "SHOW_VIEW_ON_SITE": True,
    "THEME_SWITCHER": True,
    "THEME": None,
    
    "SHOW_LANGUAGES": True,
}



LANGUAGE_CODE = "fa"
LANGUAGES = (
    ("fa", _("farsi")),
    ("en", _("English")),
)

TIME_ZONE = "Asia/Tehran"

USE_I18N = True

USE_TZ = True
CRISPY_TEMPLATE_PACK = "unfold_crispy"

CRISPY_ALLOWED_TEMPLATE_PACKS = ["unfold_crispy"]