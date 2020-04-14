import io
import zstandard as zstd
from tqdm import tqdm

import argparse


parser = argparse.ArgumentParser(description="Filter a reddit data-dump")
parser.add_argument(
    "dump_filename", help="the filename of the data-dump. Needs to be in zst format."
)
parser.add_argument(
    "subreddits", nargs="+", help="the subreddits to filter out"
)

args = parser.parse_args()
outname = "outputs_" + "_".join(args.subreddits) + ".json"
print("Writing to", outname)

with open(args.dump_filename, "rb") as fh:
    dctx = zstd.ZstdDecompressor()
    stream_reader = dctx.stream_reader(fh)
    text_stream = io.TextIOWrapper(stream_reader, encoding="utf-8")
    with open(outname, "w") as oh:
        for line in tqdm(text_stream):
            for sub in args.subreddits:
                if sub in line:
                    oh.write(line)
                    break
