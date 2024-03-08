import 'package:boltz/data/player_controller_model.dart';
import 'package:boltz/domain/player_controller_service.dart';
import 'package:boltz/providers/mini_player_title_provider.dart';
import 'package:flutter/material.dart';
import 'dart:math' as math;

class BoltzBottomMiniPlayer extends StatefulWidget {
  BoltzPlayerController controller;
  Function? onPlay;
  Function? onSkipForward;
  Function? onSkipBackward;
  BuildContext context;
  BoltzBottomMiniPlayer(
      {super.key,
      required this.context,
      required this.controller,
      this.onPlay,
      this.onSkipForward,
      this.onSkipBackward});

  @override
  State<BoltzBottomMiniPlayer> createState() => _BoltzBottomMiniPlayerState();
}

class _BoltzBottomMiniPlayerState extends State<BoltzBottomMiniPlayer> {
  // TODO Implement proper player controller with proper tracks and que
  // TODO Add music player screen

  String _tmpMusicName =
      "MusicName MusicName - ft Artist1 Artist2 Artist3 Artist4 | Album1 Album2 Album3 Album4 • ";

  @override
  Widget build(BuildContext context) {
    return Align(
      alignment: AlignmentDirectional.bottomCenter,
      child: Padding(
        padding: const EdgeInsets.all(8.0),
        child: Container(
          decoration: BoxDecoration(
              borderRadius: BorderRadius.circular(10),
              color: Theme.of(widget.context).colorScheme.secondary),
          width: double.infinity,
          height: 80,
          child: Row(
            children: [
              Padding(
                padding: const EdgeInsets.all(8.0),
                child: Container(
                  width: 60,
                  height: 60,
                  decoration: BoxDecoration(
                      color: Theme.of(widget.context).colorScheme.primary,
                      borderRadius: BorderRadius.circular(10)),
                  child: const Icon(Icons.music_note),
                ),
              ),
              const Spacer(),
              SizedBox(
                width: 150,
                child: mini_player_title_provider(
                    _tmpMusicName, widget.controller),
              ),
              const Spacer(),
              Transform.rotate(
                angle: math.pi,
                child: IconButton(
                    onPressed: () => actionNullCheck(widget.onSkipBackward)(),
                    icon: const Icon(Icons.skip_next_sharp)),
              ),
              IconButton(
                  onPressed: () => actionNullCheck(widget.onPlay)(),
                  icon: playerIcon(widget.controller.isPlaying)),
              IconButton(
                  onPressed: () => actionNullCheck(widget.onSkipForward)(),
                  icon: const Icon(Icons.skip_next_sharp)),
            ],
          ),
        ),
      ),
    );
    ;
  }
}
