import 'package:flutter/material.dart';

class DownloadsPage extends StatefulWidget {
  const DownloadsPage({super.key});

  @override
  State<DownloadsPage> createState() => _DownloadsPageState();
}

class _DownloadsPageState extends State<DownloadsPage> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(
          "Downloads Page",
          style: TextStyle(color: Theme.of(context).colorScheme.primary),
        ),
      ),
      body: const Center(child: Text("Downloads Page")),
    );
  }
}
