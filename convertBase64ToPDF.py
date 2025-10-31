from pathlib import Path
import base64
from typing import Optional, Union
import argparse

def decode_base64_file_to_pdf(input_file: Union[str, Path], output_file: Optional[Union[str, Path]] = None) -> Path:
    """
    Read a text file containing a Base64-encoded PDF (optionally a data URL prefix),
    decode it and save as a .pdf file. Returns the Path to the written PDF.

    Args:
        input_file: Path to the text file containing base64 string.
        output_file: Optional path for the output PDF. If not provided, same name as input with .pdf extension.

    Raises:
        ValueError: If decoding fails or input file is empty.
        FileNotFoundError: If input_file does not exist.
    """
    input_path = Path(input_file)
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    text = input_path.read_text(encoding="utf-8").strip()
    if not text:
        raise ValueError("Input file is empty")

    # If the base64 string is embedded in a data URL like: data:application/pdf;base64,...
    if "base64," in text:
        text = text.split("base64,", 1)[1]

    # Remove whitespace/newlines which may be present
    b64 = "".join(text.split())

    try:
        pdf_bytes = base64.b64decode(b64, validate=True)
    except Exception as exc:
        raise ValueError("Failed to decode base64 content") from exc

    if output_file:
        out_path = Path(output_file)
    else:
        out_path = input_path.with_suffix(".pdf")

    out_path.write_bytes(pdf_bytes)
    return out_path


if __name__ == "__main__":
    saved = decode_base64_file_to_pdf('base64.txt', 'output.pdf')
    print(f"Saved PDF to: {saved}")
