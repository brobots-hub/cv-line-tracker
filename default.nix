let
  pkgs = import <nixpkgs> {
    config = { };
    overlays = [
      (import ./deploy/config/line-tracker.local/etc/nixpkgs-overlay.nix)
    ];
  };

  pythonEnv = pkgs.python3.withPackages (p: [
    p.opencv4
    p.numpy
    p.ipython # optional
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
}
