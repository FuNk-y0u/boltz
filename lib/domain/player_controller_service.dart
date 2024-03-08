import 'package:flutter/material.dart';

Icon playerIcon(bool isPlaying) {
  if (isPlaying) {
    return const Icon(Icons.pause);
  } else {
    return const Icon(Icons.play_arrow);
  }
}

Function actionNullCheck(Function? onPress) {
  var action = onPress;
  if (action != null) return action;
  return () => {};
}
