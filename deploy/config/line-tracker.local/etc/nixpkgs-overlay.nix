self: super: {

  opencv4_custom = super.opencv4.override {
    pythonPackages = self.python3.pkgs;
    enablePython = true;
    enableGtk2 = true;
    enableFfmpeg = true;
    enableTesseract = true; # optional
  };

  python3 = super.python3.override {
    packageOverrides = pythonself: pythonsuper: {

      opencv4_custom = pythonsuper.toPythonModule self.opencv4_custom;

      recordclass = pythonsuper.buildPythonPackage rec {
        pname = "recordclass";
        version = "0.13.2";
        src = pythonsuper.fetchPypi {
          inherit pname version;
          sha256 = "3a65122155fffb0c6e8f329582b1b4474885dd8eecc901f1a589cafb260d5b37";
        };
        doCheck = false;
      };

      picamera = pythonsuper.buildPythonPackage rec {
        pname = "picamera";
        version = "1.13";
        src = super.fetchFromGitHub {
          owner = "waveform80";
          repo = "picamera";
          rev = "93a0808b8a4a22c848958385818b6ed26955216f";
          sha256 = "0p043j5nihmqqg69z1ks4x0q9gxlj160l6z2vwnwd24nff8ziazv";
        };
        patches = [ (super.fetchpatch {
          url = "https://github.com/danbst/picamera/commit/8a32a06c8cbd61d4c02fd72b60a9e2dd910e7e3d.patch";
          sha256 = "1d0l0wzc14741jxgwfchbz7mpw0l6bv862k6xp56y0mdxlf9zxvl"; })
        ];
        doCheck = false;
      };

      rpi_gpio = pythonsuper.buildPythonPackage rec {
        pname = "RPi.GPIO";
        version = "0.7.0";
        src = pythonsuper.fetchPypi {
          inherit pname version;
          sha256 = "7424bc6c205466764f30f666c18187a0824077daf20b295c42f08aea2cb87d3f";
        };
        doCheck = false;
      };

      colorzero = pythonsuper.buildPythonPackage rec {
        pname = "colorzero";
        version = "1.1";
        src = pythonsuper.fetchPypi {
          inherit pname version;
          sha256 = "acba47119b5d8555680d3cda9afe6ccc5481385ccc3c00084dd973f7aa184599";
        };
        doCheck = false;
      };
      
      gpiozero = pythonsuper.buildPythonPackage rec {
        pname = "gpiozero";
        version = "1.5.1";
        src = pythonsuper.fetchPypi {
          inherit pname version;
          sha256 = "ae1a8dc4e6e793ffd8f900968f3290d218052c46347fa0c0503c65fabe422e4d";
        };
        doCheck = false;
        buildInputs = with pythonself; [ colorzero ];
      };
      
    };
  };


  raspberrypi-tools = super.raspberrypi-tools.overrideAttrs (old: {
    src = super.fetchFromGitHub {
      owner = "raspberrypi";
      repo = "userland";
      rev = "6e6a2c859a17a195fbb6a97c9da584dd2b9b0178";
      sha256 = "0r0zzvxvkb5yvzm6k74slp53q3gahci7a4gjdqgdbmx1gp8awwq4";
    };
    patches = [];
  });

  pythonRemoteEnv = (self.python3.withPackages (p: [
    p.ipython
    p.toml
    p.flask
    p.flask-cors
    p.requests
    p.recordclass
    p.numpy
    p.picamera
    p.opencv4
    p.gpiozero
    p.rpi_gpio
    p.colorzero
  ])).override {
    makeWrapperArgs = if builtins.currentSystem != "x86_64-linux" then [ 
      "--prefix LD_LIBRARY_PATH : ${self.raspberrypi-tools}/lib"
    ] else [];
  };

  ffmpeg_server = self.ffmpeg.overrideAttrs (old: {
    configureFlags = old.configureFlags ++ [
        (super.lib.enableFeature true "ffserver")
        (super.lib.enableFeature true "ffplay")
    ];          
  });
}
