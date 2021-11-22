import sys
if(sys.version_info >= (3, 8)):
    from importlib.metadata import version
else:
    from importlib_metadata import version

__version__ = version(__package__)

from .captcha9kw import api9kw, CaptchaError
__all__ = ["api9kw", "CaptchaError"]
