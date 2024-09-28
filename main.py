import os
import click

from llmcc.parser import parse_from_file
from llmcc.compiler import compile_graph
from llmcc.printer import write_graph, print_graph
from llmcc.config import *
from llmcc.includer import include_graph
from llmcc.slicer import slice_graph
from llmcc.analyzer import analyze_graph


@click.command()
@click.option("-c", "--source", help="The source file to compile")
@click.option("-I", "--include-dir", help="Include directory")
@click.option("-o", "--output", help="The output file")
def main(source, include_dir, output):
    if os.path.exists(output):
        os.remove(output)

    log.info(f"ai compiling {source}")
    g = parse_from_file(source)
    g = include_graph(g, include_dir)
    # with open(output + ".cpp", "w") as f:
    #     f.write(g.root.)
    # print_graph(g)
    slice_graph(g)
    analyze_graph(g)
    compile_graph(g)
    write_graph(g, output)


if __name__ == "__main__":
    main()
