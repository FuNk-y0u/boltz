import 'package:flutter/material.dart';

class SettingsPage extends StatefulWidget {
  const SettingsPage({super.key});

  @override
  State<SettingsPage> createState() => _SettingsPageState();
}

class _SettingsPageState extends State<SettingsPage> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(
          "Settings Page",
          style: TextStyle(color: Theme.of(context).colorScheme.primary),
        ),
      ),
      body: const Center(child: Text("Settings Page")),
    );
  }
}
