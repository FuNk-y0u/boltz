import 'package:boltz/data/boltz_page_model.dart';
import 'package:flutter/material.dart';

Widget BoltzNavBar(Function(int)? onDestinationSelected, List<BoltzPage> pages,
    int currentPageIndex) {
  List<NavigationDestination> generateDestinations() {
    List<NavigationDestination> destinations = [];

    for (var page in pages) {
      destinations
          .add(NavigationDestination(icon: page.icon, label: page.name));
    }
    return destinations;
  }

  return NavigationBar(
    onDestinationSelected: onDestinationSelected,
    destinations: generateDestinations(),
    selectedIndex: currentPageIndex,
  );
}
