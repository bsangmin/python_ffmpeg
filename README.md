# Environment

-   CPU: J3160@1.60 GHz (Burst 2.24 GHz)
-   OS: Ubuntu 18.04 TLS
-   python: 3.9.1
-   ffmepg: 3.4.8

# Case 1

### Create images

-   Using one subprocess and muiltiple filter in ffmepg
    ```
    ffmpeg -f lavfi -i color=black:100x100 \
    -filter_complex \
    [0:v]drawtext=fontsize=40:fontcolor=white:x=10:y=10:text=1[v_1];\
    [0:v]drawtext=fontsize=40:fontcolor=white:x=10:y=10:text=2[v_2];\
    ...
    -map "[v_1]" -vframes 1 -q:v 2 -f image2 dist/out01.jpg \
    -map "[v_2]" -vframes 1 -q:v 2 -f image2 dist/out02.jpg \
    ...
    ```
-   Using coroutine (In my case set semaphore count to four)

    ```
    ffmpeg -f lavfi -i color=black:100x100 \
    -filter_complex \
    drawtext=fontsize=40:fontcolor=white:x=10:y=10:text=1 \
    -vframes 1 -q:v 2 -f image2 dist/out01.jpg
    --------------------------------------------------- task 1
    ffmpeg -f lavfi -i color=black:100x100 \
    -filter_complex \
    drawtext=fontsize=40:fontcolor=white:x=10:y=10:text=2 \
    -vframes 1 -q:v 2 -f image2 dist/out02.jpg
    --------------------------------------------------- task 2
    ...
    ```

### Result

```
Create 100 images for each loop

----- LOOP 1
multi_filter_ffmpeg 6.607814311981201
multi_task_coroutine 9.230214595794678
----- LOOP 2
multi_filter_ffmpeg 6.68984842300415
multi_task_coroutine 9.278635740280151
----- LOOP 3
multi_filter_ffmpeg 6.896129369735718
multi_task_coroutine 9.287603855133057
----- LOOP 4
multi_filter_ffmpeg 6.616771221160889
multi_task_coroutine 9.48145341873169
----- LOOP 5
multi_filter_ffmpeg 6.597380876541138
multi_task_coroutine 9.700622320175171
```

# Case 2

### Capture images at video

-   Using one subprocess
    ```
    ffmpeg -y -v error \
    -ss 10 -i /path/video \
    -filter_complex "drawtext=fontsize=40:fontcolor=white:x=10:y=10:text=1[v1]" \
    -vframes 1 -q:v 2 -f image2 -map "[v1]" dist/out01.jpg \
    -ss 20 -i /path/video \
    -filter_complex "drawtext=fontsize=40:fontcolor=white:x=10:y=10:text=2[v1]" \
    -vframes 1 -q:v 2 -f image2 -map "[v1]" dist/out02.jpg \
    ...
    ```
-   Using coroutine (In my case set semaphore count to four)
    ```
    ffmpeg -y -v error \
    -ss 10 -i /path/video \
    -filter_complex "drawtext=fontsize=40:fontcolor=white:x=10:y=10:text=1" \
    -vframes 1 -q:v 2 -f image2 dist/out01.jpg \
    --------------------------------------------------- task 1
    ffmpeg -y -v error \
    -ss 20 -i /path/video \
    -filter_complex "drawtext=fontsize=40:fontcolor=white:x=10:y=10:text=2" \
    -vframes 1 -q:v 2 -f image2 dist/out02.jpg \
    --------------------------------------------------- task 2
    ...
    ```

### Result

```
Capture 50 images for each loop

----- LOOP 1
run_case_ff 24.4374680519104
run_case_co 18.807467937469482
----- LOOP 2
run_case_ff 23.68189835548401
run_case_co 18.828185558319092
----- LOOP 3
run_case_ff 23.656421184539795
run_case_co 18.350685119628906
----- LOOP 4
run_case_ff 24.157839059829712
run_case_co 19.04792618751526
----- LOOP 5
run_case_ff 23.450905084609985
run_case_co 18.948893547058105
```
