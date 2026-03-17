from .iam_detection import run as iam_run
from .root_login_detection import run as root_login_run
from .s3_detection import run as s3_run

__all__ = ["iam_run", "root_login_run", "s3_run"]
