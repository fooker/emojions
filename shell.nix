{ pkgs ? import <nixpkgs> {} }:

let
  py = pkgs.python3.withPackages (pkgs: with pkgs; [
    beautifulsoup4
    svgwrite
    cairosvg
  ]);
in
  py.env

