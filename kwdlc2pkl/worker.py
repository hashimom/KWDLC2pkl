# -*- coding: utf-8 -*-
"""
 Copyright (c) 2020 Masahiko Hashimoto <hashimom@geeko.jp>
 Permission is hereby granted, free of charge, to any person obtaining a copy
 of this software and associated documentation files (the "Software"), to deal
 in the Software without restriction, including without limitation the rights
 to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 copies of the Software, and to permit persons to whom the Software is
 furnished to do so, subject to the following conditions:
 The above copyright notice and this permission notice shall be included in all
 copies or substantial portions of the Software.
 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 SOFTWARE.
"""
import os
import argparse
from concurrent.futures import ProcessPoolExecutor
from kwdlc2pkl.parser import Parser


def worker(in_file, out_path):
    """ Worker

    :param in_file: 入力パス (knp file)
    :param out_path: 出力パス (directory)
    :return:
    """
    p = Parser(in_file, out_path)
    p()


def main():
    """ main

    :return:
    """
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-i', '--in_path', help='KWDLC path', required=True)
    arg_parser.add_argument('-t', '--in_type', help='Input Type ("train" or "test" or "all")', default="all")
    arg_parser.add_argument('-o', '--out_path', help='output path', default="out/")
    arg_parser.add_argument('-p', '--proc_num', help='process num', default=2)
    args = arg_parser.parse_args()

    out_path = os.path.abspath(args.out_path)
    if not os.path.isdir(out_path):
        os.makedirs(out_path)

    # リスト作成
    in_file_list = []
    if args.in_type != "test":
        # 学習用ファイルリスト追加
        with open(os.path.abspath(args.in_path + "/train.files")) as f:
            for file in f.readlines():
                in_file_list.append(file.rstrip('\n'))
    if args.in_type != "train":
        # テスト用ファイルリスト追加
        with open(os.path.abspath(args.in_path + "/test.files")) as f:
            for file in f.readlines():
                in_file_list.append(file.rstrip('\n'))

    # 入出力パスリストの作成
    for i, path in enumerate(in_file_list):
        in_file_list[i] = os.path.abspath(args.in_path + "/" + path)
    out_path_list = [out_path] * len(in_file_list)

    with ProcessPoolExecutor(max_workers=args.proc_num) as executor:
        executor.map(worker, in_file_list, out_path_list)
    print("output files: %d" % len(in_file_list))


if __name__ == "__main__":
    main()
