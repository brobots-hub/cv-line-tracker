let
  pkgs = import <nixpkgs> {
      config = {};
      overlays = [
            (self: super: {
                python3 = super.python3.override {
                    packageOverrides = pythonself: pythonsuper: {
                        opencv4 = pythonsuper.toPythonModule (self.opencv4.override {
                            pythonPackages = pythonself;
                            enablePython = true;
                            enableGtk2 = true;
                            enableFfmpeg = true;
                            enableTesseract = true; # optional
                        });
                    };
                };
            })
      ];
  };

  pythonEnv = pkgs.python3.withPackages (p: [
      p.opencv4
      p.numpy
      p.ipython  # optional
  ]);

in {
    shell = pkgs.mkShell {
        buildInputs = [
            pythonEnv

            pkgs.git-secret
            pkgs.gnupg # required for git-secret

            # for ffserver and ffplay - they are absent in pkgs.ffmpeg
            pkgs.ffmpeg-full
        ];
    };
}