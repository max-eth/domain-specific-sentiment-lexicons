import io
import zstandard as zstd
from tqdm import tqdm
import json
import argparse
import os


parser = argparse.ArgumentParser(description="Filter a reddit data-dump")
parser.add_argument(
    "dump_filename", help="the filename of the data-dump. Needs to be in zst format."
)
parser.add_argument("subreddits", nargs="+", help="the subreddits to filter out")

args = parser.parse_args()

for sub in args.subreddits:
    os.makedirs(sub, exist_ok=True)
outfiles = {
    sub: open(os.path.join(sub, "outputs.json"), "w")
    for sub in args.subreddits
}

with open(args.dump_filename, "rb") as fh:
    dctx = zstd.ZstdDecompressor()
    stream_reader = dctx.stream_reader(fh)
    text_stream = io.TextIOWrapper(stream_reader, encoding="utf-8")
    for line in tqdm(text_stream):
        outfiles[json.loads(line)['subreddit']].write(line)

for outfile in outfiles.values():
    outfile.close()
