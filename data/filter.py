import io
import zstandard as zstd
from tqdm import tqdm

with open("RC_2019-09.zst", 'rb') as fh:
    dctx = zstd.ZstdDecompressor()
    stream_reader = dctx.stream_reader(fh)
    text_stream = io.TextIOWrapper(stream_reader, encoding='utf-8')
    with open("output.json", "w") as oh:
        for line in tqdm(text_stream):
            if 'The_Donald' in line or 'SandersForPresident' in line:
                oh.write(line)
