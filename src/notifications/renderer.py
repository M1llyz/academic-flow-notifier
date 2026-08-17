from pathlib import Path


TEMPLATE_DIR = Path("src/templates/email")


def read_template(file_name: str) -> str:
    """
    Lê um arquivo de template da pasta templates/email.
    """

    file_path = TEMPLATE_DIR / file_name

    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


def render_email(
    subject: str,
    content_html: str,
    content_text: str,
) -> tuple[str, str]:
    """
    Renderiza o e-mail completo nas versões HTML e texto.
    """

    styles = read_template("styles.css")

    html_template = read_template("notification.html")
    text_template = read_template("notification.txt")

    signature_html = read_template("signature.html")
    signature_text = read_template("signature.txt")

    body_html = (
        html_template
        .replace("{{ styles }}", styles)
        .replace("{{ subject }}", subject)
        .replace("{{ body }}", content_html)
        .replace("{{ signature }}", signature_html)
    )

    body_text = (
        text_template
        .replace("{{ subject }}", subject)
        .replace("{{ body }}", content_text)
        .replace("{{ signature }}", signature_text)
    )

    return body_html, body_text