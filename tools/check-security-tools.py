#!/usr/bin/env python3
import argh
import emoji
import requests

from string import Template

DOCUMENTATION_PATH = "../docs/repositories/security-monitor.md"
ENDPOINT_URL_TOOLS = "https://api.codacy.com/api/v3/tools"
ENDPOINT_URL_CODE_PATTERNS = Template("https://api.codacy.com/api/v3/tools/${toolUuid}/patterns")
IGNORED_TOOL_UUIDS = ["647dddc1-17c4-4840-acea-4c2c2bbecb45", # Codacy Scalameta Pro
                      "31677b6d-4ae0-4f56-8041-606a8d7a8e61", # Pylint 2 (Python 3)
                      "cf05f3aa-fd23-4586-8cce-5368917ec3e5"] # ESLint 7 (deprecated)


def check_security_tools():
    print("Checking if each tool that detects security issues is included in the documentation:\n")
    with open(DOCUMENTATION_PATH, "r") as file:
        documentation = file.read().lower()
    tools = requests.get(ENDPOINT_URL_TOOLS).json()["data"]
    count = 0
    for tool in tools:
        if tool["uuid"] in IGNORED_TOOL_UUIDS:
            continue
        tool_name = tool["name"]
        tool_short_name = tool["shortName"]
        tool_languages = tool["languages"]
        code_patterns = requests.get(ENDPOINT_URL_CODE_PATTERNS.substitute(toolUuid=tool["uuid"])).json()["data"]
        for code_pattern in code_patterns:
            if code_pattern["category"] == "Security":
                if tool_name.lower() in documentation or tool_short_name.lower() in documentation:
                    print(emoji.emojize(f":check_mark_button: {tool_name} is included "
                                        f"({', '.join(map(str, tool_languages))})"))
                else:
                    print(emoji.emojize(f":cross_mark: {tool_name} ISN'T included "
                                        f"({', '.join(map(str, tool_languages))})"))
                    count += 1
                break
    if count:
        print(f"\nFound {count} tools that aren't included in the documentation.")
        exit(1)
    else:
        print(emoji.emojize("\nAll tools are included in the documentation! :party_popper:"))
        exit(0)


argh.dispatch_command(check_security_tools)
