# Make my feed great again (Twitter Bot Blocker)

## Introduction

A Selenium script, written in Python, that automatically blocks bots (users ending with 5 or more digits) in your Twitter's notification timeline.  
This script was created as a simple exercise to learn Selenium automation. It's designed to interact with Twitter's website and perform certain actions automatically.

**Please note:** This script should not be used by anyone as it may violate Twitter's rules. It's intended purely for educational purposes.

## Prerequisites

To run this script, you need:

- Python 3.6 or higher
- Selenium
- ChromeDriver

## Installation

1. Install Python from the official website.
2. Clone this repository to your local machine.
3. Navigate to the directory containing the script.
4. Install dependencies by running `pip install -r requirements.txt` in your terminal.

## Usage

1. Navigate to the directory containing the script.
2. Run the script using the command `python make_my_feed_great_again.py`.

The script provides three ways to enter your Twitter credentials:

1. Automatic mode: The script uses the Twitter handle and password saved in the code. To use this mode, run the script with the `--auto` flag.
2. Manual mode (script parameters): The script uses the Twitter handle and password provided as script parameters. To use this mode, run the script with the `--username` and `--password` flags followed by your Twitter handle and password.
3. Manual mode (prompts): The script prompts you to enter your Twitter handle and password each time it runs. To use this mode, run the script without any flags.

## Support

If you encounter any issues while using this script, please open an issue in this repository.

## Disclaimer

This script is intended for educational purposes only. It should not be used to interact with Twitter in a way that violates their rules. Please respect the terms of service of the websites you interact with.
