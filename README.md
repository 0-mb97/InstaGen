# InstaGen: Automated Avatar Creation for Instagram

## Overview

Welcome to InstaGen, your go-to tool for automating the creation of avatars on Instagram! This project contributes to ongoing challenges in social networks during SwordWar, providing a vital tool for avatar generation and account setup. Linked with the [Instagram Signup Research Tool](https://github.com/0-mb97/Instagram_signup_research_tool.git), this project forms a comprehensive suite for research, analysis, and automation of Instagram-related tasks.


## Features

- Automated email sign-up
- Support for private proxies with authentication
- Automatic generation of all credentials
- Retrieval of verification codes from temporary email services
- Smooth handling of OpenVPN and proxy configurations
- Error handling and troubleshooting for a hassle-free experience

## Prerequisites

Before diving in, make sure you have the following essentials:


- **Python 3.x**
- [**ChromeDriver**](https://chromedriver.chromium.org/downloads) - Ensure the version matches your installed Google Chrome version to avoid compatibility issues.
- **OpenVPN file (.ovpn if applicable)**

## Installation and Usage

1. **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/instagram-avatar-automation.git
    ```

2. **Install Python dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3. **Run the script from the terminal:**

    ```bash
    python main.py -ov [path_to_ovpn_file] -r [root_password] -p [proxy_address]
    ```

    - `-ov` or `--ovpn_path`: Full path to the OpenVPN file
    - `-r` or `--root_passwd`: Root password (required for OpenVPN)
    - `-p` or `--proxy`: Proxy address and port (e.g., 127.0.0.1:8082) or private proxy in `user:pass@host:port` format.
## License:
   - Licensed under the MIT License.
   


## How to Contribute

Excited to contribute? We'd love to have you on board! Follow these steps:


1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and submit a pull request.

Feel free to reach out if you have any questions or suggestions. Happy coding!
