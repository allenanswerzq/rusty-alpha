import argparse

from llmcc.parser import parse_from_file
from llmcc.compiler import compile_graph
from llmcc.printer import write_graph, print_graph
from llmcc.config import *
from llmcc.includer import include_graph
from llmcc.slicer import slice_graph


def main():
    parser = argparse.ArgumentParser(description="ai compiler")
    parser.add_argument(
        "-c", "--source", metavar="SOURCE", help="Source file to compile"
    )
    parser.add_argument("-I", "--include-dir", metavar="DIR", help="Include directory")
    parser.add_argument("-o", "--output", metavar="OUTPUT", help="Output file")

    args = parser.parse_args()

    log.info(f"ai compiling {args.source}")
    g = parse_from_file(args.source)
    ng = include_graph(g, args.include_dir)
    if ng:
        g = ng
    log.debug(g.root.text.decode("utf-8"))
    print_graph(g)
    slice_graph(g)
    compile_graph(g)
    write_graph(g, args.output)


if __name__ == "__main__":
    main()
