# Copyright 2025 Braden Ganetsky
# Distributed under the Boost Software License, Version 1.0.
# https://www.boost.org/LICENSE_1_0.txt

import datetime
from pathlib import Path
from get_install_args import scrape_bootstrappers

def main():
    bootstrappers = (
        scrape_bootstrappers(16) |
        scrape_bootstrappers(17) |
        scrape_bootstrappers(18)
    )

    script_dir = Path(__file__).resolve().parent
    out_path = script_dir / "generated/bootstrappers.py"
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)

    with open(out_path, "w") as file:
        timestamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")
        file.write(f"# Generated on {timestamp}\n")
        file.write("bootstrappers = {\n")
        for k,v in bootstrappers.items():
            file.write(f"""    "{k}": "{v}",\n""")
        file.write("}\n")

if __name__ == "__main__":
    main()
