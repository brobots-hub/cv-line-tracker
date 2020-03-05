let
  pkgs = import <nixpkgs> {
    config = { };
    overlays = [
      (import ./deploy/config/line-tracker.local/etc/nixpkgs-overlay.nix)
    ];
  };

  recordclass = pkgs.python3.pkgs.buildPythonPackage rec {
    pname = "recordclass";
    version = "0.13.2";
    src = pkgs.python3.pkgs.fetchPypi {
      inherit pname version;
      sha256 = "3a65122155fffb0c6e8f329582b1b4474885dd8eecc901f1a589cafb260d5b37";
    };
    doCheck = false;
  };

  pythonEnv = pkgs.python3.withPackages (p: [
    p.opencv4
    p.numpy
    p.ipython # optional
    p.flask
    p.toml
  ]);

  pythonScreenEnv = pkgs.python3.withPackages (p: [
    p.opencv4
    p.numpy
    p.ipython
    p.xlib
    p.pillow
  ]);

  pythonRemoteEnv = pkgs.python3.withPackages (p: [
    p.ipython
    p.toml
    p.flask
    p.requests
    recordclass
    p.numpy
  ]);

in pkgs.mkShell {
  buildInputs = [
    pythonEnv

    pkgs.git-secret
    pkgs.gnupg # required for git-secret

    # for ffserver and ffplay - they are absent in pkgs.ffmpeg
    #pkgs.ffmpeg-full
  ];
} // {
  inherit pkgs;

  videoShell = pkgs.mkShell {
    buildInputs = [ pkgs.ffmpeg_server ];
  };

  screenShell = pkgs.mkShell {
    buildInputs = [
      pythonScreenEnv
      pkgs.openscad
    ];
  };

  remoteShell = pkgs.mkShell {
    buildInputs = [
      pythonRemoteEnv
    ];
  };
}
