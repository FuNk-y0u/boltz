import 'package:flutter/material.dart';
import 'package:boltz/providers/page_provider.dart';

Widget getCurrentPage(int index) {
  return pages[index].display;
}
