import 'package:boltz/domain/pages_service.dart';
import 'package:boltz/layout/boltz_navigation_bar.dart';
import 'package:boltz/providers/page_provider.dart';
import 'package:boltz/themes/dark_theme.dart';
import 'package:boltz/themes/light_theme.dart';
import 'package:flutter/material.dart';

void main() {
  runApp(MainApp());
}

class MainApp extends StatefulWidget {
  const MainApp({super.key});

  @override
  State<MainApp> createState() => _MainAppState();
}

class _MainAppState extends State<MainApp> {
  int currentPageIndex = 0;

  void setCurrentPageIndex(int index) {
    setState(() {
      currentPageIndex = index;
    });
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      theme: lightTheme,
      darkTheme: darkTheme,
      home: Scaffold(
        bottomNavigationBar:
            BoltzNavBar(setCurrentPageIndex, pages, currentPageIndex),
        body: getCurrentPage(currentPageIndex),
      ),
    );
  }
}
