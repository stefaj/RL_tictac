with import <nixpkgs> {};
with pkgs.python27Packages;

buildPythonPackage{
    name = "numerai";
    buildInputs = [ python27Full
                    python27Packages.Keras
                    python27Packages.setuptools
                    python27Packages.pip
                    python27Packages.simplejson
                    python27Packages.numpy
                    python27Packages.h5py
                    python27Packages.pyopengl
                    python27Packages.scipy
                    python27Packages.matplotlib
                    mesa_glu
                    mesa
                    freeglut
                   ]; 


  shellHook = ''
  # set SOURCE_DATE_EPOCH so that we can use python wheels
  SOURCE_DATE_EPOCH=$(date +%s)
  export PATH=$PWD/venv/bin:$PATH
  '';
}

