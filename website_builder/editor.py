import os
import json
import re
from datetime import datetime


# ==========================================================
# WEBSITE EDITOR
# ==========================================================

def _safe_read_file(path):

    try:

        if not os.path.isfile(path):

            return None

        with open(
            path,
            "r",
            encoding="utf-8"
        ) as file:

            return file.read()

    except Exception:

        return None


# ==========================================================
# SAFE WRITE
# ==========================================================

def _safe_write_file(
    path,
    content
):

    try:

        os.makedirs(
            os.path.dirname(path),
            exist_ok=True
        )

        temp_path = (
            path
            + ".tmp"
        )

        with open(
            temp_path,
            "w",
            encoding="utf-8"
        ) as file:

            file.write(
                content
            )

        os.replace(
            temp_path,
            path
        )

        return True

    except Exception:

        return False


# ==========================================================
# FIND WEBSITE FILES
# ==========================================================

def get_website_files(
    folder
):

    if not folder:

        return []

    folder = os.path.abspath(
        folder
    )

    if not os.path.isdir(
        folder
    ):

        return []

    allowed_extensions = {

        ".jsx",
        ".js",
        ".tsx",
        ".ts",
        ".css",
        ".html",
        ".json"

    }

    excluded_directories = {

        "node_modules",
        "dist",
        ".git",
        ".growthradar_backups",
        "__pycache__"

    }

    files = []

    for root, directories, filenames in os.walk(
        folder
    ):

        directories[:] = [

            directory
            for directory in directories
            if directory not in excluded_directories

        ]

        for filename in filenames:

            extension = os.path.splitext(
                filename
            )[1].lower()

            if extension not in allowed_extensions:

                continue

            files.append(

                os.path.join(
                    root,
                    filename
                )

            )

    return files


# ==========================================================
# WEBSITE SOURCE
# ==========================================================

def read_website_source(
    folder
):

    files = get_website_files(
        folder
    )

    source = []

    for path in files:

        content = _safe_read_file(
            path
        )

        if content is None:

            continue

        relative_path = os.path.relpath(
            path,
            folder
        )

        source.append({

            "file":
                relative_path,

            "content":
                content

        })

    return source


# ==========================================================
# CREATE BACKUP
# ==========================================================

def create_website_backup(
    folder
):

    if not folder:

        return {

            "success": False,

            "message":
                "Website folder is missing."

        }

    folder = os.path.abspath(
        folder
    )

    if not os.path.isdir(folder):

        return {

            "success": False,

            "message":
                "Website folder does not exist."

        }

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    backup_root = os.path.join(
        folder,
        ".growthradar_backups"
    )

    backup_folder = os.path.join(
        backup_root,
        timestamp
    )

    try:

        import shutil

        os.makedirs(
            backup_folder,
            exist_ok=True
        )

        for path in get_website_files(
            folder
        ):

            relative_path = os.path.relpath(
                path,
                folder
            )

            destination = os.path.join(
                backup_folder,
                relative_path
            )

            os.makedirs(
                os.path.dirname(destination),
                exist_ok=True
            )

            shutil.copy2(
                path,
                destination
            )

        return {

            "success": True,

            "folder":
                backup_folder,

            "message":
                "Website backup created successfully."

        }

    except Exception as e:

        return {

            "success": False,

            "folder":
                None,

            "message":
                "Unable to create website backup.",

            "error":
                str(e)

        }


# ==========================================================
# RESTORE BACKUP
# ==========================================================

def restore_website_backup(
    folder,
    backup_folder
):

    if not folder:

        return {

            "success": False,

            "message":
                "Website folder is missing."

        }

    if not backup_folder:

        return {

            "success": False,

            "message":
                "Backup folder is missing."

        }

    folder = os.path.abspath(
        folder
    )

    backup_folder = os.path.abspath(
        backup_folder
    )

    if not os.path.isdir(
        backup_folder
    ):

        return {

            "success": False,

            "message":
                "Backup folder does not exist."

        }

    try:

        for root, directories, filenames in os.walk(
            backup_folder
        ):

            for filename in filenames:

                source = os.path.join(
                    root,
                    filename
                )

                relative_path = os.path.relpath(
                    source,
                    backup_folder
                )

                destination = os.path.join(
                    folder,
                    relative_path
                )

                os.makedirs(
                    os.path.dirname(destination),
                    exist_ok=True
                )

                with open(
                    source,
                    "rb"
                ) as source_file:

                    data = source_file.read()

                with open(
                    destination,
                    "wb"
                ) as destination_file:

                    destination_file.write(
                        data
                    )

        return {

            "success": True,

            "message":
                "Website backup restored successfully."

        }

    except Exception as e:

        return {

            "success": False,

            "message":
                "Unable to restore website backup.",

            "error":
                str(e)

        }


# ==========================================================
# LOCATE MAIN APP
# ==========================================================

def find_main_app_file(
    folder
):

    candidates = [

        os.path.join(
            folder,
            "src",
            "App.jsx"
        ),

        os.path.join(
            folder,
            "src",
            "App.js"
        ),

        os.path.join(
            folder,
            "src",
            "App.tsx"
        ),

        os.path.join(
            folder,
            "src",
            "App.ts"
        )

    ]

    for path in candidates:

        if os.path.isfile(path):

            return path

    return None


# ==========================================================
# LOCATE CSS
# ==========================================================

def find_main_css_file(
    folder
):

    candidates = [

        os.path.join(
            folder,
            "src",
            "App.css"
        ),

        os.path.join(
            folder,
            "src",
            "index.css"
        ),

        os.path.join(
            folder,
            "src",
            "main.css"
        )

    ]

    for path in candidates:

        if os.path.isfile(path):

            return path

    return None


# ==========================================================
# SIMPLE TEXT EDIT
# ==========================================================
# ==========================================================
# SIMPLE TEXT EDIT
# ==========================================================

def replace_text(
    folder,
    old_text,
    new_text,
    replace_all=False
):

    if not old_text:

        return {

            "success": False,

            "message":
                "Old text is required."

        }

    if new_text is None:

        new_text = ""

    files = get_website_files(
        folder
    )

    matches = []

    # ------------------------------------------------------
    # FIND MATCHING FILES
    # ------------------------------------------------------

    for path in files:

        content = _safe_read_file(
            path
        )

        if content is None:

            continue

        if old_text in content:

            matches.append(
                path
            )

    if not matches:

        return {

            "success": False,

            "message":
                "The requested text was not found in the website."

        }

    # ------------------------------------------------------
    # SAFE MULTI-FILE PROTECTION
    # ------------------------------------------------------

    if len(matches) > 1:

        return {

            "success": False,

            "message":
                "The requested text exists in multiple website files. "
                "Please use a more specific edit request.",

            "files": [

                os.path.relpath(
                    path,
                    folder
                )

                for path in matches

            ]

        }

    path = matches[0]

    content = _safe_read_file(
        path
    )

    if content is None:

        return {

            "success": False,

            "message":
                "Unable to read the website source file."

        }

    # ------------------------------------------------------
    # REPLACE TEXT
    # ------------------------------------------------------

    occurrences = content.count(
        old_text
    )

    if occurrences == 0:

        return {

            "success": False,

            "message":
                "The requested text was not found in the website source."

        }

    if replace_all:

        updated_content = content.replace(
            old_text,
            new_text
        )

        replacements = occurrences

    else:

        updated_content = content.replace(
            old_text,
            new_text,
            1
        )

        replacements = 1

    # ------------------------------------------------------
    # SAVE FILE
    # ------------------------------------------------------

    if not _safe_write_file(
        path,
        updated_content
    ):

        return {

            "success": False,

            "message":
                "Unable to save website changes."

        }

    return {

        "success": True,

        "file":
            os.path.relpath(
                path,
                folder
            ),

        "replacements":
            replacements,

        "replace_all":
            bool(
                replace_all
            ),

        "message":
            "Website text updated successfully."

    }



# ==========================================================
# CSS APPEND
# ==========================================================

def append_css(
    folder,
    css
):

    if not css or not css.strip():

        return {

            "success": False,

            "message":
                "CSS content is required."

        }

    css_file = find_main_css_file(
        folder
    )

    if not css_file:

        return {

            "success": False,

            "message":
                "Main website CSS file was not found."

        }

    content = _safe_read_file(
        css_file
    )

    marker = (
        "\n\n/* Growth Radar AI Custom Styles */\n"
    )

    if marker.strip() in content:

        content += (
            "\n"
            + css.strip()
            + "\n"
        )

    else:

        content += (
            marker
            + css.strip()
            + "\n"
        )

    if not _safe_write_file(
        css_file,
        content
    ):

        return {

            "success": False,

            "message":
                "Unable to save CSS changes."

        }

    return {

        "success": True,

        "file":
            os.path.relpath(
                css_file,
                folder
            ),

        "message":
            "Website styling updated successfully."

    }


# ==========================================================
# WEBSITE EDIT SUMMARY
# ==========================================================

def get_edit_summary(
    folder
):

    source = read_website_source(
        folder
    )

    total_files = len(
        source
    )

    total_characters = sum(
        len(item["content"])
        for item in source
    )

    return {

        "success": True,

        "files":
            total_files,

        "characters":
            total_characters,

        "main_app":
            (
                os.path.relpath(
                    find_main_app_file(folder),
                    folder
                )
                if find_main_app_file(folder)
                else None
            ),

        "main_css":
            (
                os.path.relpath(
                    find_main_css_file(folder),
                    folder
                )
                if find_main_css_file(folder)
                else None
            )

    }


# ==========================================================
# EDIT WEBSITE
# ==========================================================

def edit_website(
    folder,
    operation,
    **kwargs
):

    if not folder:

        return {

            "success": False,

            "message":
                "Website folder is missing."

        }

    operation = str(
        operation or ""
    ).strip().lower()

    # ------------------------------------------------------
    # ALWAYS BACKUP BEFORE MODIFICATION
    # ------------------------------------------------------

    if operation in {
        "replace_text",
        "append_css"
    }:

        backup = create_website_backup(
            folder
        )

        if not backup.get(
            "success"
        ):

            return backup

    # ------------------------------------------------------
# REPLACE TEXT
# ------------------------------------------------------

    if operation == "replace_text":

        return replace_text(
            folder,
            kwargs.get("old_text"),
            kwargs.get("new_text"),
            replace_all=kwargs.get(
                "replace_all",
                False
        )
    )

    # ------------------------------------------------------
    # APPEND CSS
    # ------------------------------------------------------

    if operation == "append_css":

        return append_css(
            folder,
            kwargs.get("css")
        )

    # ------------------------------------------------------
    # SUMMARY
    # ------------------------------------------------------

    if operation == "summary":

        return get_edit_summary(
            folder
        )

    return {

        "success": False,

        "message":
            f"Unsupported website edit operation: {operation}"

    }