with import <nixpkgs> {};
with pkgs.python3.pkgs;

{ lib,
  buildPythonPackage,
# build-system
  setuptools,
  setuptools-scm,
# dependencies
  survey,
# tests
# hypothesis
}:

buildPythonPackage rec {
  name = "filemanagement";
  #pname = "filemanagement";
  version = "0.0.1";

  # Requires ssh key
  #src = fetchFromGitHub { 
  #  owner = "yurimimi";
  #  repo = "${name}";
  #  rev = "cba327fe0e4d87beb30c2bb200f0470bb1082cad";
  #};
  src = ./src;

  #pyproject = true;
  #propagatedBuildInputs = [ pytest numpy pkgs.libsndfile ];
  
  dependencies = [
    survey
    # some others
  ];

  #meta = {
  #  changelog = "https://github.com/yurimimi/yui/releases/tag/${version}";
  #  description = "Your utility integrator";
  #  homepage = "https://github.com/yurimimi/yui";
  #  license = lib.licenses.mit;
  #  maintainers = with lib.maintainers; [ yurimimi ];
  #};
   
  #preConfigure = ''
  #  export LDFLAGS="-L${pkgs.fftw}/lib -L${pkgs.fftwFloat}/lib -L${pkgs.fftwLongDouble}/lib"
  #  export CFLAGS="-I${pkgs.fftw}/include -I${pkgs.fftwFloat}/include -I${pkgs.fftwLongDouble}/include"
  #'';
}
