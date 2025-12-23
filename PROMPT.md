The files you've produced look very good, thank you, this is excellent. I have copied the transcript from the video here for your reference, although I feel like it's not necessary any more:

```
0:00
Gausian splatting is easier to do than
0:02
ever before. I've been playing around
0:03
with it for the last couple of months,
0:05
and it's a brilliant way to create 3D
0:07
models using home videos, found footage,
0:09
and collections of photographs. Gausian
0:12
splats are impressionistic
0:13
three-dimensional point clouds, which
0:15
capture the optics of the camera, the
0:17
atmosphere of the space, and the
0:18
materiality of its surfaces. They
0:21
capture soft, fuzzy, organic forms and
0:23
glassy, shiny, and translucent objects.
0:26
We can now do this process using all
0:28
free software and we can compute our
0:30
models faster than ever using glow map.
0:33
We can render our splats in Blender and
0:34
we can composite 3D objects into them
0:37
which also happens to help with the
0:39
process of motion tracking. So I'm going
0:41
to take you through how I created this
0:43
Gausian splat here and show you how you
0:45
can do it at home for free.
0:48
Okay. So the first thing that we need to
0:49
do is we need to convert this video into
0:51
still frames so we can process it as a
0:54
photoggramometry model. And so what I'm
0:55
going to do is I'm going to open up
0:56
Blender 4.5 and I'm going to go over to
0:59
the video editing workspace. Then what
1:01
I'm going to do is I'm going to drag my
1:03
footage into the video timeline and I'm
1:05
going to snap it to the playhead here.
1:07
Now if I zoom out a little bit and then
1:09
press Ctrl T. You can see how many
1:13
frames are in this footage. And if I
1:15
wanted to constrain the scene duration
1:17
to this strip, I can go to view range
1:21
and set frame range to strips. And
1:23
because my footage is only about 175
1:26
frames long, this should be perfectly
1:27
fine. But your footage might be longer.
1:30
In fact, it might be quite a bit longer.
1:32
And so if you're in the region of 400,
1:34
500 frames or perhaps even more than
1:36
that, you might want to consider
1:38
reducing it to make the photoggramometry
1:40
processing a little bit quicker. So if
1:42
your clip is quite long, what you can do
1:43
is you can go over here to the output
1:46
properties and you can set the frame
1:48
range end to something like 250. Then
1:51
what you can do is you can click on your
1:52
strip, press Ctrl+R, and you should see
1:54
these two little key frame indicators
1:56
pop up. This controls the rate of the
1:58
clip. If you select the one on the right
2:00
hand side, and then drag it to the scene
2:03
end, you can see that your clip has now
2:05
been constrained to 250 frames. In my
2:08
case, however, I only have 175 frames to
2:11
worry about. So, I'm not going to do
2:12
that. So, with my duration set for my
2:15
clip, I can go back here over to the
2:17
output properties, and I can choose the
2:19
location to save my images. So, I'm
2:22
going to go over to the project folder,
2:24
and I'm going to create a new folder,
2:27
which is called images.
2:29
I'm going to select that folder, and
2:31
then for my file format, I'm going to
2:32
choose PNG. You can also use JPEG for
2:35
this, but PNG is going to be slightly
2:36
higher quality. And so with these
2:38
options selected, I can go to render and
2:40
then render animation. And it's going to
2:42
export all of those still frames to this
2:45
folder called images. And now I can
2:46
close Blender. And I don't need to save
2:48
the file.
2:51
Okay. So this is where it gets a little
2:52
bit more complicated. We're going to
2:54
need to download two pieces of software
2:56
in order to calculate the
2:57
photoggramometry. First of which is
2:59
called Colemap and the second of which
3:00
is called Glow Map. So I'm going to
3:02
download Cole Map. I'm going to go to
3:03
the releases section here and I'm going
3:05
to choose colap x64 for Windows CUDA
3:08
because I have a graphics card that's
3:09
compatible with CUDA. And so once Colap
3:13
is downloaded, I'm going to extract it
3:16
and I'm going to put it into a folder
3:17
called Cole Map.
3:20
Next, I'm going to download Glow Map.
3:22
So, I'm going to go over here to
3:23
releases and I'm going to download the
3:25
latest version again, Glow Map x64
3:27
Windows CUDA. And once that's finished
3:30
downloading, again, I'm going to extract
3:32
the contents and I'm going to move those
3:33
into a new folder which is called glow
3:35
map. So now we have our coal map folder
3:38
and our glow map folder. So what we need
3:40
to do now is we need to make sure that
3:41
the operating system can recognize these
3:43
two pieces of software. And in order to
3:45
do that, we need to edit the environment
3:47
variables for Windows. So I'm going to
3:49
type in environment variables. And I'm
3:50
going to click here where it says
3:52
environment variables.
3:54
I'm going to scroll down to where it
3:56
says path. I'm going to double click on
3:58
path and then I'm going to go over to
4:00
the location where the coal map
4:01
executable is and then I'm going to
4:03
choose the folder called bin. So I'm
4:04
going to copy this path. I'm going to
4:06
add a new path here in my environment
4:08
variables and I'm going to paste the
4:11
path of that bin folder into there. Now
4:13
what we need to do is we need to go back
4:15
and we need to find the same thing for
4:17
glow map. So I'm going to double click
4:18
on glow map, click on the bin folder and
4:20
I'm going to choose this path. I'm going
4:23
to add a new entry into my environment
4:26
variables and I'm going to paste glow
4:28
map in there. So you should see one
4:29
entry for coal map and you can see
4:31
another entry for glow map. Once that's
4:33
set up, you can press okay. Press okay
4:35
again. Press okay. And now your system
4:37
should be able to recognize these two
4:39
pieces of software.
4:42
Okay. So I'll put a link in the
4:44
description to this. But the next thing
4:45
you need to do is download this Python
4:47
file which is called runglow mapap. py.
4:50
And we're going to use this to calculate
4:51
our photoggramometry. So, I'm going to
4:53
go over here to the header of the file
4:56
browser, and I'm going to type in cmd.
4:59
And that's going to open up a console
5:01
window, which is going to give me
5:03
ability to run commands. The command
5:05
that I want to run is python
5:09
run gloap. py. And then we need to type
5:13
dash dash
5:14
image
5:16
path. And then we need to specify the
5:18
path where our images are saved. And an
5:20
easy way to do this is to just click and
5:22
drag your images folder into the command
5:24
line. And now our command is ready. So
5:26
what we can do is we can press enter and
5:29
it's going to start using whole map and
5:31
glow map to process those images into a
5:34
photogometry model. Sometimes this can
5:36
be quite fast, sometimes it can be a bit
5:38
slow. It really depends how many images
5:40
you have and what resolution those
5:42
images are.
5:46
Okay. So for me the process took 76.68
5:50
seconds. That's quite fast for a
5:52
photoggramometry reconstruction. Okay.
5:55
So now we can close this command line.
5:59
And the next thing we need to do is
6:00
download the photoggramometry importer
6:02
for Blender. I'm going to go over to the
6:04
releases section and I'm going to
6:06
download photoggramometry importer.zip.
6:08
I'm going to save that to my software
6:10
folder. And then with Blender open, what
6:12
I can do is I can drag this photogometry
6:14
importer.zip zip into Blender and then I
6:17
can choose okay to install the add-on.
6:19
Now, the first thing we need to do is
6:20
actually restart Blender. So, I'm going
6:22
to close it and then I'm going to open
6:23
it again. And to make this add-on work,
6:25
we need to install some dependencies.
6:27
So, I'm going to go to edit preferences.
6:29
I'm going to search for
6:30
photoggramometry.
6:32
Expand that. And if you scroll down, you
6:35
should see that there are some
6:37
dependencies that need to be installed.
6:38
And I would recommend doing this one by
6:40
one. So, first I'm going to click on
6:41
install setup tools. Now, in this case,
6:43
I got an error because setup tools was
6:46
already installed. So, I'm going to
6:47
ignore that error for now. And I'm going
6:48
to install pillow. I'm going to install
6:50
lasers. I'm going to install LASPI. And
6:51
finally, I'm going to install pint
6:53
cloud. Now, I'm going to close this
6:55
dialogue. So, what I'm going to do is
6:57
I'm going to delete the default objects
6:58
in the scene. I'm going to go to file,
7:02
import, and I'm going to select the
7:04
option call map model workspace. I'm
7:07
going to navigate to my demo folder, and
7:09
I'm going to choose the folder which is
7:10
called sparse. Within the folder sparse,
7:12
I'm going to choose the folder called
7:13
zero. This is the first attempt at the
7:15
photoggramometry. You should see that
7:16
there are a few files in here. I'm going
7:18
to use the default settings from the
7:19
add-on. And I'm going to press import
7:21
col model. Now, I got an error that some
7:23
images were missing, but this doesn't
7:25
matter for now. Inside of your scene,
7:27
you should see that there is a kind of
7:29
point cloud. And there is a bunch of
7:31
cameras that are the camera frames that
7:33
we exported. Now, you can see that this
7:35
isn't properly oriented. So, what I'm
7:37
going to do is I'm going to maximize
7:38
Blender. I'm going to press A to select
7:40
all. I'm going to collapse this
7:42
collection that's called cameras. And
7:43
I'm going to controllclick on OpenGL
7:46
point cloud. And then with that selected
7:49
and my cursor in the 3D viewport, I'm
7:51
going to press Ctrl P and I'm going to
7:53
parent all of the objects to that OpenGL
7:55
point cloud empty. Now what I can do is
7:57
I can click on the OpenGL point cloud
7:59
and I can rotate it. So if I press R and
8:01
then X, I can rotate it on the X axis
8:03
and I can make it so all of the
8:04
buildings that we have in our
8:06
photoggramometry are pointing upwards.
8:08
Okay, so that looks pretty good. So now
8:10
what I can do is I can go to my outliner
8:12
here, search for animated, and you
8:14
should see a camera called animated. And
8:16
if I select that and then press control
8:18
number pad zero, that will take me
8:20
inside of the animated camera. Now if I
8:22
press the space bar to play the
8:23
animation, you should see that the
8:24
camera moves through the point cloud
8:26
much as it should based on the video.
8:28
And so this is how we transform the 3D
8:30
model. So what I'm going to do is I'm
8:32
going to save my file.
8:35
Okay, so in order to create our Gaussian
8:37
splat, we need to use this piece of
8:38
software which is called Brush. So I'm
8:40
going to put a link in the description,
8:41
but you can go over here to the releases
8:43
section and scroll down to the release.
8:47
In this case, I'm going to download the
8:48
Windows zip file and I'm going to save
8:50
that to my software folder alongside the
8:52
other softwares that we download. So
8:54
what I'm going to do here is I'm going
8:55
to create a new folder. I'm going to
8:56
call it brush app. I'm going to drag the
8:59
brush app into that folder. I'm going to
9:00
rightclick and I'm going to extract it.
9:02
And you should see that that creates a
9:05
file which is called brushapp.exe. So
9:07
I'm going to click on that file. And you
9:09
can see here this is the brush app. Now
9:11
in order to make this work, we need to
9:13
load up our sparse reconstruction from
9:16
before. So now with the brush app open,
9:18
I'm going to go to the directory option
9:20
here. I'm going to navigate to the
9:22
project folder and I'm just going to
9:24
select the top level here. Press select
9:27
and then you should see that you are
9:29
given these options. Now, these are the
9:31
different settings that you can use to
9:33
run brush with. And to begin with, I
9:35
would recommend just leaving it at the
9:36
default. Press start, and you should
9:39
start to see a gausian splat emerging.
9:44
So, what's happening here is that my
9:46
computer is creating thousands and
9:48
thousands of gausian splats and then
9:50
it's adjusting them based on the images
9:53
from the original data set down here.
9:55
And if I click on this little expand
9:57
icon here and then I move through the
10:00
frames, you can see that it takes us
10:02
through the different camera positions
10:04
and shows us the different
10:07
three-dimensional perspectives of the
10:09
gausian splat. Whilst it's working, you
10:11
can use the WD keys to move around the
10:14
scene, and you can also use the Q and E
10:17
buttons to move up and down. So, I'm
10:19
going to run my Gausian splat for 10,000
10:21
frames, but you can run it for longer or
10:23
you can run it for a shorter period of
10:25
time. So, now that we're at 10,000
10:27
steps, I'm going to go over here to the
10:28
controls and I'm going to choose the
10:30
export option. And I'm going to save
10:32
that to my project folder. Press save.
10:36
And now I'm going to close the brush app
10:38
to stop it from running.
10:41
So, in order to import the Gaussian
10:43
splat into Blender, we need to use this
10:45
Kiri 3DGS render add-on. And the latest
10:48
version is actually for Blender 5. So
10:50
I'm going to go over to here where it
10:51
says releases and I'm going to scroll
10:53
down to version 4.0. Expand the assets
10:56
and then I'm going to download that zip
10:58
file there. Save that to my software
11:00
folder. And when that's downloaded, you
11:02
can just drag it into Blender. Press
11:04
okay to install. So I'm going to expand
11:06
Blender. I'm going to go outside of my
11:08
camera so I can see what I'm doing. And
11:10
I'm going to press the end panel here.
11:11
And you can see that there is an option
11:12
which is 3DGS render. I'm going to click
11:15
that. And then I'm going to press import
11:16
ply. I'm going to import that ply that
11:19
we exported from the brush app. And you
11:21
should see that a bunch of points come
11:23
in like this. With my ply selected, I'm
11:26
going to control-click on the OpenGL
11:27
point cloud empty. Press Ctrl P and
11:30
select parent to object without inverse.
11:33
And then you should see that the
11:35
Gaussian point cloud aligns with the
11:38
original point cloud. Now, in order to
11:40
see the splats, what we need to do is we
11:42
need to press the render option here.
11:45
And then if we turn off our original
11:46
point cloud by controll-clicking on this
11:49
object here, you should see that you
11:50
just have the splat. And so now we're
11:52
able to navigate around our gausian
11:54
splat. If we go back inside that
11:55
animated camera and press play, you can
11:57
see that the camera is moving through
11:58
the splat along the line of those
12:00
original cameras that we imported. We
12:02
can turn those off as well to make it
12:03
more clear. And we can also add objects
12:06
into this 3D scene. So if I press shift
12:08
A, I can add a cube, place that
12:10
somewhere inside the world. And you can
12:12
see that it does interact with the
12:14
scene. Could also add the Suzanne in
12:17
there. Place that inside the scene. And
12:19
so you can see if I go over here to the
12:21
render tab, it's going to by default
12:24
render the color pass to the temporary
12:27
directory. So if I press render, you can
12:28
see that's here. It's created a frame
12:30
which is just the Gaussian splat.
12:32
However, you can do a combined pass. So
12:35
if I select this option here, combine
12:37
with native render and then render that
12:39
frame. You can see that it creates this
12:42
uh frame here which is composite and you
12:44
can see there we've got the gausian
12:46
splat mixed in with the 3D objects and
12:48
you can also render a um depth pass and
12:51
that will create something that looks a
12:53
bit like this. So there are some
12:55
compositing options available to you.
12:57
And so this is how you can get a gausian
12:59
splat into Blender. And um I found this
13:02
to be really uh enjoyable experience. Um
13:06
and I hope you can create some fun stuff
13:08
with it too.
13:10
Okay, well done for making it to the end
13:12
of the video. Just a quick note about
13:14
versions. Most of the steps in this
13:16
process work on Blender 5 except for
13:18
step four, which is importing the
13:19
photoggramometry model. Um and it's
13:21
possible that in the future that will
13:23
start working. And if it does, I'll
13:24
update the description to include the
13:27
version of photoggramometry and border
13:28
that you need to use. Thanks.
```

However, I wanted to note a couple of things I've gathered from this video:
- It leverages glomap as well as colmap; Is this because glomap is faster? Or is it because it can infer camera positions even from non-dslr cameras? What is glomap responsible for when used in conjunction with colmap?
- It leverages Blender 4.2 however, I was unable to get this to work with this version. I used Blender 4.5 which is compatible with the kiri engine 3dgs blender add-on.
- Could you update the BLENDER_GUIDE.md to leverage the add-ons mentioned in the video instead of ReshotAI?

Some other general notes:

- CUDA support is essential for faster processing times and I have noticed that is how you've setup this project, which is great. However, I would like people without an NVIDIA card to be able to run the pipeline perhaps relying on the CPU instead. I don't want to modify the original instructions, and instead create an alternative path for them (perhaps as seperate setup files).
- I really like that you've stick to using WSL2 when writing instructions for the Windows platform. That way, it's very similar or even the same as using native Ubuntu.
- I would like to modify the first section of the ./docker/README.md which provides a link to installing Docker Destkop (for Windows) for working with WLS2. This is great, but with Docker's recent new paywall additions and paid services, it would be nice to, in addition to these, to add instructions for installing Docker CLI which remains free and open-source

---

The video workflow uses COLMAP for feature extraction/matching, then Glomap for the reconstruction step specifically because it's much faster.