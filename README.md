# Computer Vision Line Tracker

# Setup

## Windows

We assume you have WSL, though most of this stuff will work with MSYS2 (or Git-bash).

- Install [Chocolatey](https://chocolatey.org/)
- `choco install ./packages.config`
  * `git-bash` is required if you want automated flashing of Raspbian image. It is optional if you flash Raspbian with Etcher
  * `vcxsrv` is required to show GUI windows from WSL
    * launch using `Xlaunch` and select "server-only" radiobutton
    * add to your `~/.bashrc` in WSL:
        ```
        export DISPLAY=:0
        ```
- in WSL run:
    ```
    sudo apt-get install -y \
        git-secret \
        python3
    ```
- TODO: avahi/bonjour

## Linux

- install [Nix multi-user](https://nixos.org/nix/manual/#sect-multi-user-installation)
- enter dev-shell with
    ```
    nix-shell -A shell
    ```