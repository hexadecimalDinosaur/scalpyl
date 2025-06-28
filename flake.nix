{
  inputs = {
    nixpkgs.url = "flake:nixpkgs-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils, ... }:
    flake-utils.lib.eachDefaultSystem (
      system:
      let
        pkgs = (import nixpkgs {
          inherit system;
          config = {
            permittedInsecurePackages = [
              "qtwebkit-5.212.0-alpha4"
            ];
          };
        });
        python-env = (pkgs.python311.withPackages (p: with p; [
          requests
          xdis
          uncompyle6
          # pyqt6
          # pyside6
          pywebview
          qtpy
          flask
          self.packages.${system}.python311Packages.decompyle3
          self.packages.${system}.python311Packages.x-python
          self.packages.${system}.python311Packages.xasm
          self.packages.${system}.python311Packages.pyinstxtractor-ng

          jupyter
          ipython
          jupyter
          rich

          # dev tools
          pip
          autopep8
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
          pyinstaller
        ]));
        pypy-env = (pkgs.pypy310.withPackages (p: with p; [
          xdis
          uncompyle6
          self.packages.${system}.pypy310Packages.decompyle3
          self.packages.${system}.pypy310Packages.x-python
          self.packages.${system}.pypy310Packages.xasm
        ]));
      in
      {
        devShells.default = pkgs.mkShell {
          packages = [
            python-env
            pypy-env
          ];
          buildInputs = [
            # pkgs.webkitgtk_6_0
            # pkgs.gtk3
            # pkgs.qt6.full
            # pkgs.qt6.qtwayland
            pkgs.qt5.full
            pkgs.qt5.qtwayland
          ];
          nativeBuildInputs = [
          ];
          shellHook = /* sh */ ''
            export DIRENV_PYTHON=${python-env.out}
            export QT_QPA_PLATFORM_PLUGIN_PATH="${pkgs.qt5.full}/lib/qt-${pkgs.qt5.qtbase.version}/plugins";
            export QT_PLUGINS_PATH="$QT_QPA_PLATFORM_PLUGIN_PATH";
            export PYWEBVIEW_LOG=debug
            export PYWEBVIEW_GUI=qt
          '';
        };
        packages = {
          pypy310Packages = rec {
            decompyle3 = (pkgs.pypy310.pkgs.callPackage ./nixpkgs/decompyle3.nix { });
            x-python = (pkgs.pypy310.pkgs.callPackage ./nixpkgs/x-python.nix { });
            xasm = (pkgs.pypy310.pkgs.callPackage ./nixpkgs/xasm.nix { inherit x-python; });
            pyinstxtractor-ng = (pkgs.pypy310.pkgs.callPackage ./nixpkgs/pyinstxtractor-ng.nix {});
          };
          python311Packages = rec {
            decompyle3 = (pkgs.python311Packages.callPackage ./nixpkgs/decompyle3.nix { });
            x-python = (pkgs.python311Packages.callPackage ./nixpkgs/x-python.nix { });
            xasm = (pkgs.python311Packages.callPackage ./nixpkgs/xasm.nix { inherit x-python; });
            pyinstxtractor-ng = (pkgs.python311Packages.callPackage ./nixpkgs/pyinstxtractor-ng.nix {});
          };
          python312Packages = rec {
             decompyle3 = (pkgs.python312Packages.callPackage ./nixpkgs/decompyle3.nix { });
             x-python = (pkgs.python312Packages.callPackage ./nixpkgs/x-python.nix { });
             xasm = (pkgs.python311Packages.callPackage ./nixpkgs/xasm.nix { inherit x-python; });
             pyinstxtractor-ng = (pkgs.python311Packages.callPackage ./nixpkgs/pyinstxtractor-ng.nix {});
          };
          python313Packages = rec {
             decompyle3 = (pkgs.python313Packages.callPackage ./nixpkgs/decompyle3.nix { });
             x-python = (pkgs.python313Packages.callPackage ./nixpkgs/x-python.nix { });
             xasm = (pkgs.python311Packages.callPackage ./nixpkgs/xasm.nix { inherit x-python; });
             pyinstxtractor-ng = (pkgs.python311Packages.callPackage ./nixpkgs/pyinstxtractor-ng.nix {});
          };
        };
      }
    );
}
