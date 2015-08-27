<snippet>
  <content>
# BNNvideofetch
This version is for windows system.
Dependencies are wget to download the 2nd m3u8 file.
#Usage

1. Find a video from http://m.bnn.ca/video/ you'd like to download.
http://m.bnn.ca/video/-/f/RZo3/click?itemId=668997&p_p_lifecycle=1 for example.
2. download the manifest.m3u8
Video comes in a variety of video qualities ranging from 2-16 (lowest to best), even numbers only.
3. Run script like so: "python BNNvideofetch.py manifest.m3u8 16 optionalcustomfilename"

A second m3u8 specific to the video quality will be downloaded. 
An html will be created with links to video fragment files.
A delete batch file will be created for file clean-up except for the video file.
A copy batch file will be created to stitch video fragment files together.

4. Download the video fragments using your favourite download manager like DownThemAll.
5. Run the copy batch file to do the stitching.
6. Run the Delete batch file to clean-up the files.
7. Watch the video using your favourite media player!

</content>
  <tabTrigger></tabTrigger>
</snippet>