import time
import yaml
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
