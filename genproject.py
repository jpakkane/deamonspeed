#!/usr/bin/env python3

# SPDX-License-Identifier: Apache-2.0
# (c) 2025 Jussi Pakkanen

import os, sys, pathlib, shutil

def setup(source_dir, build_dir, num_sources):
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
    with open(build_dir / 'build.ninja', 'w') as ofile:
        ofile.write('ninja_required_version = 1.8.2\n')
        ofile.write('''
rule compiler
 command = ../compiler.py -c -o $out $in
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
 cmd = ninja -t clean
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

if __name__ == '__main__':
    setup(pathlib.Path('srcdir'), pathlib.Path('builddir'), 100)
