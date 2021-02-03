# coding=utf-8


import asyncio
from mods.decorator import RunningTime


async def subprocess(cmd, sema):
    if not sema:
        sema = asyncio.Semaphore(SEMAPHORE)

    async with sema:
        task = await asyncio.create_subprocess_exec(
            *cmd,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
        )
        await task.communicate()


async def task_coroutine(cmds):
    sema = asyncio.Semaphore(SEMAPHORE)

    futures = [asyncio.create_task(subprocess(cmd, sema)) for cmd in cmds]

    await asyncio.gather(*futures)


@RunningTime
def multi_task_coroutine():
    cmds = []
    for idx in range(0, LOOP):
        cmd = []
        opt = {
            "bin": ["ffmpeg"],
            "pre": ["-y", "-v", "error"],
            "inputs": ["-f", "lavfi", "-i", "color=black:100x100"],
            "filter": [
                "-filter_complex",
                f"[0:v]drawtext=fontsize=40:fontcolor=white:x=10:y=10:text={idx+1}[v_{idx+1}]",
            ],
            "outputs": [
                "-map",
                f"[v_{idx+1}]",
                "-vframes",
                "1",
                "-q:v",
                "2",
                "-f",
                "image2",
                "dist/out_{:02d}.jpg".format(idx),
            ],
        }
        for k in ["bin", "pre", "inputs", "filter", "outputs"]:
            cmd.extend(opt[k])

        cmds.append(cmd)

    loop = asyncio.new_event_loop()
    loop.run_until_complete(task_coroutine(cmds))
    loop.close()


@RunningTime
def multi_filter_ffmpeg():
    opt = {
        "bin": ["ffmpeg"],
        "pre": ["-y", "-v", "error"],
        "inputs": ["-f", "lavfi", "-i", "color=black:100x100"],
        "filter": ["-filter_complex"],
        "outputs": [],
    }

    filter_ = ""
    for idx in range(0, LOOP):
        filter_ += f"[0:v]drawtext=fontsize=40:fontcolor=white:x=10:y=10:text={idx+1}[v_{idx+1}];"
        opt["outputs"].extend(
            [
                "-map",
                f"[v_{idx+1}]",
                "-vframes",
                "1",
                "-q:v",
                "2",
                "-f",
                "image2",
                "dist/out_{:02d}.jpg".format(idx),
            ]
        )
    opt["filter"].append(filter_[:-1])

    cmd = []
    for k in ["bin", "pre", "inputs", "filter", "outputs"]:
        cmd.extend(opt[k])

    asyncio.run(subprocess(cmd, None))


def main():
    for loop in range(5):
        print(f"----- LOOP {loop+1}")
        multi_filter_ffmpeg()
        multi_task_coroutine()


if __name__ == "__main__":
    LOOP = 100
    SEMAPHORE = 4

    main()
