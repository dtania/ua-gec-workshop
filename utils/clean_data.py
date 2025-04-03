#!/usr/bin/env python3
"""Download and clean text or .m2 files.

How to use:
    clean_data.py (-h | --help)
    For a text file:
        python clean_data.py --type txt --url "http://example.com/data.txt" --output cleaned.txt --num 100
    For an m2 file:
        python clean_data.py --type m2 --url "http://example.com/data.m2" --output cleaned.m2 --num 100

Options:
    --type: Choose the file type: txt for plain text files or m2 for annotation files.
    --url: The URL from which to download the file.
    --output: The filename/path where the cleaned data will be saved.
    --num: The number of sentences (for text files) or annotation blocks (for m2 files) to extract (default is 200).

"""

import argparse
import re
import requests
import sys


def download_file(url):
    """Download and return the content of a file from a given URL.

    Returns:
        str: Content of the file if request is successful.
    Raises:
        SystemExit: If the request fails.
    """
    try:
        response = requests.get(url)
        response.encoding = 'utf-8'
    except Exception as e:
        sys.exit(f"Error during downloading: {e}")

    if response.status_code == 200:
        return response.text
    else:
        sys.exit(f"Failed to download file. Status code: {response.status_code}")


def clean_text(content, num_sentences):
    """Extract text lines from content, removing lines matching a document ID.

    Lines with the pattern "# 0005" are removed.

    Args:
        content (str): The downloaded text content.
        num_sentences (int): The maximum number of valid sentences to return.

    Returns:
        list[str]: A list of cleaned sentences.
    """
    pattern = re.compile(r"^#[\d\s]+$")
    sentences = content.splitlines()
    # Filter and limit by num_sentences
    return [line for line in sentences if not pattern.match(line)][:num_sentences]


def clean_m2(content, num_blocks):
    """Process .m2 content by grouping lines into annotated blocks,
    filtering out blocks starting with unwanted document ID lines.

    Args:
        content (str): The downloaded m2 file content.
        num_blocks (int): The maximum number of blocks to return.

    Returns:
        list[list[str]]: A list of blocks, each a list of lines.
    """
    blocks = []
    current_block = []
    for line in content.splitlines():
        if line.startswith("S "):
            if current_block:
                blocks.append(current_block)
            current_block = [line]
        else:
            current_block.append(line)
    if current_block:
        blocks.append(current_block)

    # Remove blocks whose first line is a document id pattern (e.g., "S #0005")
    pattern = re.compile(r"^S #[\d\s]+$")
    filtered_blocks = [block for block in blocks if not pattern.match(block[0])]
    return filtered_blocks[:num_blocks]


def write_output(lines_or_blocks, output_filename, is_block=False):
    """Write cleaned lines or blocks to the given output file.

    Args:
        lines_or_blocks (list): List of strings or list of blocks (each block is a list of strings).
        output_filename (str): Path to the output file.
        is_block (bool): Indicates if lines_or_blocks is grouped in blocks (m2 file).
    """
    with open(output_filename, "w", encoding="utf-8") as f:
        if is_block:
            # Write block by block with an additional newline in between.
            for block in lines_or_blocks[:-1]:
                f.write("\n".join(block) + "\n")
            f.write("\n".join(lines_or_blocks[-1]))
        else:
            f.write("\n".join(lines_or_blocks))


def main():
    parser = argparse.ArgumentParser(description="Download and clean text or m2 files.")
    parser.add_argument("--type", choices=["txt", "m2"], required=True,
                        help="Type of file to clean: txt or m2")
    parser.add_argument("--url", required=True, help="URL of the file to download")
    parser.add_argument("--output", required=True, help="Output filename to write cleaned data")
    parser.add_argument("--num", type=int, default=200,
                        help="Number of sentences (for txt) or blocks (for m2) to extract. Default is 200.")
    args = parser.parse_args()

    content = download_file(args.url)

    if args.type == "txt":
        cleaned = clean_text(content, args.num)
        write_output(cleaned, args.output)
    elif args.type == "m2":
        blocks = clean_m2(content, args.num)
        write_output(blocks, args.output, is_block=True)
    else:
        sys.exit("Invalid file type selected.")


if __name__ == "__main__":
    main()
