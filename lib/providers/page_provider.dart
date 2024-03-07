import 'package:boltz/data/boltz_page_model.dart';
import 'package:boltz/presentation/downloads_page.dart';
import 'package:boltz/presentation/home_page.dart';
import 'package:boltz/presentation/playlist_page.dart';
import 'package:boltz/presentation/settings_page.dart';
import 'package:flutter/material.dart';

List<BoltzPage> pages = [
  BoltzPage("Home", const Icon(Icons.home), const HomePage()),
  BoltzPage(
      "Playlist", const Icon(Icons.playlist_play_sharp), const PlaylistPage()),
  BoltzPage("Downloads", const Icon(Icons.download), const DownloadsPage()),
  BoltzPage("Settings", const Icon(Icons.settings), const SettingsPage())
];
