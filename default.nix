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
                            enableTesseract = true;
                        });
                    };
                };
            })
      ];
  };

  pythonEnv = pkgs.python3.withPackages (p: [
      p.opencv4
      p.ipython
      p.numpy
  ]);

in {
    shell = pkgs.mkShell {
        buildInputs = [
            pythonEnv
            pkgs.git-secret
        ];
    };
}