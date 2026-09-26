import urllib.request
import urllib.error
import json
import argparse
import sys
import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_WEBHOOK_URL = os.environ["DISCORD_WEBHOOK_URL"]


def send_message(text: str) -> None:
    try:
        payload = json.dumps({'content': text, 'flags': 4}).encode('utf-8')

        req = urllib.request.Request(
            DISCORD_WEBHOOK_URL,
            data=payload,
            headers={
                'Content-Type': 'application/json',
                'User-Agent': 'Mozilla/5.0'
            }
        )

        with urllib.request.urlopen(req) as response:
            print(f"Response status: {response.status}")

    except urllib.error.HTTPError as error:
        print(f"HTTP Error: {error.code} - {error.reason}")
        raise error
    except Exception as error:
        print(f"Unexpected error: {error}")
        raise error


def validate_split(text: str) -> None:
    """Ïmprove this section to actually make it useful"""
    print("Message chunk validated successfully (dry-run)")




if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Send Markdown newsletter chunks to Discord via webhook")
    parser.add_argument("file", help="Path to the Markdown file")
    parser.add_argument(
        "--validate-split",
        action="store_true",
        help="Validate chunk splitting without sending messages to Discord"
    )
    args = parser.parse_args()

    file_path = args.file
    dispatch_fn = validate_split if args.validate_split else send_message

    try:
        with open(file_path, 'r', encoding='utf-8') as source_file:
            extracted_text = source_file.read()

            raw_chunks = extracted_text.replace('[MESSAGE_BREAK]', '[QUEBRA_MENSAGEM]').split('[QUEBRA_MENSAGEM]')
            error_chunks = []

            for i, raw_chunk in enumerate(raw_chunks):
                clean_chunk = raw_chunk.strip()

                if not clean_chunk:
                    continue

                if len(clean_chunk) > 1950:
                    error_chunks.append(i)
                    char_chunks = [clean_chunk[j:j+1950] for j in range(0, len(clean_chunk), 1950)]
                    for sub_chunk in char_chunks:
                        dispatch_fn(sub_chunk)
                        print(f"Chunk sliced by character limit: {sub_chunk[:40]}...")
                else:
                    dispatch_fn(clean_chunk)
                    print(f"Chunk sliced by delimiter: {clean_chunk[:40]}...")

            if args.validate_split and error_chunks:
                print(f"Chunks exceeding character limit: {error_chunks}")
                sys.exit(1)
            else:
                print("Newsletter successfully processed and sent in chunks!")

    except FileNotFoundError:
        print(f"File not found: {file_path}")
        sys.exit(1)
    except Exception as error:
        print(f"Unexpected error: {error}")
        raise error
