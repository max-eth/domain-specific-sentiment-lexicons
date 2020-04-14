import io
import zstandard as zstd
from tqdm import tqdm

import argparse
import os


parser = argparse.ArgumentParser(description="Filter a reddit data-dump")
parser.add_argument(
    "dump_filename", help="the filename of the data-dump. Needs to be in zst format."
)
parser.add_argument("subreddits", nargs="+", help="the subreddits to filter out")

args = parser.parse_args()

prefix = os.path.join("data", "subreddits")
print("Writing to {} ...".format(prefix))

os.makedirs(prefix)
outfiles = {
    sub: open(os.path.join(prefix, "outputs_" + sub + ".json"), "w")
    for sub in args.subreddits
}

with open(args.dump_filename, "rb") as fh:
    dctx = zstd.ZstdDecompressor()
    stream_reader = dctx.stream_reader(fh)
    text_stream = io.TextIOWrapper(stream_reader, encoding="utf-8")
    for line in tqdm(text_stream):
        for sub, oh in outfiles.items():
            if sub in line:
                oh.write(line)

for outfile in outfiles.values():
    outfile.close()
