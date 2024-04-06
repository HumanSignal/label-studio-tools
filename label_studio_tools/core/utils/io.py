import logging
import io
import shutil
import urllib
import hashlib
import requests
import os

from appdirs import user_cache_dir, user_data_dir
from urllib.parse import urlparse, urljoin
from contextlib import contextmanager
from tempfile import mkdtemp

from label_studio_tools.core.utils.params import get_env

_DIR_APP_NAME = 'label-studio'
LOCAL_FILES_DOCUMENT_ROOT = get_env(
    'LOCAL_FILES_DOCUMENT_ROOT', default=os.path.abspath(os.sep)
)

logger = logging.getLogger(__name__)

def concat_urls(base_url, url):
    return base_url.rstrip('/') + '/' + url.lstrip('/')

def get_data_dir():
    data_dir = user_data_dir(appname=_DIR_APP_NAME)
    os.makedirs(data_dir, exist_ok=True)
    return data_dir


def get_cache_dir():
    cache_dir = user_cache_dir(appname=_DIR_APP_NAME)
    os.makedirs(cache_dir, exist_ok=True)
    return cache_dir


def get_local_path(
    url,
    cache_dir=None,
    project_dir=None,
    hostname=None,
    image_dir=None,
    access_token=None,
    download_resources=True,
    task_id=None,
):
    """Get local path for url

    :param url: File url
    :param cache_dir: Cache directory to download or copy files
    :param project_dir: Project directory
    :param hostname: Hostname for external resource,
      if not provided, it will be taken from LABEL_STUDIO_URL env variable
    :param image_dir: Image and other media upload directory
    :param access_token: Access token for external resource (e.g. LS backend),
      if not provided, it will be taken from LABEL_STUDIO_API_KEY env variable
    :param download_resources: Download external files
    :param task_id: Label Studio Task ID, required for cloud storage files because of permissions

    :return: filepath
    """
    # get environment variables
    hostname = hostname or os.getenv('LABEL_STUDIO_URL', '')
    access_token = access_token or os.getenv('LABEL_STUDIO_API_KEY', '')
    if 'localhost' in hostname:
        logger.warning(
            f'Using `localhost` ({hostname}) in LABEL_STUDIO_URL, '
            f'`localhost` is not accessible inside of docker containers. '
            f'You can check your IP with utilities like `ifconfig` and set it as LABEL_STUDIO_URL.'
        )

    # try to get local directories
    if image_dir is None:
        upload_dir = os.path.join(get_data_dir(), 'media', 'upload')
        image_dir = project_dir and os.path.join(project_dir, 'upload') or upload_dir
        logger.debug(f"Image and upload dirs: image_dir={image_dir}, upload_dir={upload_dir}")

    # fix file upload url
    if url.startswith('upload') or url.startswith('/upload'):
        url = '/data' + ('' if url.startswith('/') else '/') + url

    is_local_storage_file = url.startswith('/data/') and '?d=' in url
    is_uploaded_file = url.startswith('/data/upload')
    is_cloud_storage_file = url.startswith('s3:') or url.startswith('gs:') or url.startswith('azure-blob:')

    # Local storage file: try to load locally otherwise download below
    if is_local_storage_file:
        filename, dir_path = url.split('/data/', 1)[-1].split('?d=')
        dir_path = str(urllib.parse.unquote(dir_path))
        filepath = os.path.join(LOCAL_FILES_DOCUMENT_ROOT, dir_path)
        if os.path.exists(filepath):
            logger.debug(f"Local Storage file path exists locally, use it as a local file: {filepath}")
            return filepath

    # Uploaded file: try to load locally otherwise download below
    if is_uploaded_file and os.path.exists(image_dir):
        project_id = url.split("/")[-2]  # To retrieve project_id
        image_dir = os.path.join(image_dir, project_id)
        filepath = os.path.join(image_dir, os.path.basename(url))
        if cache_dir and download_resources:
            shutil.copy(filepath, cache_dir)
        logger.debug(f"Uploaded file: Path exists in image_dir: {filepath}")
        return filepath

    # Upload or Local Storage file
    if is_uploaded_file or is_local_storage_file or is_cloud_storage_file:
        # hostname check
        if not hostname:
            raise FileNotFoundError(
                f"Can't resolve url, neither hostname or project_dir passed: {url}."
                "You can set LABEL_STUDIO_URL environment variable to use it as a hostname."
            )
        # uploaded and local storage file
        elif is_uploaded_file or is_local_storage_file:
            url = concat_urls(hostname, url)
            logger.info('Resolving url using hostname [' + hostname + ']: ' + url)
        # s3, gs, azure-blob file
        elif is_cloud_storage_file:
            if task_id is None:
                raise Exception("Label Studio Task ID is required for cloud storage files")
            url = concat_urls(hostname, f'/tasks/{task_id}/presign/?fileuri={url}')
            logger.info('Cloud storage file: Resolving url using hostname [' + hostname + ']: ' + url)

        # check access token
        if not access_token:
            raise FileNotFoundError(
                "To access uploaded and local storage files you have to " 
                "set LABEL_STUDIO_API_KEY environment variable."
            )

    filepath = download_and_cache(url, cache_dir, download_resources, hostname, access_token)
    return filepath


def download_and_cache(url, cache_dir, download_resources, hostname, access_token):
    # File specified by remote URL - download and cache it
    cache_dir = cache_dir or get_cache_dir()
    parsed_url = urlparse(url)
    url_filename = os.path.basename(parsed_url.path)
    url_hash = hashlib.md5(url.encode()).hexdigest()[:6]
    filepath = os.path.join(cache_dir, url_hash + '__' + url_filename)
    if not os.path.exists(filepath):
        logger.info('Download {url} to {filepath}'.format(url=url, filepath=filepath))
        if download_resources:
            # check if url matches hostname - then uses access token to this Label Studio instance
            logger.info(f"================> {parsed_url.netloc} :: {urlparse(hostname).netloc} :: {parsed_url.netloc == urlparse(hostname)}\n\n\n\n")
            if access_token and hostname and parsed_url.netloc == urlparse(hostname).netloc:
                headers = {
                    'Authorization': 'Bearer ' + access_token,
                    'Authorization': 'Token ' + access_token
                }
                logger.info("====> Authorization headers: " + str(headers))
            else:
                headers = {}
            r = requests.get(url, stream=True, headers=headers)
            r.raise_for_status()
            with io.open(filepath, mode='wb') as fout:
                fout.write(r.content)
    return filepath


@contextmanager
def get_temp_dir():
    dirpath = mkdtemp()
    yield dirpath
    shutil.rmtree(dirpath)


def get_all_files_from_dir(d):
    out = []
    for name in os.listdir(d):
        filepath = os.path.join(d, name)
        if os.path.isfile(filepath):
            out.append(filepath)
    return out
