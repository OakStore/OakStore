import requests
from loguru import logger
from pathlib import Path
import time


def download(url, savePath="./Download", speed=0, progress_callback=None):
    """
    下载文件
    Args:
        url: 下载链接
        savePath: 保存位置，如：C:\Download；默认./Download
        speed: 下载限速（KB/S）；默认0（不限速）
    Returns:
        bool: 下载成功返回True，失败返回False
    """
    save_dir = Path(savePath)
    save_dir.mkdir(parents=True, exist_ok=True)

    filename = url.split('/')[-1].split('?')[0]
    if not filename:
        filename = "download_file"

    filepath = save_dir / filename
    logger.info(f"准备下载: {filename} 到 {filepath.absolute()}")

    try:
        response = requests.get(url, stream=True, timeout=10)
        response.raise_for_status()

        total_size = int(response.headers.get('content-length', 0))
        if total_size > 0:
            logger.info(f"文件大小: {total_size / 1024:.2f} KB ({total_size / (1024 * 1024):.2f} MB)")
        else:
            logger.warning("无法获取文件大小")
        downloaded = 0
        start_time = time.time()
        chunk_size = 8192

        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=chunk_size):
                if not chunk:
                    continue
                f.write(chunk)
                downloaded += len(chunk)

                if total_size > 0 and progress_callback:
                    progress = int((downloaded / total_size) * 100)
                    progress_callback(progress)

                if speed > 0:
                    elapsed = time.time() - start_time
                    expected_time = downloaded / (speed * 1024)
                    if elapsed < expected_time:
                        time.sleep(expected_time - elapsed)

                # 输出进度日志
                current_time = time.time()
                if current_time - last_log_time >= 1:
                    if total_size > 0:
                        progress = (downloaded / total_size) * 100
                        speed_bps = downloaded / (current_time - start_time) / 1024  # KB/s
                        logger.info(f"下载进度: {progress:.1f}% ({downloaded / 1024:.1f} KB / {total_size / 1024:.1f} KB) 速度: {speed_bps:.1f} KB/s")
                    else:
                        logger.info(f"已下载: {downloaded / 1024:.1f} KB")
                    last_log_time = current_time

        elapsed_time = time.time() - start_time
        avg_speed = downloaded / elapsed_time / 1024 if elapsed_time > 0 else 0

        if progress_callback:
            progress_callback(100)

        logger.info(f"下载完成，文件名: {filename}, 大小: {downloaded / 1024:.2f} KB, 耗时: {elapsed_time:.2f}秒, 平均速度: {avg_speed:.2f} KB/s")

        return True

    except Exception as e:
        logger.error(f"下载出错: {e}")
        if filepath.exists():
            filepath.unlink()
        if progress_callback:
            progress_callback(0)
        return False
