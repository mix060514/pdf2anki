# PDF2Anki

PDF2Anki is a tool that helps you convert PDF files into Anki flashcards efficiently. It is designed to assist students and learners in creating study materials from their PDF documents.

## Features

- Extract text and images from PDF files
- Convert PDF content into Anki-compatible flashcards
- Support for maintaining image references
- Custom field mapping for Anki cards

## Installation

1. Clone this repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Place your PDF file in the input directory
2. Run the conversion script:
```bash
python pdf2anki.py --input your_file.pdf --output cards.txt
```
3. Import the generated file into Anki

## Configuration

The tool supports customization through a config file:

- `image_dir`: Directory for extracted images
- `fields`: Custom field mapping for Anki cards
- `template`: Card template selection

## Dependencies

- Python 3.7+
- pdfminer
- pillow
- genanki

## License

MIT License
