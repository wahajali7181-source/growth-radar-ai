import os
import streamlit as st


def get_preview_files(folder):
    """
    Return generated website files.
    """

    if not folder:
        return []

    if not os.path.exists(folder):
        return []

    files = []

    for root, _, filenames in os.walk(folder):

        for filename in filenames:

            path = os.path.join(
                root,
                filename
            )

            relative = os.path.relpath(
                path,
                folder
            )

            files.append(relative)

    return sorted(files)


def read_preview_file(folder, relative_path):
    """
    Safely read a generated website file.
    """

    if not folder or not relative_path:
        return None

    base_path = os.path.abspath(folder)

    full_path = os.path.abspath(
        os.path.join(
            base_path,
            relative_path
        )
    )

    # Prevent path traversal.
    if not full_path.startswith(
        base_path + os.sep
    ):
        return None

    if not os.path.isfile(full_path):
        return None

    try:

        with open(
            full_path,
            "r",
            encoding="utf-8"
        ) as file:

            return file.read()

    except Exception:

        return None


def show_preview(folder):
    """
    Display generated website project preview.
    """

    st.subheader(
        "👁 Website Preview"
    )

    if not folder:

        st.info(
            "Generate a website first."
        )

        return

    if not os.path.exists(folder):

        st.error(
            "Generated website project was not found."
        )

        return

    files = get_preview_files(
        folder
    )

    if not files:

        st.warning(
            "No generated website files found."
        )

        return

    st.success(
        "✅ Generated website project is ready."
    )

    st.caption(
        f"Project: `{folder}`"
    )

    st.write(
        f"Generated files: **{len(files)}**"
    )

    # ==========================================================
    # LIVE PREVIEW
    # ==========================================================

    st.markdown(
        "### 🌐 Live Website"
    )

    st.info(
        "The generated website can be opened using its local Vite server."
    )

    preview_url = "http://localhost:5173"

    st.link_button(
        "🚀 Open Live Website",
        preview_url,
        use_container_width=True
    )

    st.caption(
        "Make sure `npm run dev` is running inside the generated website folder."
    )

    st.divider()

    # ==========================================================
    # FILE SELECTOR
    # ==========================================================

    safe_key = (
        "website_preview_file_"
        + folder.replace("\\", "_")
        .replace("/", "_")
        .replace(" ", "_")
        .replace(":", "")
    )

    selected_file = st.selectbox(
        "Select generated file",
        files,
        key=safe_key
    )

    if selected_file:

        content = read_preview_file(
            folder,
            selected_file
        )

        if content is not None:

            extension = os.path.splitext(
                selected_file
            )[1].lower()

            language = "text"

            if extension in [
                ".jsx",
                ".js"
            ]:

                language = "javascript"

            elif extension == ".css":

                language = "css"

            elif extension == ".html":

                language = "html"

            elif extension == ".json":

                language = "json"

            st.code(
                content,
                language=language
            )

        else:

            st.error(
                "Unable to read selected file."
            )

    st.divider()

    st.success(
        "🟢 Website project is ready for local preview."
    )