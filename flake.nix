{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/e6f23dc08d3624daab7094b701aa3954923c6bbb";  # python 3.12.10
    flake-utils.url = "github:numtide/flake-utils";
    nur = {
      url = "github:hexadecimalDinosaur/nur";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = { nixpkgs, flake-utils, nur, ... }:
  {
    nixConfig = {
      extra-substituters = [
        "https://hexadecimaldinosaur.cachix.org"
      ];
      extra-trusted-public-keys = [
        "hexadecimaldinosaur.cachix.org-1:793qwEYh8UCmiTHMSFkz1/mu8mRDC7VCr7xI7e8M8s8="
      ];
    };
  } //
  flake-utils.lib.eachDefaultSystem (
    system:
    let
      pkgs = (import nixpkgs {
        inherit system;
        overlays = [ nur.overlays.python ];
      });
      python-env = (pkgs.python312.withPackages (p: with p; [
        requests
        xdis
        uncompyle6
        decompyle3
        x-python
        xasm
        pyinstxtractor-ng
        dearpygui

        jupyter
        ipython
        jupyter
        rich

        # dev tools
        pip
        autopep8
        flake8
        isort
        ptpython
        yapf
        pycodestyle
        mccabe
        pyflakes
        mypy
        python-lsp-server
        pylsp-rope
        python-lsp-ruff
        pytest
        pytest-mypy
        pytest-flake8
        pyinstaller
        setuptools
        build
        (toPythonModule pkgs.memray)
      ]));
    in
    {
      devShells.default = pkgs.mkShell {
        packages = [
          python-env
          pkgs.pypy310
        ];
        buildInputs = [
        ];
        nativeBuildInputs = [
        ];
        shellHook = /* sh */ ''
          export DIRENV_PYTHON=${python-env.out}
        '';
      };
    }
  );
}
