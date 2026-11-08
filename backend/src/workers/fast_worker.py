"""ARQ worker for editor renders, exports, and social publishing."""

import os

from arq.connections import RedisSettings
from arq.worker import func

from ..config import Config
from ..services.clip_export_service import (
    CLIP_EXPORT_JOB_TIMEOUT_SECONDS,
    export_clip_preset,
)
from ..services.editor_service import combine_editor, export_editor, prepare_editor
from ..services.social_service import PUBLISH_JOB_TIMEOUT_SECONDS
from .job_queue import FAST_QUEUE_NAME
from .tasks import publish_social_post


class FastWorkerSettings:
    config = Config()
    functions = [
        prepare_editor,
        export_editor,
        combine_editor,
        func(
            export_clip_preset,
            timeout=CLIP_EXPORT_JOB_TIMEOUT_SECONDS,
            max_tries=1,
        ),
        func(
            publish_social_post,
            timeout=PUBLISH_JOB_TIMEOUT_SECONDS,
            keep_result=0,
        ),
    ]
    queue_name = FAST_QUEUE_NAME
    redis_settings = RedisSettings(
        host=config.redis_host, port=config.redis_port, database=0
    )
    max_jobs = max(1, int(os.getenv("FAST_WORKER_MAX_JOBS", "2")))
    health_check_interval = 30
