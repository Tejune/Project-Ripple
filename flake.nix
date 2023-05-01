{
  description = "Application packaged using poetry2nix";

  inputs.flake-utils.url = "github:numtide/flake-utils";
  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  inputs.poetry2nix = {
    url = "github:nix-community/poetry2nix";
    inputs.nixpkgs.follows = "nixpkgs";
  };

  outputs = inputs@{ self, nixpkgs, flake-utils, poetry2nix }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        # see https://github.com/nix-community/poetry2nix/tree/master#api for more functions and examples.
        inherit (poetry2nix.legacyPackages.${system}) mkPoetryApplication;
        pkgs = nixpkgs.legacyPackages.${system};
      in
      {
        packages = {
          project-ripple = mkPoetryApplication {
            python = pkgs.python311;
            projectDir = self;
            propagatedBuildInputs = [ pkgs.python311Packages.tkinter ];
            overrides = pkgs.poetry2nix.defaultPoetryOverrides.extend
              (self: super:
                {
                  pygame = pkgs.python311Packages.pygame;
                  pillow = pkgs.python311Packages.pillow;
                }
              );
          };
          default = self.packages.${system}.project-ripple;
        };

        devShells.default = pkgs.mkShell {
          packages = [ poetry2nix.packages.${system}.poetry ];
        };
      });
}
