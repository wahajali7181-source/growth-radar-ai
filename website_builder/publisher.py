import json
import os
import shutil
import socket
import subprocess
import time
import urllib.error
import urllib.request
import zipfile
import urllib.parse

# ==========================================================
# CONFIG
# ==========================================================

NETLIFY_API = "https://api.netlify.com/api/v1"

NETLIFY_TOKEN_ENV = "GROWTHRADAR_NETLIFY_TOKEN"

REGISTRY_DIR = "data"
REGISTRY_FILE = os.path.join(
    REGISTRY_DIR,
    "website_publishing.json"
)


# ==========================================================
# SAFE PORT FINDER
# ==========================================================

def find_free_port(
    start_port=5173,
    max_attempts=100
):

    for port in range(
        start_port,
        start_port + max_attempts
    ):

        with socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        ) as sock:

            sock.setsockopt(
                socket.SOL_SOCKET,
                socket.SO_REUSEADDR,
                1
            )

            try:

                sock.bind(
                    ("127.0.0.1", port)
                )

                return port

            except OSError:

                continue

    return None


# ==========================================================
# PROJECT VALIDATION
# ==========================================================

def validate_project(folder):

    if not folder:

        return {
            "valid": False,
            "reason": "Project folder is missing."
        }

    folder = os.path.abspath(folder)

    if not os.path.isdir(folder):

        return {
            "valid": False,
            "reason":
                "Website project folder does not exist."
        }

    required_files = [

        "index.html",

        "package.json",

        "vite.config.js",

        "tailwind.config.js",

        os.path.join(
            "src",
            "App.jsx"
        ),

        os.path.join(
            "src",
            "main.jsx"
        ),

        os.path.join(
            "src",
            "App.css"
        )

    ]

    missing = []

    for file in required_files:

        path = os.path.join(
            folder,
            file
        )

        if not os.path.isfile(path):

            missing.append(file)

    if missing:

        return {

            "valid": False,

            "reason":
                "Required website files are missing.",

            "missing":
                missing

        }

    return {

        "valid": True,

        "reason":
            "Website project is valid."

    }


# ==========================================================
# NPM
# ==========================================================

def _npm_command():

    if os.name == "nt":

        return "npm.cmd"

    return "npm"


# ==========================================================
# INSTALL DEPENDENCIES
# ==========================================================

def install_dependencies(folder):

    validation = validate_project(
        folder
    )

    if not validation["valid"]:

        return {

            "success": False,

            "message":
                validation["reason"],

            "error":
                validation.get("missing")

        }

    npm = _npm_command()

    try:

        result = subprocess.run(

            [
                npm,
                "install"
            ],

            cwd=folder,

            capture_output=True,

            text=True,

            timeout=300

        )

        if result.returncode != 0:

            return {

                "success": False,

                "message":
                    "Unable to install website dependencies.",

                "error":
                    result.stderr[-4000:]

            }

        return {

            "success": True,

            "message":
                "Website dependencies installed successfully."

        }

    except FileNotFoundError:

        return {

            "success": False,

            "message":
                "Node.js / npm was not found on this computer.",

            "error":
                "npm.cmd could not be found."

        }

    except subprocess.TimeoutExpired:

        return {

            "success": False,

            "message":
                "Dependency installation timed out.",

            "error":
                "npm install exceeded 5 minutes."

        }

    except Exception as e:

        return {

            "success": False,

            "message":
                "Unable to install dependencies.",

            "error":
                str(e)

        }


# ==========================================================
# BUILD WEBSITE
# ==========================================================

def build_website(folder):

    validation = validate_project(
        folder
    )

    if not validation["valid"]:

        return {
            "success": False,
            "message": validation["reason"],
            "error": validation.get("missing")
        }

    folder = os.path.abspath(
        folder
    )

    # ======================================================
    # INSTALL DEPENDENCIES
    # ======================================================

    install_result = install_dependencies(
        folder
    )

    if not install_result["success"]:

        return install_result

    npm = _npm_command()

    process = None

    try:

        # ==================================================
        # START BUILD PROCESS
        # ==================================================

        process = subprocess.Popen(

            [
                npm,
                "run",
                "build"
            ],

            cwd=folder,

            stdout=subprocess.PIPE,

            stderr=subprocess.PIPE,

            text=True,

            encoding="utf-8",

            errors="replace",

            creationflags=(
                subprocess.CREATE_NEW_PROCESS_GROUP
                if os.name == "nt"
                else 0
            )

        )

        try:

            stdout, stderr = process.communicate(
                timeout=180
            )

        except subprocess.TimeoutExpired:

            # ==============================================
            # WINDOWS PROCESS TREE CLEANUP
            # ==============================================

            if os.name == "nt":

                try:

                    subprocess.run(

                        [
                            "taskkill",
                            "/PID",
                            str(process.pid),
                            "/T",
                            "/F"
                        ],

                        capture_output=True,

                        text=True,

                        timeout=15

                    )

                except Exception:

                    pass

            else:

                try:

                    process.kill()

                except Exception:

                    pass

            try:

                process.wait(
                    timeout=10
                )

            except Exception:

                pass

            return {

                "success": False,

                "message":
                    "Website production build timed out.",

                "error":
                    "npm run build exceeded 3 minutes and the process was terminated."

            }

        # ==================================================
        # BUILD FAILED
        # ==================================================

        if process.returncode != 0:

            error_output = (
                stderr.strip()
                or stdout.strip()
                or "Unknown npm build error."
            )

            return {

                "success": False,

                "message":
                    "Website production build failed.",

                "error":
                    error_output[-8000:]

            }

        # ==================================================
        # VERIFY DIST
        # ==================================================

        dist = os.path.join(
            folder,
            "dist"
        )

        if not os.path.isdir(dist):

            return {

                "success": False,

                "message":
                    "Build completed but dist folder was not created.",

                "error":
                    dist

            }

        # ==================================================
        # VERIFY DIST CONTENT
        # ==================================================

        try:

            dist_files = []

            for root, _, filenames in os.walk(
                dist
            ):

                for filename in filenames:

                    dist_files.append(
                        os.path.join(
                            root,
                            filename
                        )
                    )

            if not dist_files:

                return {

                    "success": False,

                    "message":
                        "Build completed but dist folder is empty.",

                    "error":
                        dist

                }

        except Exception as e:

            return {

                "success": False,

                "message":
                    "Unable to verify production build.",

                "error":
                    str(e)

            }

        # ==================================================
        # SUCCESS
        # ==================================================

        return {

            "success": True,

            "folder":
                folder,

            "dist":
                dist,

            "message":
                "Website production build completed successfully.",

            "files":
                len(dist_files)

        }

    except FileNotFoundError:

        return {

            "success": False,

            "message":
                "Node.js / npm was not found.",

            "error":
                "npm.cmd could not be started."

        }

    except Exception as e:

        # ==================================================
        # SAFETY CLEANUP
        # ==================================================

        if process is not None:

            try:

                if process.poll() is None:

                    if os.name == "nt":

                        subprocess.run(

                            [
                                "taskkill",
                                "/PID",
                                str(process.pid),
                                "/T",
                                "/F"
                            ],

                            capture_output=True,

                            text=True,

                            timeout=10

                        )

                    else:

                        process.kill()

            except Exception:

                pass

        return {

            "success": False,

            "message":
                "Unable to build website.",

            "error":
                str(e)

        }

# ==========================================================
# START LOCAL PREVIEW
# ==========================================================

def start_preview_server(folder):

    validation = validate_project(
        folder
    )

    if not validation["valid"]:

        return {

            "success": False,
            "url": None,
            "port": None,
            "message":
                validation["reason"],
            "error":
                validation.get("missing")

        }

    folder = os.path.abspath(
        folder
    )

    install_result = install_dependencies(
        folder
    )

    if not install_result["success"]:

        return {

            "success": False,
            "url": None,
            "port": None,
            "message":
                install_result["message"],
            "error":
                install_result.get("error")

        }

    port = find_free_port()

    if port is None:

        return {

            "success": False,
            "url": None,
            "port": None,
            "message":
                "No free port available.",
            "error":
                "Could not find an available local port."

        }

    npm = _npm_command()

    try:

        process = subprocess.Popen(

            [
                npm,
                "run",
                "dev",
                "--",
                "--host",
                "127.0.0.1",
                "--port",
                str(port)
            ],

            cwd=folder,

            stdout=subprocess.DEVNULL,

            stderr=subprocess.DEVNULL,

            creationflags=(
                subprocess.CREATE_NEW_PROCESS_GROUP
                if os.name == "nt"
                else 0
            )

        )

        time.sleep(2)

        if process.poll() is not None:

            return {

                "success": False,
                "url": None,
                "port": None,
                "message":
                    "Website server stopped immediately.",
                "error":
                    "Vite server could not be started."

            }

        url = (
            f"http://127.0.0.1:{port}"
        )

        return {

            "success": True,
            "url": url,
            "port": port,
            "pid": process.pid,
            "folder": folder,
            "message":
                "Website preview server started successfully."

        }

    except FileNotFoundError:

        return {

            "success": False,
            "url": None,
            "port": None,
            "message":
                "Node.js / npm was not found.",
            "error":
                "npm.cmd could not be started."

        }

    except Exception as e:

        return {

            "success": False,
            "url": None,
            "port": None,
            "message":
                "Unable to start website server.",
            "error":
                str(e)

        }


# ==========================================================
# STOP LOCAL PREVIEW
# ==========================================================

def stop_preview_server(
    process_id
):

    if not process_id:

        return {

            "success": False,

            "message":
                "Process ID is missing."

        }

    try:

        if os.name == "nt":

            subprocess.run(

                [
                    "taskkill",
                    "/PID",
                    str(process_id),
                    "/T",
                    "/F"
                ],

                capture_output=True,

                text=True

            )

        else:

            os.kill(
                int(process_id),
                15
            )

        return {

            "success": True,

            "message":
                "Website preview server stopped."

        }

    except Exception as e:

        return {

            "success": False,

            "message":
                "Unable to stop preview server.",

            "error":
                str(e)

        }


# ==========================================================
# PUBLISH PACKAGE
# ==========================================================

def prepare_publish_package(
    folder
):

    validation = validate_project(
        folder
    )

    if not validation["valid"]:

        return {

            "success": False,

            "folder": None,

            "message":
                validation["reason"]

        }

    folder = os.path.abspath(
        folder
    )

    project_name = os.path.basename(
        folder
    )

    publish_root = os.path.abspath(
        "published_sites"
    )

    publish_folder = os.path.join(
        publish_root,
        project_name
    )

    os.makedirs(
        publish_folder,
        exist_ok=True
    )

    for item in os.listdir(folder):

        if item == "node_modules":
            continue

        if item == "dist":
            continue

        source = os.path.join(
            folder,
            item
        )

        destination = os.path.join(
            publish_folder,
            item
        )

        if os.path.isdir(source):

            if os.path.exists(destination):

                shutil.rmtree(
                    destination
                )

            shutil.copytree(
                source,
                destination
            )

        else:

            shutil.copy2(
                source,
                destination
            )

    return {

        "success": True,

        "folder":
            publish_folder,

        "message":
            "Website publish package prepared successfully."

    }


# ==========================================================
# NETLIFY TOKEN
# ==========================================================

def _get_netlify_token():

    # ==========================================================
    # 1. NORMAL ENVIRONMENT VARIABLE
    # ==========================================================

    token = os.getenv(
        NETLIFY_TOKEN_ENV
    )

    if token:

        return token.strip()


    # ==========================================================
    # 2. WINDOWS USER REGISTRY FALLBACK
    # ==========================================================

    if os.name == "nt":

        try:

            import winreg

            with winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Environment"
            ) as key:

                value, _ = winreg.QueryValueEx(
                    key,
                    NETLIFY_TOKEN_ENV
                )

                if value:

                    return str(
                        value
                    ).strip()

        except Exception:

            pass


    # ==========================================================
    # 3. TOKEN NOT FOUND
    # ==========================================================

    return None

# ==========================================================
# NETLIFY REQUEST
# ==========================================================

def _netlify_request(
    method,
    path,
    body=None,
    content_type="application/json"
):

    token = _get_netlify_token()

    if not token:

        raise RuntimeError(
            "Netlify API token is not configured. "
            f"Set {NETLIFY_TOKEN_ENV}."
        )

    url = (
        NETLIFY_API
        + path
    )

    headers = {

        "Authorization":
            f"Bearer {token}",

        "User-Agent":
            "GrowthRadarAI-WebsiteBuilder/1.0",

        "Accept":
            "application/json"

    }

    if body is not None:

        headers["Content-Type"] = (
            content_type
        )

    request = urllib.request.Request(

        url,

        data=body,

        headers=headers,

        method=method

    )

    try:

        with urllib.request.urlopen(
            request,
            timeout=120
        ) as response:

            raw = response.read()

            if not raw:

                return {}

            return json.loads(
                raw.decode(
                    "utf-8"
                )
            )

    except urllib.error.HTTPError as e:

        error_body = ""

        try:

            error_body = (
                e.read()
                .decode("utf-8")
            )

        except Exception:
            pass

        raise RuntimeError(
            f"Netlify API error "
            f"{e.code}: "
            f"{error_body[:4000]}"
        )

    except urllib.error.URLError as e:

        raise RuntimeError(
            f"Unable to connect to Netlify: {e}"
        )


# ==========================================================
# CREATE ZIP FROM DIST
# ==========================================================

def _zip_dist(
    dist_folder
):

    if not os.path.isdir(
        dist_folder
    ):

        raise RuntimeError(
            "dist folder does not exist."
        )

    zip_path = os.path.join(

        os.path.dirname(
            dist_folder
        ),

        "website_deploy.zip"

    )

    if os.path.exists(
        zip_path
    ):

        os.remove(
            zip_path
        )

    with zipfile.ZipFile(

        zip_path,

        "w",

        compression=zipfile.ZIP_DEFLATED

    ) as archive:

        for root, _, files in os.walk(
            dist_folder
        ):

            for filename in files:

                full_path = os.path.join(
                    root,
                    filename
                )

                relative_path = os.path.relpath(
                    full_path,
                    dist_folder
                )

                archive.write(
                    full_path,
                    relative_path
                )

    return zip_path


# ==========================================================
# WEBSITE REGISTRY
# ==========================================================

def _load_registry():

    os.makedirs(
        REGISTRY_DIR,
        exist_ok=True
    )

    if not os.path.isfile(
        REGISTRY_FILE
    ):

        return {}

    try:

        with open(
            REGISTRY_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(
                file
            )

            if isinstance(
                data,
                dict
            ):

                return data

    except Exception:
        pass

    return {}


def _save_registry(
    registry
):

    os.makedirs(
        REGISTRY_DIR,
        exist_ok=True
    )

    temp_file = (
        REGISTRY_FILE
        + ".tmp"
    )

    with open(
        temp_file,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            registry,
            file,
            indent=4
        )

    os.replace(
        temp_file,
        REGISTRY_FILE
    )


def _registry_key(
    folder
):

    return os.path.normcase(
        os.path.abspath(
            folder
        )
    )


# ==========================================================
# NETLIFY SITE NAME
# ==========================================================

def _netlify_site_name(
    business_name
):

    value = str(
        business_name
    ).strip().lower()

    result = []

    for char in value:

        if char.isalnum():

            result.append(
                char
            )

        elif char in [
            " ",
            "-",
            "_"
        ]:

            if not result or result[-1] != "-":

                result.append("-")

    name = "".join(
        result
    ).strip("-")

    if not name:

        name = "growth-radar-site"

    return name[:50]

# existing_netlify_site
def find_existing_netlify_site(
    business_name
):
    """
    Find an existing Netlify site by its
    generated site name.

    This prevents duplicate-site errors when
    the local publishing registry is missing.
    """

    site_name = _netlify_site_name(
        business_name
    )

    try:

        encoded_name = urllib.parse.quote(
            site_name
        )

        sites = _netlify_request(
            "GET",
            f"/sites?name={encoded_name}"
        )

        if not isinstance(
            sites,
            list
        ):

            return None

        # Prefer exact site-name match.
        for site in sites:

            if not isinstance(
                site,
                dict
            ):

                continue

            existing_name = str(
                site.get(
                    "name",
                    ""
                )
            ).strip().lower()

            if existing_name == site_name.lower():

                return site

        return None

    except Exception:

        # Discovery failure should not break
        # the normal create-site flow.
        return None
# ==========================================================
# CREATE NETLIFY SITE
# ==========================================================

def create_netlify_site(
    business_name
):

    site_name = _netlify_site_name(
        business_name
    )

    payload = json.dumps({

        "name":
            site_name

    }).encode(
        "utf-8"
    )

    return _netlify_request(

        "POST",

        "/sites",

        body=payload,

        content_type="application/json"

    )


# ==========================================================
# DEPLOY ZIP TO NETLIFY
# ==========================================================

def _deploy_zip(
    site_id,
    zip_path
):

    with open(
        zip_path,
        "rb"
    ) as file:

        zip_data = file.read()

    return _netlify_request(

        "POST",

        f"/sites/{site_id}/deploys",

        body=zip_data,

        content_type="application/zip"

    )


# ==========================================================
# PUBLISH NEW WEBSITE
# ==========================================================
def publish_to_netlify(
    folder,
    business_name=None
):

    validation = validate_project(
        folder
    )

    if not validation["valid"]:

        return {

            "success": False,

            "site_id": None,

            "deploy_id": None,

            "live_url": None,

            "folder": folder,

            "message":
                validation["reason"],

            "error":
                validation.get(
                    "missing"
                )

        }

    folder = os.path.abspath(
        folder
    )

    if not business_name:

        business_name = os.path.basename(
            folder
        )

    existing = None

    try:

        # ======================================================
        # BUILD WEBSITE
        # ======================================================

        build_result = build_website(
            folder
        )

        if not build_result.get(
            "success"
        ):

            return build_result

        # ======================================================
        # LOAD LOCAL REGISTRY
        # ======================================================

        registry = _load_registry()

        key = _registry_key(
            folder
        )

        existing = registry.get(
            key
        )

        # ======================================================
        # CASE 1
        # LOCAL REGISTRY HAS SITE
        # ======================================================

        if (
            existing
            and existing.get("site_id")
        ):

            site_id = existing.get(
                "site_id"
            )

            zip_path = None

            try:

                zip_path = _zip_dist(
                    build_result["dist"]
                )

                deploy = _deploy_zip(
                    site_id,
                    zip_path
                )

                live_url = (
                    deploy.get("ssl_url")
                    or deploy.get("url")
                    or existing.get("live_url")
                )

                existing[
                    "business_name"
                ] = business_name

                existing[
                    "folder"
                ] = folder

                existing[
                    "live_url"
                ] = live_url

                existing[
                    "last_deploy_id"
                ] = deploy.get(
                    "id"
                )

                existing[
                    "updated_at"
                ] = time.time()

                registry[key] = existing

                _save_registry(
                    registry
                )

                return {

                    "success": True,

                    "site_id":
                        site_id,

                    "deploy_id":
                        deploy.get(
                            "id"
                        ),

                    "live_url":
                        live_url,

                    "admin_url":
                        existing.get(
                            "admin_url"
                        ),

                    "folder":
                        folder,

                    "message":
                        "Website updated successfully."

                }

            finally:

                if zip_path:

                    try:

                        os.remove(
                            zip_path
                        )

                    except Exception:
                        pass

        # ======================================================
        # CASE 2
        # REGISTRY DOES NOT HAVE SITE
        #
        # Search Netlify directly.
        # ======================================================

        netlify_site = (
            find_existing_netlify_site(
                business_name
            )
        )

        if netlify_site:

            site_id = netlify_site.get(
                "id"
            )

            if not site_id:

                raise RuntimeError(
                    "Existing Netlify site was found "
                    "but no site ID was returned."
                )

            zip_path = None

            try:

                zip_path = _zip_dist(
                    build_result["dist"]
                )

                deploy = _deploy_zip(
                    site_id,
                    zip_path
                )

                live_url = (
                    deploy.get("ssl_url")
                    or deploy.get("url")
                    or netlify_site.get("ssl_url")
                    or netlify_site.get("url")
                )

                # ==================================================
                # RESTORE LOCAL REGISTRY
                # ==================================================

                registry[key] = {

                    "site_id":
                        site_id,

                    "business_name":
                        business_name,

                    "folder":
                        folder,

                    "live_url":
                        live_url,

                    "site_name":
                        netlify_site.get(
                            "name"
                        ),

                    "admin_url":
                        netlify_site.get(
                            "admin_url"
                        ),

                    "last_deploy_id":
                        deploy.get(
                            "id"
                        ),

                    "updated_at":
                        time.time()

                }

                _save_registry(
                    registry
                )

                return {

                    "success": True,

                    "site_id":
                        site_id,

                    "deploy_id":
                        deploy.get(
                            "id"
                        ),

                    "live_url":
                        live_url,

                    "admin_url":
                        netlify_site.get(
                            "admin_url"
                        ),

                    "folder":
                        folder,

                    "message":
                        "Existing Netlify website found and updated successfully."

                }

            finally:

                if zip_path:

                    try:

                        os.remove(
                            zip_path
                        )

                    except Exception:
                        pass

        # ======================================================
        # CASE 3
        # NO EXISTING SITE
        #
        # Create a brand-new Netlify site.
        # ======================================================

        site = create_netlify_site(
            business_name
        )

        site_id = site.get(
            "id"
        )

        if not site_id:

            raise RuntimeError(
                "Netlify created the site "
                "but returned no site ID."
            )

        zip_path = None

        try:

            zip_path = _zip_dist(
                build_result["dist"]
            )

            deploy = _deploy_zip(
                site_id,
                zip_path
            )

            live_url = (
                deploy.get("ssl_url")
                or deploy.get("url")
                or site.get("ssl_url")
                or site.get("url")
            )

            # ==================================================
            # SAVE NEW SITE TO REGISTRY
            # ==================================================

            registry[key] = {

                "site_id":
                    site_id,

                "business_name":
                    business_name,

                "folder":
                    folder,

                "live_url":
                    live_url,

                "site_name":
                    site.get(
                        "name"
                    ),

                "admin_url":
                    site.get(
                        "admin_url"
                    ),

                "last_deploy_id":
                    deploy.get(
                        "id"
                    ),

                "updated_at":
                    time.time()

            }

            _save_registry(
                registry
            )

            return {

                "success": True,

                "site_id":
                    site_id,

                "deploy_id":
                    deploy.get(
                        "id"
                    ),

                "live_url":
                    live_url,

                "admin_url":
                    site.get(
                        "admin_url"
                    ),

                "folder":
                    folder,

                "message":
                    "New website published successfully."

            }

        finally:

            if zip_path:

                try:

                    os.remove(
                        zip_path
                    )

                except Exception:
                    pass

    except Exception as e:

        return {

            "success": False,

            "site_id":
                existing.get(
                    "site_id"
                )
                if existing
                else None,

            "deploy_id": None,

            "live_url":
                existing.get(
                    "live_url"
                )
                if existing
                else None,

            "folder":
                folder,

            "message":
                "Unable to publish website.",

            "error":
                str(e)

        }


# ==========================================================
# UPDATE EXISTING WEBSITE
# ==========================================================

def update_netlify_site(
    folder
):

    validation = validate_project(
        folder
    )

    if not validation["valid"]:

        return {

            "success": False,

            "message":
                validation["reason"],

            "error":
                validation.get(
                    "missing"
                )

        }

    folder = os.path.abspath(
        folder
    )

    try:

        build_result = build_website(
            folder
        )

        if not build_result["success"]:

            return build_result

        registry = _load_registry()

        key = _registry_key(
            folder
        )

        existing = registry.get(
            key
        )

        if not existing:

            return {

                "success": False,

                "message":
                    "This website has not been published yet.",

                "error":
                    "No Netlify site record found."

            }

        site_id = existing.get(
            "site_id"
        )

        if not site_id:

            return {

                "success": False,

                "message":
                    "Netlify site ID is missing.",

                "error":
                    "Invalid publishing registry record."

            }

        zip_path = _zip_dist(
            build_result["dist"]
        )

        deploy = _deploy_zip(
            site_id,
            zip_path
        )

        live_url = (
            deploy.get("ssl_url")
            or deploy.get("url")
            or existing.get("live_url")
        )

        existing[
            "live_url"
        ] = live_url

        existing[
            "last_deploy_id"
        ] = deploy.get(
            "id"
        )

        existing[
            "updated_at"
        ] = time.time()

        registry[key] = existing

        _save_registry(
            registry
        )

        try:

            os.remove(
                zip_path
            )

        except Exception:
            pass

        return {

            "success": True,

            "site_id":
                site_id,

            "deploy_id":
                deploy.get(
                    "id"
                ),

            "live_url":
                live_url,

            "folder":
                folder,

            "message":
                "Live website updated successfully."

        }

    except Exception as e:

        return {

            "success": False,

            "site_id":
                existing.get(
                    "site_id"
                )
                if "existing" in locals()
                and existing
                else None,

            "deploy_id": None,

            "live_url": None,

            "folder":
                folder,

            "message":
                "Unable to update live website.",

            "error":
                str(e)

        }


# ==========================================================
# GET PUBLISHING RECORD
# ==========================================================

def get_publish_record(
    folder
):

    if not folder:

        return None

    registry = _load_registry()

    return registry.get(
        _registry_key(
            folder
        )
    )


# ==========================================================
# GET NETLIFY SITE STATUS
# ==========================================================

def get_publish_status(
    folder
):

    record = get_publish_record(
        folder
    )

    if not record:

        return {

            "success": False,

            "published": False,

            "message":
                "Website has not been published yet."

        }

    try:

        site_id = record[
            "site_id"
        ]

        site = _netlify_request(

            "GET",

            f"/sites/{site_id}"

        )

        deploys = _netlify_request(

            "GET",

            f"/sites/{site_id}/deploys"

        )

        latest = None

        if isinstance(
            deploys,
            list
        ) and deploys:

            latest = deploys[0]

        return {

            "success": True,

            "published": True,

            "site_id":
                site_id,

            "live_url":
                (
                    site.get("ssl_url")
                    or site.get("url")
                    or record.get("live_url")
                ),

            "site_name":
                site.get("name"),

            "custom_domain":
                site.get(
                    "custom_domain"
                ),

            "state":
                latest.get("state")
                if latest
                else None,

            "deploy_id":
                latest.get("id")
                if latest
                else None,

            "message":
                "Website publishing status retrieved successfully."

        }

    except Exception as e:

        return {

            "success": False,

            "published": True,

            "message":
                "Unable to retrieve publishing status.",

            "error":
                str(e)

        }


# ==========================================================
# CONNECT CUSTOM DOMAIN
# ==========================================================

def connect_custom_domain(
    folder,
    domain
):

    domain = str(
        domain or ""
    ).strip()

    if not domain:

        return {

            "success": False,

            "message":
                "Domain is required."

        }

    record = get_publish_record(
        folder
    )

    if not record:

        return {

            "success": False,

            "message":
                "Publish the website before connecting a domain."

        }

    site_id = record.get(
        "site_id"
    )

    if not site_id:

        return {

            "success": False,

            "message":
                "Netlify site ID is missing."

        }

    try:

        payload = json.dumps({

            "custom_domain":
                domain,

            "force_ssl":
                True

        }).encode(
            "utf-8"
        )

        site = _netlify_request(

            "PATCH",

            f"/sites/{site_id}",

            body=payload,

            content_type="application/json"

        )

        record[
            "custom_domain"
        ] = domain

        record[
            "updated_at"
        ] = time.time()

        registry = _load_registry()

        registry[
            _registry_key(folder)
        ] = record

        _save_registry(
            registry
        )

        return {

            "success": True,

            "domain":
                domain,

            "site_id":
                site_id,

            "live_url":
                site.get(
                    "ssl_url"
                )
                or site.get(
                    "url"
                ),

            "message":
                "Custom domain connected to the Netlify site. "
                "DNS must point to Netlify before SSL can become active."

        }

    except Exception as e:

        return {

            "success": False,

            "domain":
                domain,

            "message":
                "Unable to connect custom domain.",

            "error":
                str(e)

        }


# ==========================================================
# ROLLBACK
# ==========================================================

def rollback_website(
    folder,
    deploy_id
):

    if not deploy_id:

        return {

            "success": False,

            "message":
                "Deploy ID is required."

        }

    record = get_publish_record(
        folder
    )

    if not record:

        return {

            "success": False,

            "message":
                "Website publishing record was not found."

        }

    site_id = record.get(
        "site_id"
    )

    if not site_id:

        return {

            "success": False,

            "message":
                "Netlify site ID is missing."

        }

    try:

        result = _netlify_request(

            "POST",

            f"/sites/{site_id}"
            f"/deploys/{deploy_id}"
            f"/restore",

            body=b"{}",

            content_type="application/json"

        )

        record[
            "last_rollback_deploy_id"
        ] = deploy_id

        record[
            "updated_at"
        ] = time.time()

        registry = _load_registry()

        registry[
            _registry_key(folder)
        ] = record

        _save_registry(
            registry
        )

        return {

            "success": True,

            "site_id":
                site_id,

            "deploy_id":
                deploy_id,

            "live_url":
                result.get(
                    "ssl_url"
                )
                or result.get(
                    "url"
                ),

            "message":
                "Website rollback completed successfully."

        }

    except Exception as e:

        return {

            "success": False,

            "message":
                "Unable to rollback website.",

            "error":
                str(e)

        }


# ==========================================================
# PUBLISH OR UPDATE
# ==========================================================

def publish_website(
    folder,
    business_name=None
):

    record = get_publish_record(
        folder
    )

    if record and record.get(
        "site_id"
    ):

        return update_netlify_site(
            folder
        )

    return publish_to_netlify(

        folder,

        business_name

    )