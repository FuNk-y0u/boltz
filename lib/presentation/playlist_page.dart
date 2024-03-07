import 'package:flutter/material.dart';

class PlaylistPage extends StatefulWidget {
  const PlaylistPage({super.key});

  @override
  State<PlaylistPage> createState() => _PlaylistPageState();
}

class _PlaylistPageState extends State<PlaylistPage> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(
          "Playlist Page",
          style: TextStyle(color: Theme.of(context).colorScheme.primary),
        ),
      ),
      body: const Center(child: Text("Playlist Page")),
    );
  }
}
