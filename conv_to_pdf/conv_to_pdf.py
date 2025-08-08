import os
import sys
from fpdf import FPDF
from markdown_pdf import Section, MarkdownPdf


def convert_to_pdf(input_file, output_file):
    """
    Convertit un fichier .txt ou .md en .pdf.
    Args:
        input_file (str): Le chemin vers le fichier d'entrée (.txt ou .md).
        output_file (str): Le chemin vers le fichier de sortie .pdf.
    """
    file_extension = os.path.splitext(input_file)[1].lower()

    if file_extension == '.txt':
        convert_txt_to_pdf(input_file, output_file)
    elif file_extension == '.md':
        convert_md_to_pdf(input_file, output_file)
    else:
        print(
            f"Erreur : L'extension de fichier '{file_extension}' n'est pas "
            "prise en charge. Seuls les .txt et .md sont acceptés."
        )
        return
    print(
        f"Le fichier '{input_file}' a été converti avec succès en "
        f"'{output_file}'"
    )


def convert_txt_to_pdf(input_file, output_file):
    """
    Convertit un fichier texte en PDF en utilisant fpdf2.
    """
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            pdf.multi_cell(0, 10, txt=line)

    pdf.output(output_file)


def convert_md_to_pdf(input_file, output_file):
    """
    Convertit un fichier Markdown en PDF en utilisant markdown-pdf.
    """
    pdf = MarkdownPdf()
    
    with open(input_file, 'r', encoding='utf-8') as f:
        markdown_content = f.read()

    pdf.add_section(Section(markdown_content))
    pdf.save(output_file)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(
            "Usage: python convert_to_pdf.py <fichier_entree> "
            "<fichier_sortie.pdf>"
        )
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    if not os.path.exists(input_path):
        print(
            f"Erreur : Le fichier d'entrée '{input_path}' n'a pas été trouvé."
        )
        sys.exit(1)

    if os.path.splitext(output_path)[1].lower() != '.pdf':
        print("Erreur : Le fichier de sortie doit avoir une extension .pdf.")
        sys.exit(1)

    convert_to_pdf(input_path, output_path)