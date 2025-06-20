import time
try:
    import yaml
except ImportError as exc:  # pragma: no cover - runtime dependency check
    raise SystemExit(
        "PyYAML is not installed. Run `pip install -r poc/frame-processor/requirements.txt`"
    ) from exc
from .processor import FrameProcessor


def load_config():
    with open('config.yaml') as f:
        return yaml.safe_load(f)


def main():
    cfg = load_config()
    processor = FrameProcessor(cfg)
    while True:
        processor.check_new_videos()
        time.sleep(10)


if __name__ == '__main__':
    main()
