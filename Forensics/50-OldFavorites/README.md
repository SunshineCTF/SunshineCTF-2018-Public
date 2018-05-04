#  [Forensics 50] Old Favorites

Audio Stego challenge

## Attachment(s)

[OldFavorites.mp4](https://ctf.hackucf.org/challenge-files/OldFavorites.mp4)

## How it works

A five second sound file which contains the flag was inserted into the music video 'Never gonna give you up' by Rick Astley. The sound file creates sound waves which look like the flag "sun{you_know_the_rules}", which can be seen in a spectrogram.

## How to solve it

Open the MP4 either normally or in an audio editing software such as audacity and listen for the warped sound which indicates where the flag is (2:19-2:24). Open the file in spectrogram view and zoom in on the correct time range where the flag appears.

