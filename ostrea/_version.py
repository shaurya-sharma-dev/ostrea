"""
This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""

import subprocess

# Version info tuple in same format as sys.version_info.
__version_info__ = (1, 0, 0, "alpha", 1)

# The below code defines a function called _get_version_string. 
# The underscore is added to the beginning to signify that the function itself isn't part of the public API,
# though this is paired with del to ensure the namespace isn't cluttered.

def _get_version_string(version_info: tuple = __version_info__) -> str:
    # Get the major.minor.patch integers as a list of strings.
    _parsed_version_info = [str(x) for x in version_info[:3]]

    # This if condition runs on prereleases (alpha, beta, and release candidate).
    if version_info[3] != "final":
        # For prereleases, first map the prerelease string ("alpha", "beta", "candidate")
        # to its appropriate PEP 440 prerelease tag before appending the prerelease number to it.

        # Then, we append the prerelease tag and number (e.g. a1, b2, rc3) to the last list element.
        # We append it to the last list element instead of making its own list element because prereleases 
        # CANNOT be seperated by periods. So 1.2.3a4 is valid, but 1.2.3.a4 is not.
        _parsed_version_info[2] += {
            "alpha": "a", 
            "beta": "b", 
            "candidate": "rc",
            "final": ""
        }[version_info[3]] + str(version_info[4])

    # Join everything in the _parsed_version_info list while separating it with dots.
    return ".".join([str(x) for x in _parsed_version_info])

# Generate the PEP 440 compliant version string.
__version__ = _get_version_string()

# Get integrity from tag
def _get_version_integrity(target_version: str = __version__) -> bool|None:
    "Verifies if the current repository state exactly matches the target_version tag."
    try:
        # Get the commit hash of the target tag
        tag_commit = (
            subprocess.check_output(
                ["git", "rev-parse", f"{target_version}^{{commit}}"],
                stderr=subprocess.DEVNULL,
            )
            .decode()
            .strip()
        )

        # Get the commit hash of HEAD
        head_commit = (
            subprocess.check_output(["git", "rev-parse", "HEAD"])
            .decode()
            .strip()
        )

        # Compare the commit hashes
        if tag_commit != head_commit:
            # HEAD does not match the target_version tag's commit.
            return False

        # Check for uncommitted changes
        status_output = (
            subprocess.check_output(["git", "status", "--porcelain"])
            .decode()
            .strip()
        )

        if status_output:
            # Head matches but uncommited changes.
            return False

        # Repository state matches target_version.
        return True

    except subprocess.CalledProcessError:
        # Tag does not exist.
        return None

def _print_version_and_integrity():
    print(f"[INFO]: The current version is {__version__}.")
    integrity = _get_version_integrity()
    if integrity:
        print("[SUCCESS]: The current repository state matches the version.")
    else:
        if integrity is None:
            print("[ERROR]: The version tag does not exist.")
        else:
            print("[WARNING]: The current repository state does not match the current version. You may need to update it.")