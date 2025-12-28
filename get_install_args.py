# Copyright 2025 Braden Ganetsky
# Distributed under the Boost Software License, Version 1.0.
# https://www.boost.org/LICENSE_1_0.txt

import argparse
import re
import sys
import urllib.request
from pathlib import Path

def fetch_html(url: str) -> str:
    response = urllib.request.urlopen(url)
    return response.read().decode('utf-8')

def extract_bootstrappers(html: str) -> dict:
    # This pattern matches the version-specific URLs to the build tools.
    # The format is different between 2019 and 2022/2026, but this works for both formats.
    pattern = r"""<td>(\d{2}\.\d{1,2}\.\d{1,2})</td>.*?<a href="([^"]*?vs_[Bb]uild[Tt]ools\.exe)".*?>(?:<u>)?Build ?Tools(?:</u>)?</a></td>"""

    matches = re.findall(pattern, html, re.DOTALL)
    assert len(matches) > 0

    # Some versions have 2 URLs, one under "LTSC" and the other under "current".
    # We only need to keep 1 of those URLs, so we keep the first one that appears.
    # They always appear in adjacent entries.
    dedup = []
    for i in range(len(matches)):
        a = matches[i]
        b = matches[i-1]
        if i == 0 or (a[0] != b[0]):
            dedup.append(a)
    matches = dedup

    return {m[0]: m[1] for m in matches}

def scrape_bootstrappers_2019() -> dict:
    # Check a few versions as a heuristic
    bootstrappers : dict = extract_bootstrappers(fetch_html("https://learn.microsoft.com/en-us/visualstudio/releases/2019/history"))
    assert "16.0.0" in bootstrappers
    assert "16.3.1" in bootstrappers
    assert "16.8.7" in bootstrappers
    assert "16.10.0" in bootstrappers
    assert "16.11.53" in bootstrappers
    assert "16.11.53" in bootstrappers
    return bootstrappers

def scrape_bootstrappers_2022() -> dict:
    # Check a few versions as a heuristic
    bootstrappers : dict = extract_bootstrappers(fetch_html("https://learn.microsoft.com/en-us/visualstudio/releases/2022/release-history"))
    assert "17.0.0" in bootstrappers
    assert "17.2.20" in bootstrappers
    assert "17.7.5" in bootstrappers
    assert "17.13.3" in bootstrappers
    assert "17.14.23" in bootstrappers
    return bootstrappers

def scrape_bootstrappers_2026() -> dict:
    # Check a few versions as a heuristic
    bootstrappers : dict = extract_bootstrappers(fetch_html("https://learn.microsoft.com/en-us/visualstudio/releases/2026/release-history"))
    assert "18.0.0" in bootstrappers
    assert "18.1.1" in bootstrappers
    return bootstrappers

def scrape_bootstrappers(major: int) -> dict:
    assert major in [16, 17, 18]
    if major == 16:
        return scrape_bootstrappers_2019()
    elif major == 17:
        return scrape_bootstrappers_2022()
    else: # major == 18
        return scrape_bootstrappers_2026()

class Version:
    def __init__(self, version: str):
        given_version = re.match(r"^(\d+)\.(\d+)(?:\.(\d+))?$", version)
        if not given_version:
            self.error = f"Given version does not match format major.minor[.patch]: {version}"
            return

        captures = given_version.groups()

        major = captures[0]
        if major not in ["16", "17", "18"]:
            self.error = f"Given major version is not in [16, 17, 18]: {major}"
            return

        bootstrappers = scrape_bootstrappers(int(major))

        minor = captures[1]
        possible_versions = [v for v in bootstrappers if v.startswith(f"{major}.{minor}")]
        if len(possible_versions) == 0:
            self.error = f"Given minor version does not exist: {major}.{minor}"
            return

        patch = captures[2]
        possible_patches = [re.match(r"^.*\.(\d+)$", v).group(1) for v in possible_versions]
        if patch is None:
            patch = sorted([int(p) for p in possible_patches])[-1]
        else:
            patch = captures[2]
            if patch not in possible_patches:
                self.error = f"Given version does not exist: {major}.{minor}.{patch}"
                return

        self.major = int(major)
        self.minor = int(minor)
        self.patch = int(patch)
        self.bootstrapper = bootstrappers[f"{self}"]

    def is_valid(self) -> bool:
        return not hasattr(self, "error")

    def __str__(self):
        if self.is_valid():
            return f"{self.major}.{self.minor}.{self.patch}"
        else:
            return self.error

def buildtools_component_id(v: Version) -> str:
    assert v.major in [16, 17, 18]
    assert v.minor >= 0
    assert v.patch >= 0

    if v.major == 18:
        number = f"14.{v.minor+50}.18.{v.minor}"
    elif v.major == 17:
        assert v.minor <= 14
        number = f"14.{v.minor+30}.17.{v.minor}"
    elif v.major == 16:
        assert v.minor <= 11
        if v.minor in [10, 11]:
            number = f"14.29.16.{v.minor}"
        elif v.minor in [8, 9]:
            number = f"14.28.16.{v.minor}"
        else: # v.minor <= 7
            number = f"14.2{v.minor}.16.{v.minor}"

    return f"Microsoft.VisualStudio.Component.VC.{number}.x86.x64"

def main():
    parser = argparse.ArgumentParser(
        description="Grab the Visual Studio Build Tools bootstrapper and the installer components, for a given version"
    )
    parser.add_argument("vs_version", help="The Visual Studio version, {16|17|18}.minor[.patch]")
    args = parser.parse_args()

    version = Version(args.vs_version)
    if not version.is_valid():
        print(version, file=sys.stderr)
        exit(1)

    # Outputs of the script
    print(version)
    print(version.bootstrapper)
    print(buildtools_component_id(version))

if __name__ == "__main__":
    main()
