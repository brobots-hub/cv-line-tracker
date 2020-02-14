self: super: {

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

  ffmpeg_server = self.ffmpeg.overrideAttrs (old: {
    configureFlags = old.configureFlags ++ [
        (super.lib.enableFeature true "ffserver")
        (super.lib.enableFeature true "ffplay")
    ];          
  });
}
