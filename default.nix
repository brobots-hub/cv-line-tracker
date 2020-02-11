let
  pkgs = import <nixpkgs> {
    config = { };
    overlays = [
      (self: super: {
        opencv4 = super.opencv4.override {
          pythonPackages = self.python3.pkgs;
          enablePython = true;
          enableGtk2 = true;
          enableFfmpeg = true;
          enableTesseract = true; # optional
        };
        python3 = super.python3.override {
          packageOverrides = pythonself: pythonsuper: {
            opencv4 = pythonsuper.toPythonModule self.opencv4;
          };
        };
      })
    ];
  };

  pythonEnv = pkgs.python3.withPackages (p: [
    p.opencv4
    p.numpy
    p.ipython # optional
    p.flask
    p.toml
  ]);

in pkgs.mkShell {
  buildInputs = [
    pythonEnv

    pkgs.git-secret
    pkgs.gnupg # required for git-secret

    # for ffserver and ffplay - they are absent in pkgs.ffmpeg
    pkgs.ffmpeg-full
  ];
} // {
  inherit pkgs;
}
