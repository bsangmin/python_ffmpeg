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


def case_co():
    cmds = []
    for idx in range(LOOP):
        cmd = ["ffmpeg", "-y", "-v", "error"]
        cmd.extend(["-ss", f"{idx*5}", "-i", "nonbackup/sample.mkv"])
        cmd.extend(
            [
                "-filter_complex",
                f"drawtext=fontsize=40:fontcolor=white:x=10:y=10:text={idx+1}",
            ]
        )
        cmd.extend(
            [
                "-vframes",
                "1",
                "-q:v",
                "2",
                "-f",
                "image2",
                "dist/out_{:02d}.jpg".format(idx),
            ]
        )
        cmds.append(cmd)

    @RunningTime
    def run_case_co(cmds):
        loop = asyncio.new_event_loop()
        loop.run_until_complete(task_coroutine(cmds))
        loop.close()

    run_case_co(cmds)


def case_ff():
    cmd = ["ffmpeg", "-y", "-v", "error"]
    for idx in range(LOOP):
        cmd.extend(["-ss", f"{idx*5}", "-i", "nonbackup/sample.mkv"])
        cmd.extend(
            [
                "-filter_complex",
                f"drawtext=fontsize=40:fontcolor=white:x=10:y=10:text={idx+1}[v1]",
            ]
        )
        cmd.extend(
            [
                "-vframes",
                "1",
                "-q:v",
                "2",
                "-f",
                "image2",
                "-map",
                "[v1]",
                "dist/out_{:02d}.jpg".format(idx),
            ]
        )

    @RunningTime
    def run_case_ff(cmd, sema):
        asyncio.run(subprocess(cmd, sema))

    run_case_ff(cmd, None)


def main():
    for loop in range(5):
        print(f"----- LOOP {loop+1}")
        case_ff()
        case_co()


if __name__ == "__main__":
    LOOP = 50
    SEMAPHORE = 4

    main()