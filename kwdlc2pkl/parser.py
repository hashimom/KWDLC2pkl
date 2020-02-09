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
import json
import pickle


class Parser:
    def __init__(self, in_file, out_path):
        """ 解析

        :param in_file: 入力パス (knp file)
        :param out_path: 出力パス (directory)
        """
        base, _ = os.path.splitext(os.path.basename(in_file))
        self.in_file = in_file
        self.out_file = out_path + "/" + base

    def __call__(self, file_type="pkl"):
        """

        :param file_type: pkl or json
        :return:
        """
        with open(self.in_file) as f:
            bodies = []
            body = None

            for line in f.readlines():
                line_split = line.split()

                # 文
                if line_split[0] == "#":
                    body = {"id": line_split[1]}
                    chunks = []
                    chunk = None

                # 文節
                elif line_split[0] == "*":
                    if chunk is not None:
                        chunk["words"] = words
                        chunks.append(chunk)

                    chunk = {"link_idx": int(line_split[1][:-1])}
                    words = []

                # 補足？
                elif line_split[0] == "+":
                    pass

                # 文末
                elif line_split[0] == "EOS":
                    if body is not None:
                        body["chunks"] = chunks
                        bodies.append(body)
                    if chunk is not None:
                        chunk["words"] = words
                        chunks.append(chunk)

                    # 係り受け情報の追加
                    for chunk in chunks:
                        if chunk["link_idx"] > 0:
                            chunk["link"] = chunks[chunk["link_idx"]]["words"]

                # 単語
                else:
                    word = {
                        "surface": line_split[0],
                        "original": line_split[2],
                        "read": line_split[1],
                        "position": [[line_split[3], line_split[4]],
                                     [line_split[5], line_split[6]]]
                    }
                    words.append(word)

        # save
        to_json = {"bodies": bodies}
        if file_type == "json":
            with open(self.out_file + ".json", 'w') as f:
                json.dump(to_json, f, indent=2, ensure_ascii=False)
        else:
            with open(self.out_file + ".pkl", "wb") as f:
                pickle.dump(to_json, f)



