{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
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
      # python 3.12.11
      python-env = (pkgs.python312.withPackages (p: with p; [
        requests
        xdis  # 6.1.5
        uncompyle6  # 3.9.2
        decompyle3  # 3.9.2
        x-python  # 1.5.2
        xasm  # 1.2.1.dev0
        pyinstxtractor-ng  # 2025.1.6
        dearpygui  # 2.0.0b2
        pylingual  # 0.1.0

        jupyter
        ipython
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
