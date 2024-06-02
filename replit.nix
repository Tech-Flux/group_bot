{ pkgs }: {
  deps = [
    pkgs.python310Full
    pkgs.python310Packages.pip
  ];

  shellHook = ''
    pip install telebot pymongo python-dotenv openai==0.28 yt_dlp googletrans transformers colorama Pillow beautifulsoup4
  '';
}
