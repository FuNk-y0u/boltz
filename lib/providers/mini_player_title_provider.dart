import 'package:boltz/data/player_controller_model.dart';
import 'package:flutter/material.dart';
import 'package:marquee/marquee.dart';

Widget mini_player_title_provider(
    String text, BoltzPlayerController controller) {
  if (controller.isPlaying && text.length > 23) {
    return Marquee(
      text: text,
      accelerationCurve: Curves.linear,
      accelerationDuration: const Duration(milliseconds: 500),
      decelerationCurve: Curves.easeOut,
      decelerationDuration: const Duration(milliseconds: 500),
      showFadingOnlyWhenScrolling: true,
      fadingEdgeEndFraction: 0.1,
      velocity: 50,
      textDirection: TextDirection.ltr,
    );
  } else {
    return Text(
      text,
      overflow: TextOverflow.fade,
      maxLines: 1,
      softWrap: false,
    );
  }
}
