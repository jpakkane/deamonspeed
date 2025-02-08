#!/usr/bin/env python3

# SPDX-License-Identifier: Apache-2.0
# (c) 2025 Jussi Pakkanen

import os, sys, pathlib, shutil, argparse

cmdparser = argparse.ArgumentParser()
cmdparser.add_argument('--daemon', action='store_true', dest='daemon', default=False)
cmdparser.add_argument('--num-sources', dest='num_sources', default=100, type=int)


def setup(source_dir, build_dir, num_sources, use_daemon):
    if source_dir.exists():
        shutil.rmtree(source_dir)
    if build_dir.exists():
        shutil.rmtree(build_dir)
    private_dir = build_dir / 'private'
    source_dir.mkdir()
    build_dir.mkdir()
    private_dir.mkdir()
    output = 'prog'
    sources = [f'source{i}.cpp' for i in range(num_sources)]
    objects = [i + '.o' for i in sources]

    for s in sources:
        open(source_dir / s, 'wb').close()

    # Write Ninja file
    if use_daemon:
        extra_args = f'--private-dir private'
    else:
        extra_args = ''
    with open(build_dir / 'build.ninja', 'w') as ofile:
        ofile.write('ninja_required_version = 1.8.2\n')
        ofile.write(f'''
rule compiler
 command = ../compiler.py {extra_args} -c -o $out $in
 description = Compiling $in
''')
        ofile.write('''
rule linker
 command = ../compiler.py -o $out $in
 description = Linking $out
''')
        ofile.write('''
rule custom
 command = $cmd

build clean: custom
 command = ninja -t clean
 description = Cleaning
''')

        for i in range(num_sources):
            src = sources[i]
            obj = objects[i]
            relsrc = '..' / source_dir / src
            ofile.write(f'''build {obj}: compiler {relsrc}
''')
        ofile.write(f'\nbuild output: linker ')
        for o in objects:
            ofile.write(o)
            ofile.write(' ')
        ofile.write('\n')
        ofile.write('default output\n')

if __name__ == '__main__':
    args = cmdparser.parse_args()
    setup(pathlib.Path('srcdir'), pathlib.Path('builddir'), args.num_sources, args.daemon)
    if args.daemon:
        print('''To run the timing test run this command:

./daemon.py builddir/private 1&; time ninja -C builddir

Ninja seems to track that all spawned child processes have also finished
and I could not find a way to make it not do so. If you run the build command
directly, your timing will have 10 extra seconds while Ninja waits for the
daemon to shut down.''')
