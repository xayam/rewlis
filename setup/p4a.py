import subprocess

command = \
    "p4a apk " + \
    "--debug " + \
    "--private=$CURR_DIR/$NAME_PROJECT " + \
    "--package=com.github.$NAME_GITHUB.$NAME_PROJECT " + \
    "--dist_name=$NAME_APP-$TARGET_PLATFORM " + \
    '--name="$NAME_APP" ' + \
    "--wakelock " + \
    "--window " + \
    "--permission android.permission.INTERNET " + \
    "android.permission.READ_EXTERNAL_STORAGE " + \
    "android.permission.WRITE_EXTERNAL_STORAGE " + \
    "android.permission.GLOBAL_SEARCH " + \
    "android.permission.MEDIA_CONTENT_CONTROL " + \
    "android.permission.READ_MEDIA_AUDIO " + \
    "--orientation=landscape " + \
    "--icon=$CURR_DIR/$NAME_PROJECT/res/img/icon.png " + \
    "--presplash=$CURR_DIR/$NAME_PROJECT/res/img/presplash.png " + \
    "--version=$APP_VERSION " + \
    "--arch=$TARGET_PLATFORM " + \
    "--bootstrap=sdl2 " + \
    "--requirements=android,python3,kivy,mutagen,cython,ffmpeg,libx264," + \
    "libshine,libvpx,av_codecs,av,ffpyplayer,openssl,ffpyplayer_codecs," + \
    "setuptools,regex,sdl2_image,sdl2_ttf,sdl2_mixer,sdl2"

if __name__ == "__main__":
    subprocess.call([command], shell=True)
